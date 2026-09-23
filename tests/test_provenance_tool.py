import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("provenance_tool", ROOT / "src" / "provenance_tool.py")
tool = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(tool)


class ProvenanceToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_dir = ROOT / "examples" / "synthetic_collaboration"
        cls.raw = json.loads((cls.example_dir / "provenance.input.json").read_text(encoding="utf-8"))

    def build(self, raw=None):
        return tool.build_record(copy.deepcopy(raw if raw is not None else self.raw), self.example_dir)

    def test_example_builds_and_is_deterministic(self):
        first_record, first_markdown = self.build()
        second_record, second_markdown = self.build()
        self.assertEqual(first_record, second_record)
        self.assertEqual(first_markdown, second_markdown)
        self.assertEqual(tool.validate_record(first_record), [])

    def test_invalid_classification_is_rejected(self):
        record, _ = self.build()
        record["evidence"][0]["classification"] = "probably_observed"
        errors = tool.validate_record(record)
        self.assertTrue(any("invalid classification" in error for error in errors))

    def test_missing_reference_is_rejected(self):
        record, _ = self.build()
        record["decisions"][0]["evidence_refs"] = ["evidence.does.not.exist"]
        errors = tool.validate_record(record)
        self.assertTrue(any("unresolved reference" in error for error in errors))

    def test_system_inference_requires_basis_and_limit(self):
        record, _ = self.build()
        inferred = next(item for item in record["evidence"] if item["classification"] == "system_inferred")
        inferred.pop("inference_basis")
        inferred["limits"] = []
        errors = tool.validate_record(record)
        self.assertTrue(any("inference_basis" in error for error in errors))
        self.assertTrue(any("requires at least one limit" in error for error in errors))

    def test_secret_is_redacted_from_json_and_markdown(self):
        raw = copy.deepcopy(self.raw)
        raw["sources"][0]["notes"] = "temporary token " + "sk-" + "proj-abcdefghijklmnop123456"
        record, markdown = self.build(raw)
        serialized = json.dumps(record)
        self.assertNotIn("abcdefghijklmnop123456", serialized)
        self.assertNotIn("abcdefghijklmnop123456", markdown)
        self.assertIn("[REDACTED]", record["sources"][0]["notes"])
        self.assertTrue(any(item["reason"] == "potential_secret" for item in record["redactions"]))

    def test_sensitive_key_value_is_redacted(self):
        raw = copy.deepcopy(self.raw)
        raw["sources"][0]["api_key"] = "plain-text-value"
        sanitized, redactions = tool.redact_secrets(raw)
        self.assertEqual(sanitized["sources"][0]["api_key"], "[REDACTED]")
        self.assertEqual(len(redactions), 1)

    def test_forbidden_authorship_score_is_rejected(self):
        record, _ = self.build()
        record["authorship_score"] = 0.5
        errors = tool.validate_record(record)
        self.assertTrue(any("forbidden field" in error for error in errors))

    def test_artifact_path_escape_is_rejected_before_read(self):
        raw = copy.deepcopy(self.raw)
        raw["artifacts"][0]["path"] = "../private.txt"
        with self.assertRaises(tool.ProvenanceError):
            self.build(raw)


if __name__ == "__main__":
    unittest.main()

