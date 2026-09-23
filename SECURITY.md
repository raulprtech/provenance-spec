# Security and privacy

Automatic capture and author-controlled sharing are proposed, not implemented. See the [trust charter](docs/trust-and-transparency.md) before planning a pilot. Do not promise a safe or non-punitive environment unless actual access and use policies support it.

The importer copies original artifact bytes without scanning or redacting every field. A clean generated record does not imply clean attachments. Review the entire package, not just its Markdown view. Current pilots should use synthetic, non-confidential material.

The reference implementation reads user supplied JSON and local artifact paths. Do not run it on confidential material without reviewing the input and output. Its secret redaction is heuristic and incomplete.

The format does not authenticate participants or sign records. File hashes can detect byte changes against an independently trusted value, but a manifest and its files can be altered together. The EGO importer uses relative output paths and copies only declared synthetic files; consumers must still review those files before sharing.

Please report suspected credential exposure or a vulnerability privately through GitHub's repository security reporting when available. If that is unavailable, contact the repository owner privately through their established channel. Do not post exploit details or secrets in a public issue.
