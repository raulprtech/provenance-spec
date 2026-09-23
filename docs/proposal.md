# PROVENANCE specification proposal

Status: **public working draft 0.1.0**. This is an independent proposal for discussion and testing. It has not been adopted by a standards organization and does not claim interoperability with W3C PROV or RO-Crate.

## Initial scope and trust

The initial application is documenting captured AI assistance, explicit human decisions, and bounded delegation while preparing scientific articles. We favor trust and voluntary, non-punitive transparency over detection to punish AI use. Scientific claims remain open to scrutiny; the project cannot override external policies or guarantee protection from third-party uses.

The [article profile](scientific-article-profile.md) defines the design target and roadmap. The [trust charter](trust-and-transparency.md) specifies consent, correction, access, and sharing expectations. Automatic capture, model-assisted organization, and author-approved disclosure are planned, not implemented. This revision does not change the 0.1.0 wire format.

## Problem

Collaborative work with AI often leaves a narrative of decisions without a dependable link to the evidence a reviewer can inspect. A useful record should preserve what was declared, observed, and checked, plus the limits of any interpretation. It should remain readable without requiring a private chat transcript.

The [adoption guide](why-adopt.md) gives concrete scientific-article scenarios, checks available today, and conditions for a responsible pilot. The proposed benefit is improved documentary reconstruction; effectiveness has not yet been measured independently.

## Proposed format

The proposal consists of `schema/provenance.schema.json` and the semantic rules in `docs/specification.md`. A conforming record has a version, scope, declared participants, sources, local artifacts with hashes, classified evidence, decisions with alternatives, and limitations. The format distinguishes `observed`, `user_declared`, `tool_verified`, and `system_inferred`. The Markdown view is derived from the JSON record.

The Python tools under `src/` are a reference implementation, not the definition of the standard. The EGO importer is an experimental adapter and is not required for conformance.

## Versioning and change process

- Draft `0.1.0` is open to breaking changes while the evaluation protocol is being piloted.
- Every published revision must identify changes to required fields, allowed values, reference rules, and privacy behavior in `CHANGELOG.md`.
- Consumers should reject an unsupported `schema_version`; they should never silently reinterpret a record.
- Before a stable release, the project needs independent examples, producer/consumer conformance tests, documented migration rules, and a broader prior-art review.

## Relationship to ARIA

ARIA and exams are outside the initial scope. A later educational profile requires separate policy, privacy, accessibility, and evaluation work. Article documentation does not establish learning or suitability for disciplinary decisions. No ARIA integration is claimed.

## Review questions

1. Are the four evidence classes sufficiently precise to support independent reconstruction?
2. Which required fields add documentation burden without improving reconstruction?
3. How should referenced but unavailable evidence be represented without implying verification?
4. What is the smallest trustworthy binding mechanism if authenticity is needed later?
