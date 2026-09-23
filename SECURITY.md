# Security and privacy

The reference implementation reads user supplied JSON and local artifact paths. Do not run it on confidential material without reviewing the input and output. Its secret redaction is heuristic and incomplete.

The format does not authenticate participants or sign records. File hashes can detect byte changes against an independently trusted value, but a manifest and its files can be altered together. The EGO importer uses relative output paths and copies only declared synthetic files; consumers must still review those files before sharing.

Please report suspected credential exposure or a vulnerability privately through GitHub's repository security reporting when available. If that is unavailable, contact the repository owner privately through their established channel. Do not post exploit details or secrets in a public issue.
