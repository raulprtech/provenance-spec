# Synthetic decision provenance example

Record: `record.synthetic.001`  
Schema: `0.1.0`  
Created: `2026-09-19T18:00:00Z`

## Scope

A fictional collaboration chooses the first format for an offline documentation prototype.

Intended use: Demonstrate representable observable records without exposing a private conversation.

Excluded claims:

- No claim about authorship share.
- No claim that a participant learned.
- No claim that file hashes authenticate people or statements.

## Participants (declared)

- `participant.ai.01` — Fictional assistant (ai_system; user_declared; declared by: synthetic fixture author; role: proposal generator and recorder)
- `participant.human.01` — Fictional project lead (human; user_declared; declared by: synthetic fixture author; role: decision maker)
- `participant.tool.01` — PROVENANCE v0.1 builder (tool; tool_verified; declared by: src/provenance_tool.py; role: hashing and deterministic rendering)

## Decisions

### decision.format.01: Use structured JSON plus generated Markdown for the first prototype.

Status: **accepted**; decided: `2026-09-19T18:00:00Z`; decision makers: `participant.human.01`.

Recorded rationale summary: The supplied note records a preference for an offline, deterministic documentation prototype.

Alternatives:

- **deferred** — Signed append-only ledger: Identity and signature infrastructure are outside the synthetic v0.1 scope.
- **rejected** — Unstructured narrative only: It would not support machine validation or explicit reference checks.

Evidence: `evidence.note.exists`, `evidence.choice.declared`. Artifacts: `artifact.note.01`.

Limits:

- This decision is fictional and does not establish effectiveness in real projects.

## Evidence

- `evidence.choice.declared` **user_declared** — The fictional project lead selected the deterministic offline prototype.
  - Recorded by: `participant.ai.01`; sources: `source.note.01`; artifacts: `artifact.note.01`.
  - Limit: The example is synthetic and is not evidence about a real collaboration.
- `evidence.motivation.inferred` **system_inferred** — The selected option may have been favored because it reduced operational dependencies.
  - Recorded by: `participant.ai.01`; sources: `source.note.01`; artifacts: None declared.
  - Inference basis: The note states that the selected prototype is offline and that the signed-ledger option was deferred as out of scope.
  - Limit: This is an interpretation, not a declared motive or private reasoning trace.
- `evidence.note.exists` **tool_verified** — The referenced note existed at build time and its bytes were hashed.
  - Recorded by: `participant.tool.01`; sources: `source.note.01`; artifacts: `artifact.note.01`.
  - Limit: Existence and hash do not establish truth or human identity.

## Artifacts

- `artifact.note.01` — `artifacts/decision-note.txt` (text/plain, 293 bytes); SHA-256 `f57f75c015ee682c571b34e70f00052e3929cebae915e9677922e175c592d295`; verification: **tool_verified**; role: Observable synthetic decision note

## Sources

- `source.note.01` — Synthetic decision note (user_record; observed): artifacts/decision-note.txt

## Record-wide limits

- This is a synthetic fixture, not a reconstructed private conversation.
- The record is self-asserted except where a field is explicitly tool_verified.
- A successful build proves format and local reference consistency only.

## Redactions

- No automatic redactions recorded.

---

This document is generated from the structured record. It reports supplied, observable metadata; it does not expose private reasoning, allocate authorship percentages, or demonstrate learning.
