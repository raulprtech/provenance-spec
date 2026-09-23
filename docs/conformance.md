# Conformance for draft 0.1.0

A producer conforms to this draft when it emits JSON that validates against `schema/provenance.schema.json` and satisfies the semantic checks below. A consumer conforms when it rejects unsupported `schema_version` values, unresolved local references, and malformed `system_inferred` evidence, and presents the evidence class and limitations to readers.

## Semantic checks

1. IDs are unique within each collection; references resolve to the appropriate collection.
2. Every `system_inferred` evidence item has a visible `inference_basis` and at least one limitation. Other classes do not carry `inference_basis`.
3. Artifact paths are relative to the declared package base and do not escape it. A producer computes hash and size from the actual bytes it packages.
4. `tool_verified` names the narrow operation that was checked. A hash match must not be presented as authenticity or truth.
5. Participant declarations do not silently become verified identity claims.
6. No private reasoning, authorship percentage, or learning score is required or inferred.

The reference CLI checks part of this profile. JSON Schema validation is a separate step because the CLI does not implement the whole JSON Schema vocabulary. The examples are synthetic test vectors, not evidence of field deployment.

## Reproduce locally

```bash
python3 -m unittest discover -s tests -v
python3 src/provenance_tool.py validate examples/synthetic_collaboration/provenance.json
python3 src/provenance_tool.py validate examples/ego_round2_import/public-package/provenance.json
```

If `jsonschema` is already installed, also check both records against Draft 2020-12. This is optional tooling, not a runtime dependency of the reference CLI.

## Known gaps

The scientific-article profile is a design target, not part of 0.1.0 conformance. Passing current checks does not demonstrate capture completeness, human approval, or readiness for confidential article material.

Reproduced gaps include missing required source titles or decision times accepted by the CLI (a missing decision time then breaks rendering), malformed reference objects raising an exception, and unsupported `tool_verified` claims passing structural checks. The CLI `validate` command does not rehash artifact files. The importer copies original attachments without scanning/redacting all their contents and does not fully cross-check manifest metadata. These are open implementation issues, not fixed by this documentation revision.


The Python validator does not fully check date-time syntax or every `additionalProperties` condition from the schema. The draft lacks a separate signed trust profile, independent third-party implementations, and an interoperability test against W3C PROV or RO-Crate.
