# PROVENANCE

Public working draft 0.1.0 for recording observable decisions and evidence in human–AI collaboration. This is a proposal for review, not an adopted standard. The format is independent of ARIA and any particular AI provider.

The record has two views: structured `provenance.json` and generated `PROVENANCE.md`. It links decisions to alternatives, declared participants, sources, artifacts, hashes, evidence classes, and limits. The four classes are `observed`, `user_declared`, `tool_verified`, and `system_inferred`.

In research, this can make a change of method or interpretation easier for a collaborator to reconstruct from cited evidence. In an exam or thesis defense, it can give an examiner concrete choices to discuss with a student when AI assistance is permitted. These are proposed uses, not measured benefits; the record does not establish authorship or understanding. See [why and how to pilot it](docs/why-adopt.md).

## Start here

- [Proposal and maturity](docs/proposal.md)
- [Why try it in research or academic assessment?](docs/why-adopt.md)
- [Por qué probarlo en investigación o evaluación académica](docs/por-que-adoptarlo.md)
- [Format specification](docs/specification.md)
- [JSON Schema](schema/provenance.schema.json)
- [Conformance rules](docs/conformance.md)
- [Synthetic decision example](examples/synthetic_collaboration/PROVENANCE.md)
- [Prior art](docs/prior-art.md)
- [Evaluation protocol](docs/evaluation-protocol.md)

The `src/` programs are a Python 3.10+ reference implementation using the standard library. The [EGO Round 2 importer](docs/ego-round2-import.md) is an experimental adapter; it is not a prerequisite for using the format.

## Try the reference implementation

```bash
python3 -m unittest discover -s tests -v
python3 src/provenance_tool.py validate examples/synthetic_collaboration/provenance.json
python3 src/provenance_tool.py build \
  examples/synthetic_collaboration/provenance.input.json \
  --base-dir examples/synthetic_collaboration \
  --json-out /tmp/provenance-example.json \
  --markdown-out /tmp/PROVENANCE-example.md
```

Hashes verify byte equality against a supplied value. They do not authenticate people, establish the truth of a statement, or prove that someone learned. The format does not record private reasoning or calculate authorship percentages.

## Maturity and participation

Draft 0.1.0 can change. Producers and consumers should pin the `schema_version` they support. [Contributing](CONTRIBUTING.md) explains how to propose changes; [security and privacy notes](SECURITY.md) describe current limits. The project is licensed under [Apache 2.0](LICENSE).
