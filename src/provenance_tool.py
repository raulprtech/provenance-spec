#!/usr/bin/env python3
"""Deterministic builder and semantic validator for PROVENANCE v0.1."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

SCHEMA_VERSION = "0.1.0"
CLASSIFICATIONS = {"observed", "user_declared", "tool_verified", "system_inferred"}
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._:-]{0,127}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
SENSITIVE_KEY_RE = re.compile(
    r"(?i)(?:^|_)(?:api_?key|access_?token|auth(?:orization)?|password|passwd|private_?key|secret)(?:$|_)"
)
SECRET_PATTERNS = (
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{12,}={0,2}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)
FORBIDDEN_KEYS = {
    "chain_of_thought",
    "private_reasoning",
    "reasoning_trace",
    "ai_percentage",
    "authorship_score",
    "learning_score",
}
REQUIRED_TOP = {
    "schema_version",
    "record_id",
    "title",
    "created_at",
    "scope",
    "participants",
    "sources",
    "artifacts",
    "evidence",
    "decisions",
    "limits",
    "redactions",
}


class ProvenanceError(ValueError):
    pass


def _pointer(parts: Iterable[str]) -> str:
    escaped = [part.replace("~", "~0").replace("/", "~1") for part in parts]
    return "/" + "/".join(escaped) if escaped else ""


def redact_secrets(value: Any) -> tuple[Any, list[dict[str, str]]]:
    """Return a deep-copied value with conservative secret redaction metadata."""
    redactions: list[dict[str, str]] = []

    def visit(node: Any, path: list[str]) -> Any:
        if isinstance(node, dict):
            result: dict[str, Any] = {}
            for key, child in node.items():
                child_path = [*path, str(key)]
                if SENSITIVE_KEY_RE.search(str(key)) and key != "redactions":
                    result[key] = "[REDACTED]"
                    redactions.append(
                        {
                            "json_pointer": _pointer(child_path),
                            "reason": "potential_secret",
                            "replacement": "[REDACTED]",
                        }
                    )
                else:
                    result[key] = visit(child, child_path)
            return result
        if isinstance(node, list):
            return [visit(item, [*path, str(index)]) for index, item in enumerate(node)]
        if isinstance(node, str):
            cleaned = node
            matched = False
            for pattern in SECRET_PATTERNS:
                cleaned, count = pattern.subn("[REDACTED]", cleaned)
                matched = matched or count > 0
            if matched:
                redactions.append(
                    {
                        "json_pointer": _pointer(path),
                        "reason": "potential_secret",
                        "replacement": "[REDACTED]",
                    }
                )
            return cleaned
        return copy.deepcopy(node)

    sanitized = visit(value, [])
    if not isinstance(sanitized, dict):
        raise ProvenanceError("root: expected object")
    prior = sanitized.get("redactions", [])
    if not isinstance(prior, list):
        prior = []
    sanitized["redactions"] = sorted(
        [*prior, *redactions], key=lambda item: (item.get("json_pointer", ""), item.get("reason", ""))
    )
    return sanitized, redactions


def _safe_artifact_path(base_dir: Path, relative: str) -> Path:
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts or relative.startswith("~"):
        raise ProvenanceError(f"artifact path must remain relative to base directory: {relative!r}")
    base = base_dir.resolve()
    target = (base / Path(*posix.parts)).resolve()
    try:
        target.relative_to(base)
    except ValueError as exc:
        raise ProvenanceError(f"artifact path escapes base directory: {relative!r}") from exc
    if not target.is_file():
        raise ProvenanceError(f"artifact not found: {relative!r}")
    return target


def materialize_artifacts(record: dict[str, Any], base_dir: Path) -> None:
    artifacts = record.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ProvenanceError("artifacts: expected array")
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict) or not isinstance(artifact.get("path"), str):
            raise ProvenanceError(f"artifacts[{index}].path: expected string")
        target = _safe_artifact_path(base_dir, artifact["path"])
        digest = hashlib.sha256()
        size = 0
        with target.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
                size += len(chunk)
        artifact["sha256"] = digest.hexdigest()
        artifact["size_bytes"] = size
        artifact["verification"] = "tool_verified"


def _walk_forbidden(node: Any, path: str, errors: list[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else key
            if key in FORBIDDEN_KEYS:
                errors.append(f"{child}: forbidden field")
            if SENSITIVE_KEY_RE.search(key) and value != "[REDACTED]":
                errors.append(f"{child}: potential secret must be redacted")
            _walk_forbidden(value, child, errors)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _walk_forbidden(value, f"{path}[{index}]", errors)
    elif isinstance(node, str):
        for pattern in SECRET_PATTERNS:
            if pattern.search(node):
                errors.append(f"{path}: potential secret must be redacted")
                break


def _require_nonempty_string(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: expected non-empty string")


def _collect_ids(items: Any, path: str, errors: list[str]) -> set[str]:
    result: set[str] = set()
    if not isinstance(items, list):
        errors.append(f"{path}: expected array")
        return result
    for index, item in enumerate(items):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_path}: expected object")
            continue
        identifier = item.get("id")
        if not isinstance(identifier, str) or not ID_RE.fullmatch(identifier):
            errors.append(f"{item_path}.id: invalid identifier")
        elif identifier in result:
            errors.append(f"{item_path}.id: duplicate identifier {identifier!r}")
        else:
            result.add(identifier)
    return result


def _check_refs(refs: Any, allowed: set[str], path: str, errors: list[str]) -> None:
    if not isinstance(refs, list):
        errors.append(f"{path}: expected array")
        return
    for index, ref in enumerate(refs):
        if ref not in allowed:
            errors.append(f"{path}[{index}]: unresolved reference {ref!r}")


def validate_record(record: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["root: expected object"]

    missing = sorted(REQUIRED_TOP - set(record))
    unexpected = sorted(set(record) - REQUIRED_TOP)
    errors.extend(f"root: missing required field {name!r}" for name in missing)
    errors.extend(f"root: unexpected field {name!r}" for name in unexpected)
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version: expected {SCHEMA_VERSION!r}")
    if not isinstance(record.get("record_id"), str) or not ID_RE.fullmatch(record.get("record_id", "")):
        errors.append("record_id: invalid identifier")
    _require_nonempty_string(record.get("title"), "title", errors)
    _require_nonempty_string(record.get("created_at"), "created_at", errors)

    scope = record.get("scope")
    if not isinstance(scope, dict):
        errors.append("scope: expected object")
    else:
        if set(scope) != {"description", "intended_use", "exclusions"}:
            errors.append("scope: expected exactly description, intended_use, exclusions")
        _require_nonempty_string(scope.get("description"), "scope.description", errors)
        _require_nonempty_string(scope.get("intended_use"), "scope.intended_use", errors)
        if not isinstance(scope.get("exclusions"), list):
            errors.append("scope.exclusions: expected array")

    participant_ids = _collect_ids(record.get("participants"), "participants", errors)
    source_ids = _collect_ids(record.get("sources"), "sources", errors)
    artifact_ids = _collect_ids(record.get("artifacts"), "artifacts", errors)
    evidence_ids = _collect_ids(record.get("evidence"), "evidence", errors)
    _collect_ids(record.get("decisions"), "decisions", errors)

    for index, participant in enumerate(record.get("participants", [])):
        if not isinstance(participant, dict):
            continue
        if participant.get("kind") not in {"human", "ai_system", "tool", "organization"}:
            errors.append(f"participants[{index}].kind: invalid value")
        if participant.get("declaration_class") not in CLASSIFICATIONS:
            errors.append(f"participants[{index}].declaration_class: invalid classification")
        _require_nonempty_string(participant.get("display_name"), f"participants[{index}].display_name", errors)
        _require_nonempty_string(participant.get("declared_by"), f"participants[{index}].declared_by", errors)

    for index, artifact in enumerate(record.get("artifacts", [])):
        if not isinstance(artifact, dict):
            continue
        path = artifact.get("path")
        if not isinstance(path, str) or PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
            errors.append(f"artifacts[{index}].path: must be a safe relative path")
        if artifact.get("verification") != "tool_verified":
            errors.append(f"artifacts[{index}].verification: expected 'tool_verified'")
        if not isinstance(artifact.get("sha256"), str) or not SHA256_RE.fullmatch(artifact.get("sha256", "")):
            errors.append(f"artifacts[{index}].sha256: expected lowercase SHA-256")
        if not isinstance(artifact.get("size_bytes"), int) or artifact.get("size_bytes", -1) < 0:
            errors.append(f"artifacts[{index}].size_bytes: expected non-negative integer")

    for index, item in enumerate(record.get("evidence", [])):
        if not isinstance(item, dict):
            continue
        classification = item.get("classification")
        if classification not in CLASSIFICATIONS:
            errors.append(f"evidence[{index}].classification: invalid classification")
        if item.get("recorded_by") not in participant_ids:
            errors.append(f"evidence[{index}].recorded_by: unresolved participant reference")
        _require_nonempty_string(item.get("statement"), f"evidence[{index}].statement", errors)
        _check_refs(item.get("source_refs"), source_ids, f"evidence[{index}].source_refs", errors)
        _check_refs(item.get("artifact_refs"), artifact_ids, f"evidence[{index}].artifact_refs", errors)
        limits = item.get("limits")
        if not isinstance(limits, list):
            errors.append(f"evidence[{index}].limits: expected array")
        if classification == "system_inferred":
            _require_nonempty_string(item.get("inference_basis"), f"evidence[{index}].inference_basis", errors)
            if not isinstance(limits, list) or not limits:
                errors.append(f"evidence[{index}].limits: system inference requires at least one limit")
        elif "inference_basis" in item:
            errors.append(f"evidence[{index}].inference_basis: allowed only for system_inferred")

    for index, decision in enumerate(record.get("decisions", [])):
        if not isinstance(decision, dict):
            continue
        if decision.get("status") not in {"proposed", "accepted", "rejected", "deferred"}:
            errors.append(f"decisions[{index}].status: invalid value")
        _require_nonempty_string(decision.get("summary"), f"decisions[{index}].summary", errors)
        _require_nonempty_string(decision.get("rationale_summary"), f"decisions[{index}].rationale_summary", errors)
        _check_refs(decision.get("decision_maker_refs"), participant_ids, f"decisions[{index}].decision_maker_refs", errors)
        if isinstance(decision.get("decision_maker_refs"), list) and not decision["decision_maker_refs"]:
            errors.append(f"decisions[{index}].decision_maker_refs: expected at least one reference")
        _check_refs(decision.get("evidence_refs"), evidence_ids, f"decisions[{index}].evidence_refs", errors)
        _check_refs(decision.get("artifact_refs"), artifact_ids, f"decisions[{index}].artifact_refs", errors)
        alternatives = decision.get("alternatives")
        if not isinstance(alternatives, list):
            errors.append(f"decisions[{index}].alternatives: expected array")
        else:
            for alt_index, alternative in enumerate(alternatives):
                if not isinstance(alternative, dict):
                    errors.append(f"decisions[{index}].alternatives[{alt_index}]: expected object")
                    continue
                if alternative.get("disposition") not in {"selected", "rejected", "deferred", "not_evaluated"}:
                    errors.append(f"decisions[{index}].alternatives[{alt_index}].disposition: invalid value")
                _require_nonempty_string(alternative.get("label"), f"decisions[{index}].alternatives[{alt_index}].label", errors)
                _require_nonempty_string(alternative.get("reason"), f"decisions[{index}].alternatives[{alt_index}].reason", errors)

    if not isinstance(record.get("limits"), list) or not record.get("limits"):
        errors.append("limits: expected non-empty array")
    if not isinstance(record.get("redactions"), list):
        errors.append("redactions: expected array")
    _walk_forbidden(record, "", errors)
    return sorted(set(errors))


def canonicalize(record: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(record)
    for name in ("participants", "sources", "artifacts", "evidence", "decisions"):
        if isinstance(result.get(name), list):
            result[name] = sorted(result[name], key=lambda item: item.get("id", "") if isinstance(item, dict) else "")
    return result


def _refs(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "None declared"


def render_markdown(record: dict[str, Any]) -> str:
    lines = [
        f"# {record['title']}",
        "",
        f"Record: `{record['record_id']}`  ",
        f"Schema: `{record['schema_version']}`  ",
        f"Created: `{record['created_at']}`",
        "",
        "## Scope",
        "",
        record["scope"]["description"],
        "",
        f"Intended use: {record['scope']['intended_use']}",
        "",
        "Excluded claims:",
        "",
    ]
    lines.extend(f"- {item}" for item in record["scope"]["exclusions"])
    lines.extend(["", "## Participants (declared)", ""])
    for item in record["participants"]:
        role = f"; role: {item['role']}" if item.get("role") else ""
        lines.append(
            f"- `{item['id']}` — {item['display_name']} ({item['kind']}; "
            f"{item['declaration_class']}; declared by: {item['declared_by']}{role})"
        )
    lines.extend(["", "## Decisions", ""])
    for decision in record["decisions"]:
        lines.extend(
            [
                f"### {decision['id']}: {decision['summary']}",
                "",
                f"Status: **{decision['status']}**; decided: `{decision['decided_at']}`; "
                f"decision makers: {_refs(decision['decision_maker_refs'])}.",
                "",
                f"Recorded rationale summary: {decision['rationale_summary']}",
                "",
                "Alternatives:",
                "",
            ]
        )
        lines.extend(
            f"- **{alternative['disposition']}** — {alternative['label']}: {alternative['reason']}"
            for alternative in decision["alternatives"]
        )
        lines.extend(
            [
                "",
                f"Evidence: {_refs(decision['evidence_refs'])}. Artifacts: {_refs(decision['artifact_refs'])}.",
                "",
                "Limits:",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in decision["limits"])
        lines.append("")
    lines.extend(["## Evidence", ""])
    for item in record["evidence"]:
        lines.append(f"- `{item['id']}` **{item['classification']}** — {item['statement']}")
        lines.append(f"  - Recorded by: `{item['recorded_by']}`; sources: {_refs(item['source_refs'])}; artifacts: {_refs(item['artifact_refs'])}.")
        if item.get("inference_basis"):
            lines.append(f"  - Inference basis: {item['inference_basis']}")
        for limit in item["limits"]:
            lines.append(f"  - Limit: {limit}")
    lines.extend(["", "## Artifacts", ""])
    for item in record["artifacts"]:
        lines.append(
            f"- `{item['id']}` — `{item['path']}` ({item['media_type']}, {item['size_bytes']} bytes); "
            f"SHA-256 `{item['sha256']}`; verification: **{item['verification']}**; role: {item['role']}"
        )
    lines.extend(["", "## Sources", ""])
    for item in record["sources"]:
        lines.append(
            f"- `{item['id']}` — {item['title']} ({item['kind']}; {item['classification']}): {item['locator']}"
        )
    lines.extend(["", "## Record-wide limits", ""])
    lines.extend(f"- {item}" for item in record["limits"])
    lines.extend(["", "## Redactions", ""])
    if record["redactions"]:
        lines.extend(
            f"- `{item['json_pointer']}` — {item['reason']}; replacement: `{item['replacement']}`"
            for item in record["redactions"]
        )
    else:
        lines.append("- No automatic redactions recorded.")
    lines.extend(
        [
            "",
            "---",
            "",
            "This document is generated from the structured record. It reports supplied, observable metadata; it does not expose private reasoning, allocate authorship percentages, or demonstrate learning.",
            "",
        ]
    )
    return "\n".join(lines)


def build_record(raw: Any, base_dir: Path) -> tuple[dict[str, Any], str]:
    sanitized, _ = redact_secrets(raw)
    materialize_artifacts(sanitized, base_dir)
    result = canonicalize(sanitized)
    errors = validate_record(result)
    if errors:
        raise ProvenanceError("validation failed:\n- " + "\n- ".join(errors))
    return result, render_markdown(result)


def _load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a materialized provenance JSON file")
    validate.add_argument("input", type=Path)
    build = subparsers.add_parser("build", help="sanitize, hash, validate and render a supplied record")
    build.add_argument("input", type=Path)
    build.add_argument("--base-dir", type=Path, required=True)
    build.add_argument("--json-out", type=Path, required=True)
    build.add_argument("--markdown-out", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate":
            errors = validate_record(_load(args.input))
            if errors:
                raise ProvenanceError("validation failed:\n- " + "\n- ".join(errors))
            print(f"valid: {args.input}")
            return 0
        record, markdown = build_record(_load(args.input), args.base_dir)
        _write_json(args.json_out, record)
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(markdown, encoding="utf-8")
        print(f"built: {args.json_out}")
        print(f"built: {args.markdown_out}")
        return 0
    except (OSError, json.JSONDecodeError, ProvenanceError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

