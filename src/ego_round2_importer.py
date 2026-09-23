#!/usr/bin/env python3
"""Import a synthetic EGO Round 2 export into PROVENANCE v0.1."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

from provenance_tool import ProvenanceError, canonicalize, render_markdown, validate_record

MANIFEST_NAME = "producer-manifest.json"
MANIFEST_PROTOCOL = "ego.offline-experiment-export/v1"
RECEIPT_PROTOCOL = "nigma.sanitized-experiment-receipt/v1"
LEARNING_PROTOCOL = "ego.synthetic-report-learning/v1"
REQUEST_PROTOCOL = "provenance.ego-round2-import-request/v1"
EXPECTED_OUTPUTS = ("plan-receipt.json", "status-receipt.json", "receipt.json", "learning-package.json")
HEX64 = re.compile(r"^[a-f0-9]{64}$")


class ImportError(ProvenanceError):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ImportError(f"cannot read JSON {path.name!r}: {exc}") from exc
    if not isinstance(value, dict):
        raise ImportError(f"{path.name}: expected a JSON object")
    return value


def hash_size(path: Path) -> tuple[str, int]:
    digest, size = hashlib.sha256(), 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def safe_source_file(source_dir: Path, name: str) -> Path:
    pure = PurePosixPath(name)
    if pure.is_absolute() or len(pure.parts) != 1 or pure.name != name or name.startswith("."):
        raise ImportError(f"manifest output name is not a safe basename: {name!r}")
    root, target = source_dir.resolve(), (source_dir.resolve() / name).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ImportError(f"manifest output escapes source directory: {name!r}") from exc
    if not target.is_file() or target.is_symlink():
        raise ImportError(f"manifest output is missing or not a regular file: {name!r}")
    return target


def verify_manifest(source_dir: Path, manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if manifest.get("protocol_version") != MANIFEST_PROTOCOL:
        raise ImportError(f"manifest protocol must be {MANIFEST_PROTOCOL!r}")
    outputs = manifest.get("outputs")
    if not isinstance(outputs, dict):
        raise ImportError("producer-manifest.json.outputs: expected object")
    if set(outputs) != set(EXPECTED_OUTPUTS):
        missing = sorted(set(EXPECTED_OUTPUTS) - set(outputs))
        unexpected = sorted(set(outputs) - set(EXPECTED_OUTPUTS))
        raise ImportError(f"manifest outputs mismatch; missing={missing}, unexpected={unexpected}")
    verified: dict[str, dict[str, Any]] = {}
    for name in EXPECTED_OUTPUTS:
        entry = outputs[name]
        if not isinstance(entry, dict):
            raise ImportError(f"manifest outputs[{name!r}]: expected object")
        expected_hash, expected_size = entry.get("sha256"), entry.get("size_bytes")
        if not isinstance(expected_hash, str) or not HEX64.fullmatch(expected_hash):
            raise ImportError(f"manifest outputs[{name!r}].sha256: invalid SHA-256")
        if not isinstance(expected_size, int) or expected_size < 0:
            raise ImportError(f"manifest outputs[{name!r}].size_bytes: invalid size")
        source = safe_source_file(source_dir, name)
        actual_hash, actual_size = hash_size(source)
        if (actual_hash, actual_size) != (expected_hash, expected_size):
            raise ImportError(
                f"integrity mismatch for {name!r}: expected sha256={expected_hash} size={expected_size}; "
                f"observed sha256={actual_hash} size={actual_size}"
            )
        verified[name] = {"source": source, "sha256": actual_hash, "size_bytes": actual_size}
    return verified


def validate_receipts(documents: dict[str, dict[str, Any]]) -> None:
    expected = {
        "plan-receipt.json": ("experiment.plan", "planned"),
        "status-receipt.json": ("experiment.status", "planned"),
        "receipt.json": ("experiment.report", "completed"),
    }
    shared = ("route_id", "route_digest", "runtime_snapshot_id", "runtime_snapshot_digest", "runtime_run_id")
    report = documents["receipt.json"]
    for name, (capability, state) in expected.items():
        receipt = documents[name]
        if receipt.get("protocol_version") != RECEIPT_PROTOCOL:
            raise ImportError(f"{name}.protocol_version: unsupported receipt protocol")
        if receipt.get("capability") != capability or receipt.get("state") != state:
            raise ImportError(f"{name}: unexpected capability/state")
        for field in shared:
            if receipt.get(field) != report.get(field):
                raise ImportError(f"{name}.{field}: inconsistent receipt chain")


def validate_learning(learning: dict[str, Any]) -> None:
    if learning.get("schema_version") != LEARNING_PROTOCOL:
        raise ImportError(f"learning-package.json.schema_version must be {LEARNING_PROTOCOL!r}")
    generated, summary = learning.get("generated_from"), learning.get("evidence_summary")
    if not isinstance(generated, dict) or not isinstance(summary, dict):
        raise ImportError("learning package requires generated_from and evidence_summary objects")
    catalog = generated.get("evidence")
    if not isinstance(catalog, list):
        raise ImportError("learning-package.json.generated_from.evidence: expected array")
    evidence_ids: set[str] = set()
    for index, item in enumerate(catalog):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ImportError(f"learning evidence[{index}]: invalid entry")
        identifier = item["id"]
        if identifier in evidence_ids:
            raise ImportError(f"learning evidence: duplicate id {identifier!r}")
        if not isinstance(item.get("uri"), str) or not isinstance(item.get("sha256"), str) or not HEX64.fullmatch(item["sha256"]):
            raise ImportError(f"learning evidence[{identifier!r}]: invalid uri/hash")
        evidence_ids.add(identifier)

    def check_refs(refs: Any, location: str) -> None:
        if not isinstance(refs, list):
            raise ImportError(f"{location}: expected array")
        missing = sorted({ref for ref in refs if ref not in evidence_ids})
        if missing:
            raise ImportError(f"{location}: unresolved learning evidence references {missing}")

    observations = summary.get("observations")
    if not isinstance(observations, list):
        raise ImportError("learning-package.json.evidence_summary.observations: expected array")
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict) or not isinstance(observation.get("statement"), str):
            raise ImportError(f"learning observation[{index}]: invalid entry")
        check_refs(observation.get("evidence_ref_ids"), f"learning observation[{index}].evidence_ref_ids")
    interpretation = summary.get("interpretation")
    if not isinstance(interpretation, dict) or not isinstance(interpretation.get("statement"), str):
        raise ImportError("learning interpretation: invalid entry")
    check_refs(interpretation.get("evidence_ref_ids"), "learning interpretation.evidence_ref_ids")


def validate_request(request: dict[str, Any]) -> None:
    if request.get("schema_version") != REQUEST_PROTOCOL:
        raise ImportError(f"import request schema must be {REQUEST_PROTOCOL!r}")
    for field in ("record_title", "declared_by"):
        if not isinstance(request.get(field), str) or not request[field].strip():
            raise ImportError(f"import request {field}: expected non-empty string")
    declarations = request.get("declarations")
    if not isinstance(declarations, list):
        raise ImportError("import request declarations: expected array")
    for index, item in enumerate(declarations):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not isinstance(item.get("statement"), str):
            raise ImportError(f"import declaration[{index}]: id and statement required")
        if not isinstance(item.get("limits"), list) or not item["limits"]:
            raise ImportError(f"import declaration[{index}].limits: expected non-empty array")


def artifact_id(name: str) -> str:
    return "artifact.ego." + name.removesuffix(".json").replace("-", ".")


def source_id(name: str) -> str:
    return "source.ego." + name.removesuffix(".json").replace("-", ".")


def make_record(manifest: dict[str, Any], documents: dict[str, dict[str, Any]], request: dict[str, Any],
                copied: dict[str, dict[str, Any]], manifest_hash: str, manifest_size: int) -> dict[str, Any]:
    learning, report = documents["learning-package.json"], documents["receipt.json"]
    summary = learning["evidence_summary"]
    generated_evidence = {item["id"]: item for item in learning["generated_from"]["evidence"]}
    artifacts = [{
        "id": "artifact.ego.producer.manifest", "path": f"artifacts/{MANIFEST_NAME}",
        "media_type": "application/json", "role": "Copied producer manifest; locally hashed but not self-attested by that manifest",
        "verification": "tool_verified", "sha256": manifest_hash, "size_bytes": manifest_size,
    }]
    sources = [{
        "id": "source.ego.producer.manifest", "title": "Synthetic EGO Round 2 producer manifest",
        "kind": "tool_output", "locator": f"artifacts/{MANIFEST_NAME}", "classification": "observed",
        "notes": "Relative public-package locator; original filesystem path intentionally omitted.",
    }]
    for name in EXPECTED_OUTPUTS:
        metadata = copied[name]
        artifacts.append({
            "id": artifact_id(name), "path": f"artifacts/{name}", "media_type": "application/json",
            "role": "Synthetic EGO Round 2 output verified against producer manifest", "verification": "tool_verified",
            "sha256": metadata["sha256"], "size_bytes": metadata["size_bytes"],
        })
        sources.append({
            "id": source_id(name), "title": f"Imported synthetic output: {name}", "kind": "tool_output",
            "locator": f"artifacts/{name}", "classification": "tool_verified",
            "notes": "Hash and size match producer-manifest.json; authenticity is not established.",
        })
    for evidence_id, item in sorted(generated_evidence.items()):
        sources.append({
            "id": f"source.learning.{evidence_id}", "title": f"Referenced but unavailable learning evidence: {evidence_id}",
            "kind": "tool_output", "locator": item["uri"], "classification": "observed",
            "notes": f"Declared SHA-256 {item['sha256']}; payload absent, digest not verified.",
        })

    evidence: list[dict[str, Any]] = []
    for name in EXPECTED_OUTPUTS:
        evidence.append({
            "id": "evidence.integrity." + name.removesuffix(".json").replace("-", "."),
            "classification": "tool_verified", "statement": f"{name} matched the SHA-256 and size declared in producer-manifest.json.",
            "recorded_by": "participant.provenance.importer",
            "source_refs": ["source.ego.producer.manifest", source_id(name)],
            "artifact_refs": ["artifact.ego.producer.manifest", artifact_id(name)],
            "limits": ["This verifies local byte integrity against the supplied manifest, not provenance authenticity."],
        })
    for name in ("plan-receipt.json", "status-receipt.json", "receipt.json"):
        receipt = documents[name]
        evidence.append({
            "id": "evidence.receipt." + receipt["capability"].split(".")[-1], "classification": "observed",
            "statement": f"The imported {name} declares capability {receipt['capability']!r}, state {receipt['state']!r}, and timestamp {receipt['observed_at']!r}.",
            "recorded_by": "participant.provenance.importer", "source_refs": [source_id(name)],
            "artifact_refs": [artifact_id(name)], "limits": ["The importer observed declared fields; it did not independently observe execution."],
        })
    for declaration in request["declarations"]:
        evidence.append({
            "id": "evidence.user." + declaration["id"], "classification": "user_declared",
            "statement": declaration["statement"], "recorded_by": "participant.import.operator",
            "source_refs": [], "artifact_refs": [], "limits": declaration["limits"],
        })
    for observation in summary["observations"]:
        refs = observation["evidence_ref_ids"]
        evidence.append({
            "id": "evidence.learning." + observation["id"].replace("_", "."), "classification": "observed",
            "statement": f"The learning package declares this observation: {observation['statement']}",
            "recorded_by": "participant.ego.producer",
            "source_refs": [source_id("learning-package.json"), *(f"source.learning.{ref}" for ref in refs)],
            "artifact_refs": [artifact_id("learning-package.json")],
            "limits": ["The referenced evidence payloads are not present; this records a declaration, not independent verification."],
        })
    interpretation = summary["interpretation"]
    evidence.append({
        "id": "evidence.learning.interpretation", "classification": "system_inferred",
        "statement": interpretation["statement"], "recorded_by": "participant.ego.producer",
        "source_refs": [source_id("learning-package.json"), *(f"source.learning.{ref}" for ref in interpretation["evidence_ref_ids"])],
        "artifact_refs": [artifact_id("learning-package.json")],
        "inference_basis": "The imported learning package labels this statement as interpretation and links it to its internal evidence catalogue.",
        "limits": [*summary["limitations"], "The underlying evidence payloads are absent and were not hash-verified."],
    })
    evidence.append({
        "id": "evidence.workflow.reconstructed", "classification": "system_inferred",
        "statement": "The three receipts represent the semantic sequence plan, status, then report for one synthetic runtime run.",
        "recorded_by": "participant.provenance.importer",
        "source_refs": [source_id(name) for name in ("plan-receipt.json", "status-receipt.json", "receipt.json")],
        "artifact_refs": [artifact_id(name) for name in ("plan-receipt.json", "status-receipt.json", "receipt.json")],
        "inference_basis": "Capabilities are experiment.plan, experiment.status, and experiment.report; shared route/runtime fields match.",
        "limits": ["All receipts have the same timestamp, so chronological order is not independently established."],
    })
    evidence.append({
        "id": "evidence.learning.package.boundary", "classification": "observed",
        "statement": f"The imported learning package declares {len(learning.get('study_plan', {}).get('study_sessions', []))} study sessions and comprehension exercise {learning.get('comprehension_exercise_id')!r}.",
        "recorded_by": "participant.provenance.importer", "source_refs": [source_id("learning-package.json")],
        "artifact_refs": [artifact_id("learning-package.json")],
        "limits": ["A declared plan or exercise does not show that any person completed it or learned from it."],
    })
    limits = [
        "Integrity checks establish byte equality with the supplied manifest, not authenticity, identity, truth, or authorization.",
        "The import is synthetic and does not show integration with a live ARIA or Nigma service.",
        "The learning package is a plan and exercise set; it does not demonstrate completion, comprehension, mastery, or learning.",
        "Referenced internal evidence payloads are catalogued but absent from the exported bundle, so their hashes are not verified.",
        *(item for item in summary.get("limitations", []) if isinstance(item, str)),
    ]
    return canonicalize({
        "schema_version": "0.1.0", "record_id": "record.ego.round2." + report["id"].split("-")[-1],
        "title": request["record_title"], "created_at": manifest["generated_at"],
        "scope": {
            "description": "Offline import of a synthetic EGO Round 2 receipt chain and learning package.",
            "intended_use": "Document integrity checks, evidence boundaries, and a reconstructable synthetic workflow.",
            "exclusions": [
                "No claim of authentic identity, production execution, scientific validity, authorship share, comprehension, mastery, or learning.",
                "No private filesystem paths, chats, patient data, test data, or credentials are included.",
            ],
        },
        "participants": [
            {"id": "participant.ego.producer", "kind": "tool", "display_name": manifest["producer"],
             "declaration_class": "observed", "declared_by": "producer-manifest.json", "role": "synthetic export producer"},
            {"id": "participant.import.operator", "kind": "human", "display_name": request["declared_by"],
             "declaration_class": "user_declared", "declared_by": "import request", "role": "scope declarant"},
            {"id": "participant.provenance.importer", "kind": "tool", "display_name": "PROVENANCE EGO Round 2 importer",
             "declaration_class": "tool_verified", "declared_by": "src/ego_round2_importer.py", "role": "integrity verifier and deterministic recorder"},
        ],
        "sources": sources, "artifacts": artifacts, "evidence": evidence, "decisions": [], "limits": limits, "redactions": [],
    })


def import_bundle(source_dir: Path, output_dir: Path, request_path: Path) -> dict[str, Any]:
    source_dir = source_dir.resolve()
    if output_dir.exists():
        raise ImportError(f"output directory already exists: {output_dir}")
    manifest_path = safe_source_file(source_dir, MANIFEST_NAME)
    manifest = load_object(manifest_path)
    verified = verify_manifest(source_dir, manifest)
    documents = {name: load_object(metadata["source"]) for name, metadata in verified.items()}
    validate_receipts(documents)
    validate_learning(documents["learning-package.json"])
    request = load_object(request_path)
    validate_request(request)
    report_artifacts = documents["receipt.json"].get("artifacts")
    learning_meta = verified["learning-package.json"]
    if not isinstance(report_artifacts, list) or len(report_artifacts) != 1:
        raise ImportError("receipt.json.artifacts: expected exactly one learning package artifact")
    declared_learning = report_artifacts[0]
    if (declared_learning.get("sha256"), declared_learning.get("size_bytes")) != (learning_meta["sha256"], learning_meta["size_bytes"]):
        raise ImportError("receipt.json learning-package artifact does not match verified output")
    manifest_hash, manifest_size = hash_size(manifest_path)
    parent = output_dir.parent.resolve()
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".provenance-import-", dir=parent) as temporary:
        staging = Path(temporary) / output_dir.name
        artifacts_dir = staging / "artifacts"
        artifacts_dir.mkdir(parents=True)
        shutil.copyfile(manifest_path, artifacts_dir / MANIFEST_NAME)
        for name, metadata in verified.items():
            shutil.copyfile(metadata["source"], artifacts_dir / name)
        copied = {name: {"sha256": metadata["sha256"], "size_bytes": metadata["size_bytes"]} for name, metadata in verified.items()}
        record = make_record(manifest, documents, request, copied, manifest_hash, manifest_size)
        errors = validate_record(record)
        if errors:
            raise ImportError("generated PROVENANCE record is invalid:\n- " + "\n- ".join(errors))
        (staging / "provenance.json").write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (staging / "PROVENANCE.md").write_text(render_markdown(record), encoding="utf-8")
        os.replace(staging, output_dir)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--declaration-file", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        record = import_bundle(args.source_dir, args.output_dir, args.declaration_file)
        print(f"imported: {args.output_dir}")
        print(f"record: {record['record_id']}")
        return 0
    except (OSError, ImportError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
