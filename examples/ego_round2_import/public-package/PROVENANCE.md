# Synthetic EGO Round 2 receipt provenance

Record: `record.ego.round2.22d2e3aea021e6e4`  
Schema: `0.1.0`  
Created: `2026-09-20T12:05:00.000Z`

## Scope

Offline import of a synthetic EGO Round 2 receipt chain and learning package.

Intended use: Document integrity checks, evidence boundaries, and a reconstructable synthetic workflow.

Excluded claims:

- No claim of authentic identity, production execution, scientific validity, authorship share, comprehension, mastery, or learning.
- No private filesystem paths, chats, patient data, test data, or credentials are included.

## Participants (declared)

- `participant.ego.producer` — ego-offline-integration-harness (tool; observed; declared by: producer-manifest.json; role: synthetic export producer)
- `participant.import.operator` — Pseudonymous import operator (human; user_declared; declared by: import request; role: scope declarant)
- `participant.provenance.importer` — PROVENANCE EGO Round 2 importer (tool; tool_verified; declared by: src/ego_round2_importer.py; role: integrity verifier and deterministic recorder)

## Decisions

## Evidence

- `evidence.integrity.learning.package` **tool_verified** — learning-package.json matched the SHA-256 and size declared in producer-manifest.json.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.producer.manifest`, `source.ego.learning.package`; artifacts: `artifact.ego.producer.manifest`, `artifact.ego.learning.package`.
  - Limit: This verifies local byte integrity against the supplied manifest, not provenance authenticity.
- `evidence.integrity.plan.receipt` **tool_verified** — plan-receipt.json matched the SHA-256 and size declared in producer-manifest.json.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.producer.manifest`, `source.ego.plan.receipt`; artifacts: `artifact.ego.producer.manifest`, `artifact.ego.plan.receipt`.
  - Limit: This verifies local byte integrity against the supplied manifest, not provenance authenticity.
- `evidence.integrity.receipt` **tool_verified** — receipt.json matched the SHA-256 and size declared in producer-manifest.json.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.producer.manifest`, `source.ego.receipt`; artifacts: `artifact.ego.producer.manifest`, `artifact.ego.receipt`.
  - Limit: This verifies local byte integrity against the supplied manifest, not provenance authenticity.
- `evidence.integrity.status.receipt` **tool_verified** — status-receipt.json matched the SHA-256 and size declared in producer-manifest.json.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.producer.manifest`, `source.ego.status.receipt`; artifacts: `artifact.ego.producer.manifest`, `artifact.ego.status.receipt`.
  - Limit: This verifies local byte integrity against the supplied manifest, not provenance authenticity.
- `evidence.learning.interpretation` **system_inferred** — El fixture demuestra una transformación local repetible para esta entrada sintética.
  - Recorded by: `participant.ego.producer`; sources: `source.ego.learning.package`, `source.learning.artifact_steps`, `source.learning.artifact_digest`; artifacts: `artifact.ego.learning.package`.
  - Inference basis: The imported learning package labels this statement as interpretation and links it to its internal evidence catalogue.
  - Limit: No demuestra que exista una integración de red con Nigma o ARIA.
  - Limit: No demuestra validez científica ni comportamiento con workloads reales.
  - Limit: The underlying evidence payloads are absent and were not hash-verified.
- `evidence.learning.observation.digest` **observed** — The learning package declares this observation: Dos evaluaciones del mismo contenido produjeron el mismo digest.
  - Recorded by: `participant.ego.producer`; sources: `source.ego.learning.package`, `source.learning.artifact_digest`; artifacts: `artifact.ego.learning.package`.
  - Limit: The referenced evidence payloads are not present; this records a declaration, not independent verification.
- `evidence.learning.observation.steps` **observed** — The learning package declares this observation: El fixture completó los tres pasos declarados sin reintentos.
  - Recorded by: `participant.ego.producer`; sources: `source.ego.learning.package`, `source.learning.artifact_steps`; artifacts: `artifact.ego.learning.package`.
  - Limit: The referenced evidence payloads are not present; this records a declaration, not independent verification.
- `evidence.learning.package.boundary` **observed** — The imported learning package declares 3 study sessions and comprehension exercise 'quiz_evidence_boundary'.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.learning.package`; artifacts: `artifact.ego.learning.package`.
  - Limit: A declared plan or exercise does not show that any person completed it or learned from it.
- `evidence.receipt.plan` **observed** — The imported plan-receipt.json declares capability 'experiment.plan', state 'planned', and timestamp '2026-09-20T12:05:00Z'.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.plan.receipt`; artifacts: `artifact.ego.plan.receipt`.
  - Limit: The importer observed declared fields; it did not independently observe execution.
- `evidence.receipt.report` **observed** — The imported receipt.json declares capability 'experiment.report', state 'completed', and timestamp '2026-09-20T12:05:00Z'.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.receipt`; artifacts: `artifact.ego.receipt`.
  - Limit: The importer observed declared fields; it did not independently observe execution.
- `evidence.receipt.status` **observed** — The imported status-receipt.json declares capability 'experiment.status', state 'planned', and timestamp '2026-09-20T12:05:00Z'.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.status.receipt`; artifacts: `artifact.ego.status.receipt`.
  - Limit: The importer observed declared fields; it did not independently observe execution.
- `evidence.user.scope.synthetic.round2` **user_declared** — The operator declares that this import is limited to the supplied synthetic Round 2 export.
  - Recorded by: `participant.import.operator`; sources: None declared; artifacts: None declared.
  - Limit: This declaration is not independently authenticated and does not authorize production execution.
- `evidence.workflow.reconstructed` **system_inferred** — The three receipts represent the semantic sequence plan, status, then report for one synthetic runtime run.
  - Recorded by: `participant.provenance.importer`; sources: `source.ego.plan.receipt`, `source.ego.status.receipt`, `source.ego.receipt`; artifacts: `artifact.ego.plan.receipt`, `artifact.ego.status.receipt`, `artifact.ego.receipt`.
  - Inference basis: Capabilities are experiment.plan, experiment.status, and experiment.report; shared route/runtime fields match.
  - Limit: All receipts have the same timestamp, so chronological order is not independently established.

## Artifacts

- `artifact.ego.learning.package` — `artifacts/learning-package.json` (application/json, 7671 bytes); SHA-256 `51c32666ccfbcae14892d0d40acf4936f96e40ad1fef4feb858ee6b9a7a223a5`; verification: **tool_verified**; role: Synthetic EGO Round 2 output verified against producer manifest
- `artifact.ego.plan.receipt` — `artifacts/plan-receipt.json` (application/json, 1158 bytes); SHA-256 `dfbfd418047400845c2bf8d84d542e434e8e602becf4c7d8ccfcc7e9b546336e`; verification: **tool_verified**; role: Synthetic EGO Round 2 output verified against producer manifest
- `artifact.ego.producer.manifest` — `artifacts/producer-manifest.json` (application/json, 1355 bytes); SHA-256 `7e645b384a687d9906980eee73f5935a1e82e4e3f80be05af0d57adc59e72af2`; verification: **tool_verified**; role: Copied producer manifest; locally hashed but not self-attested by that manifest
- `artifact.ego.receipt` — `artifacts/receipt.json` (application/json, 1452 bytes); SHA-256 `7496f60f64a2ce547d5ebefcf72f97700875297d70b013fc00bf342f355866fd`; verification: **tool_verified**; role: Synthetic EGO Round 2 output verified against producer manifest
- `artifact.ego.status.receipt` — `artifacts/status-receipt.json` (application/json, 1162 bytes); SHA-256 `e4fee4eb78ebf47078cde133226efca9a8a85c5abeb611affbad22eb027e961f`; verification: **tool_verified**; role: Synthetic EGO Round 2 output verified against producer manifest

## Sources

- `source.ego.learning.package` — Imported synthetic output: learning-package.json (tool_output; tool_verified): artifacts/learning-package.json
- `source.ego.plan.receipt` — Imported synthetic output: plan-receipt.json (tool_output; tool_verified): artifacts/plan-receipt.json
- `source.ego.producer.manifest` — Synthetic EGO Round 2 producer manifest (tool_output; observed): artifacts/producer-manifest.json
- `source.ego.receipt` — Imported synthetic output: receipt.json (tool_output; tool_verified): artifacts/receipt.json
- `source.ego.status.receipt` — Imported synthetic output: status-receipt.json (tool_output; tool_verified): artifacts/status-receipt.json
- `source.learning.artifact_digest` — Referenced but unavailable learning evidence: artifact_digest (tool_output; observed): fixture://ego/synthetic-checksum-run-001/digest.txt
- `source.learning.artifact_steps` — Referenced but unavailable learning evidence: artifact_steps (tool_output; observed): fixture://ego/synthetic-checksum-run-001/steps.json

## Record-wide limits

- Integrity checks establish byte equality with the supplied manifest, not authenticity, identity, truth, or authorization.
- The import is synthetic and does not show integration with a live ARIA or Nigma service.
- The learning package is a plan and exercise set; it does not demonstrate completion, comprehension, mastery, or learning.
- Referenced internal evidence payloads are catalogued but absent from the exported bundle, so their hashes are not verified.
- No demuestra que exista una integración de red con Nigma o ARIA.
- No demuestra validez científica ni comportamiento con workloads reales.

## Redactions

- No automatic redactions recorded.

---

This document is generated from the structured record. It reports supplied, observable metadata; it does not expose private reasoning, allocate authorship percentages, or demonstrate learning.
