# Agent instructions

This repository is a public draft specification and a reference implementation. Read `README.md`, `docs/specification.md`, and `docs/conformance.md` before changing the format.

- Prioritize scientific articles, captured AI assistance, explicit human decisions, and bounded delegation. Follow `docs/scientific-article-profile.md` and `docs/trust-and-transparency.md`; exams and ARIA are deferred.
- Do not describe planned automatic capture, model summaries, or approval controls as implemented. Never equate missing records with misconduct or add AI-use suspicion scores.
- Treat the JSON Schema and the normative rules in `docs/specification.md` as the format proposal. Changes to either require an entry in `CHANGELOG.md` and updated conformance examples.
- Preserve the distinction among `observed`, `user_declared`, `tool_verified`, and `system_inferred`. A hash check verifies bytes against a supplied value; it does not authenticate an actor or establish truth.
- Do not add private conversations, hidden reasoning, credentials, patient data, personal filesystem paths, or unlicensed materials to examples or test fixtures.
- Keep examples synthetic and inspect every generated artifact before publishing.
- Run `python3 -m unittest discover -s tests -v` and validate the example JSON before proposing a release. A passing test suite does not by itself make the proposal a standard.
- Treat integrations, including ARIA and EGO, as adapters. They must declare the exact schema version they consume and handle unsupported versions explicitly.
- Do not publish a new version, change repository visibility, or claim organizational endorsement without maintainer review.
