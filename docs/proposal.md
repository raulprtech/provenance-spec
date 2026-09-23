# PROVENANCE specification proposal

Status: **public working draft 0.1.0**. This is an independent proposal for discussion and testing. It has not been adopted by a standards organization and does not claim interoperability with W3C PROV or RO-Crate.

## Problem

Collaborative work with AI often leaves a narrative of decisions without a dependable link to the evidence a reviewer can inspect. A useful record should preserve what was declared, observed, and checked, plus the limits of any interpretation. It should remain readable without requiring a private chat transcript.

## Proposed format

The proposal consists of `schema/provenance.schema.json` and the semantic rules in `docs/specification.md`. A conforming record has a version, scope, declared participants, sources, local artifacts with hashes, classified evidence, decisions with alternatives, and limitations. The format distinguishes `observed`, `user_declared`, `tool_verified`, and `system_inferred`. The Markdown view is derived from the JSON record.

The Python tools under `src/` are a reference implementation, not the definition of the standard. The EGO importer is an experimental adapter and is not required for conformance.

## Versioning and change process

- Draft `0.1.0` is open to breaking changes while the evaluation protocol is being piloted.
- Every published revision must identify changes to required fields, allowed values, reference rules, and privacy behavior in `CHANGELOG.md`.
- Consumers should reject an unsupported `schema_version`; they should never silently reinterpret a record.
- Before a stable release, the project needs independent examples, producer/consumer conformance tests, documented migration rules, and a broader prior-art review.

## Relationship to ARIA

ARIA may consume this format through a versioned adapter after it can distinguish declared facts from checked facts and display limits. The current publication does not attest that ARIA has implemented the adapter or that any user learned from a learning package.

## Review questions

1. Are the four evidence classes sufficiently precise to support independent reconstruction?
2. Which required fields add documentation burden without improving reconstruction?
3. How should referenced but unavailable evidence be represented without implying verification?
4. What is the smallest trustworthy binding mechanism if authenticity is needed later?
