# Scientific-article profile: design target

Status: proposed scope, **not an implemented capture system or a new schema release**. The existing 0.1.0 format is a baseline. Exams and ARIA are deferred.

## Unit of documentation

An intervention is an identifiable assistance event with a task and available evidence. A delegation is an explicitly recorded assignment of a task or bounded authority to a tool; it does not imply acceptance of the result. A human decision is an explicit declaration or captured human action with a narrow, supportable meaning. Model reconstruction is neither of these.

Assistance categories include literature discovery, ideas, methods, code, analysis, interpretation, drafting, translation, editing, visualization, and reviewer response. Allow multiple categories and a described other category. Model classifications remain labeled inferences and are correctable.

## Information needed in the future profile

| Information | Boundary |
|---|---|
| Intervention ID, known event time, capture time, recorder | Do not invent precise event times from retrospective summaries. |
| Article element and version: paragraph, figure, table, code, reference | Externally produced work may be outside coverage. |
| Requested task, proposed contribution, permitted evidence references | Full prompts and transcripts are not required. |
| Declared tool/model identifier and version when available | A supplied name is not authenticated identity; unknown is allowed. |
| Explicit human delegation and its limits | Automatic changes within a delegation are not per-change human approval. |
| Accepted, modified, rejected, pending, or unknown outcome | Separate declaration, captured action, and model interpretation. |
| Optional stated reason, actor, and decision evidence | Never infer private intention or comprehension. |
| Capture window, connected tools, exclusions, failures | Completeness is relative to a bounded capture scope. |
| Corrections, revisions, superseded interventions | Do not retain sensitive removed content just to preserve history. |
| Review and sharing state | A generated draft is not an author-approved disclosure. |

These are design requirements, not fields to insert into the strict 0.1.0 schema. A future version needs a schema, fixtures, migration rules, and conformance tests. Separate origin, observation method, and verification scope rather than silently reinterpreting the four existing classes.

## Intended workflow

1. Author agrees to capture scope, storage, recipients, retention, and exclusions; collection can be paused.
2. Connected tools capture minimal events and permitted evidence. Expose failures and unavailable context without suspicion labels.
3. A model groups and summarizes events with references to their IDs, marks interpretations, and abstains where evidence is absent. Source content is data, not instructions to alter logging, trust labels, or publication permissions.
4. The author corrects attributions and confirms only decisions actually made. Preserve pending and unknown states.
5. Produce a detailed working record and a separate concise AI-use disclosure. The author selects permitted material and explicitly approves sharing; neither output is automatically published.

The disclosure describes assistance types, affected work, human decisions and review, and coverage limits. It does not assign contribution percentages, imply all claims were independently checked, or certify journal-policy compliance. Authors review destination-specific requirements separately.

## Synthetic example, not an implemented event format

An author asks for clearer wording for a paragraph in Discussion version 3. The tool captures a suggestion and the author applying a modified version. The record may state “AI suggested wording; the author applied an edited version,” linking the permitted difference. It cannot say “the author verified every claim” or explain their motive unless explicitly recorded. An externally edited figure remains outside coverage.

## Baseline and blockers

The current model can illustrate parts of this scenario, but lacks first-class interventions, delegation bounds, coverage, unknown decision times, revision links, and approval states. The EGO fixture is a historical adapter test, not an article workflow or evidence of learning.

Before handling confidential material, address partial validation, malformed-reference crashes, and unscanned copied importer attachments. A clean record does not imply clean attachments. Test summaries against unsupported attribution, omissions, conflicting accounts, and instructions embedded in evidence.

## Roadmap and gates

1. **Contract:** compare with a simple disclosure table and a documented PROV/RO-Crate profile; justify fields and propose a versioned migration.
2. **Safety and conformance:** align schema and CLI checks, add negative tests, inspect attachments, and specify access, retention, correction, and sharing controls.
3. **End-to-end prototype:** build one bounded article-editing adapter, model-assisted summarization, and reviewed disclosure. Cover accept, modify, reject, delegate, unknown, and correction cases.
4. **Research pilot:** execute the evaluation protocol with independent annotation and equivalent information across conditions; no efficacy claims before results.
5. **Later application:** consider ARIA/exams under a separate educational profile and study. Article documentation does not establish learning or misconduct.
