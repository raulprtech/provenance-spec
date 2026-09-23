# PROVENANCE

An experimental proposal for automatically documenting AI assistance, human decisions, and delegation while preparing a scientific article. **Transparent AI use, built on trust—not detection to punish its use.**

This is a proposal for review, not an adopted standard, an AI detector, or an authorship assessment.

## Scientific articles first

The intended workflow captures interventions from integrated tools and lets a model organize them into an author-reviewable record: literature discovery, ideation, methodology, code, analysis, interpretation, drafting, translation, editing, visualization, and reviewer responses.

Each intervention should connect to an article element and version, available evidence, and explicitly recorded human acceptance, modification, rejection, or delegation. We seek to document **all captured interventions within a declared scope**, not every possible way AI helped. External work remains unknown.

## Trust, not judgment for using AI

Researchers should be able to share decisions and delegations without the mere use of AI becoming a reason to judge or punish them. We favor trust in a documented process over attempts to detect AI use for punishment.

This is a design commitment, not a demonstrated effect. Scientific claims remain open to criticism, and the project cannot override journal policies or guarantee how others use a disclosure. Capture should be consented and bounded; sharing requires author review. Missing records mean unknown coverage, not misconduct. No AI-use score or authorship percentage belongs in this project.

Read the [trust charter](docs/trust-and-transparency.md) and [Spanish guide](docs/por-que-adoptarlo.md).

## Available versus planned

| Available now | Proposed, not implemented |
|---|---|
| Draft 0.1.0 schema, partial offline validator, deterministic Markdown generator | Tool-connected automatic capture and model-assisted organization |
| Evidence, artifact, and decision records | Structured interventions, delegation, coverage, corrections, and approval workflow |
| Synthetic examples and experimental EGO importer | Article-editor integration and author-approved AI-use disclosure generator |

The current record has structured `provenance.json` and generated `PROVENANCE.md` views. It distinguishes `observed`, `user_declared`, `tool_verified`, and `system_inferred`. Hash checks establish byte equality, not identity, chronology, truth, authorship, or learning.

The [article profile](docs/scientific-article-profile.md) defines the target and remaining work. The wire format stays at `0.1.0`; this documentation revision does not release a schema or claim automatic capture works. Exams and ARIA are a later, separately evaluated application, outside the initial scope.

## Start here

- [Proposal and maturity](docs/proposal.md)
- [Scientific-article profile and roadmap](docs/scientific-article-profile.md)
- [Trust and non-punitive transparency](docs/trust-and-transparency.md)
- [Why pilot it for scientific articles?](docs/why-adopt.md)
- [Transparencia y confianza en artículos científicos](docs/por-que-adoptarlo.md)
- [Research papers and their limits](docs/evidence-base.md)
- [Existing format specification](docs/specification.md)
- [JSON Schema](schema/provenance.schema.json)
- [Conformance and known gaps](docs/conformance.md)
- [Synthetic decision example](examples/synthetic_collaboration/PROVENANCE.md)
- [Prior art](docs/prior-art.md)
- [Evaluation protocol](docs/evaluation-protocol.md)

The Python 3.10+ tools use the standard library. The [EGO importer](docs/ego-round2-import.md) is a historical synthetic adapter, not an article integration or a prerequisite.

## Try the existing reference implementation

```bash
EGO_ROUND2_FIXTURE_DIR=examples/ego_round2_import/public-package/artifacts \
  python3 -m unittest discover -s tests -v
python3 src/provenance_tool.py validate examples/synthetic_collaboration/provenance.json
python3 src/provenance_tool.py build \
  examples/synthetic_collaboration/provenance.input.json \
  --base-dir examples/synthetic_collaboration \
  --json-out /tmp/provenance-example.json \
  --markdown-out /tmp/PROVENANCE-example.md
```

The CLI is a partial validator. It does not independently recheck artifact bytes in its `validate` command, and copied importer attachments are not sanitized. Review all inputs and outputs before sharing; do not use confidential material in the pilot.

## Maturity and participation

Draft 0.1.0 can change. Consumers should pin supported versions. See [contributing](CONTRIBUTING.md), [security and privacy](SECURITY.md), and [Apache 2.0 license](LICENSE). No independent effectiveness study or organizational endorsement is claimed.
