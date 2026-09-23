# Why try PROVENANCE in research or academic assessment?

PROVENANCE is a **working draft**, not an adopted standard. Its value proposition is a testable one: a compact record of decisions, alternatives, evidence, and limits may help someone who was not present reconstruct what happened without reading a private AI conversation. That benefit has not yet been demonstrated in an independent study. The [evaluation protocol](evaluation-protocol.md) describes how to test it.

## Research: make consequential choices reviewable

A research project changes direction for many reasons: a cohort is excluded, an endpoint is redefined, an analysis is deferred, or a result is judged too uncertain to claim. A PROVENANCE record can link a decision to the evidence available at that time, the alternatives considered, the people declared to be involved, and the remaining uncertainty. A machine-readable record can be checked for missing references; the generated Markdown can be read by a collaborator, supervisor, or reviewer.

For example, a team might record that it deferred a model comparison because one input was not available at the required time. The record can point to a versioned protocol and a verification artifact. It should label the team's explanation as `user_declared`, a file hash as `tool_verified`, and any later interpretation as `system_inferred`. The reviewer can then see which part is a declaration, which bytes were checked, and which conclusion still needs scrutiny.

Potential uses include lab handoffs, preregistered analysis changes, artifact review, reproducibility packages, and responses to reviewer questions. The record supplements a protocol, lab notebook, repository history, and domain-specific provenance such as W3C PROV or RO-Crate. It does not certify that the study was valid or that the record is complete.

## Examinations: discuss a student's documented choices

In an exam, thesis defense, or assessed project where AI assistance is permitted, a student could submit a small record describing decisions they are willing to disclose: which alternative they selected, which sources or artifacts support it, what help they declare using, and what remains uncertain. An examiner could use that record to ask focused questions such as “Why did you reject the other method?” or “What does this hash establish?” The student's answer and the work itself remain the basis for judging understanding under the institution's published rules.

For example, a student may declare that an AI tool suggested two solution paths, then record their own selection and the test output they inspected. The record can preserve that distinction. It cannot establish who wrote each line, whether the student understood the method, or whether undisclosed assistance occurred. Those questions require the normal assessment design, such as supervised work or an oral explanation, if the institution considers them relevant.

Adoption in an assessment should be optional or explicitly covered by course policy, announced before the work begins, and accessible to students using different tools or no AI. Require only information needed for the learning objective. Do not demand private chats, hidden reasoning, credentials, or third-party data. Provide a way to correct a mistaken record and to describe evidence that cannot be shared for privacy or intellectual-property reasons.

## What an adopter can check today

- Whether a record has required fields and resolvable local references.
- Whether an inference names its basis and at least one limit.
- Whether packaged artifact bytes match their recorded SHA-256 and size.
- Whether the same input and artifact bytes generate the same human-readable output.

These checks concern the *record*. They do not authenticate a participant, prove that a statement is true, detect cheating, determine authorship, or measure learning. The current reference implementation has [known conformance gaps](conformance.md) and its secret redaction is incomplete.

## A responsible pilot

1. Choose a low-stakes, synthetic or consented scenario and pin the exact draft version.
2. Compare the record with an existing note or template on the same task.
3. Ask an independent reader to reconstruct decisions, evidence, and limits; measure errors and time spent documenting.
4. Review privacy and accessibility before retaining or sharing records.
5. Publish results, including failures and workload, before making claims that the format improves research review or assessment.

The reason to try the draft is that it makes those questions concrete and measurable. The reason to adopt it as a requirement must come from a successful evaluation in the intended setting.
