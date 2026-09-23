import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SPEC = importlib.util.spec_from_file_location("ego_round2_importer", ROOT / "src" / "ego_round2_importer.py")
importer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(importer)
REQUEST = ROOT / "examples" / "ego_round2_import" / "import-request.json"


class EgoRound2ImporterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configured = os.environ.get("EGO_ROUND2_FIXTURE_DIR")
        if not configured:
            raise unittest.SkipTest("EGO_ROUND2_FIXTURE_DIR is not set")
        cls.source_fixture = Path(configured)
        if not cls.source_fixture.is_dir():
            raise unittest.SkipTest("configured EGO Round 2 fixture directory is unavailable")

    def copy_fixture(self, root: Path) -> Path:
        source = root / "source"
        shutil.copytree(self.source_fixture, source)
        return source

    def test_import_integrity_classifications_and_reconstruction(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.copy_fixture(root)
            output = root / "public-package"
            record = importer.import_bundle(source, output, REQUEST)
            self.assertEqual(importer.validate_record(record), [])
            self.assertEqual(
                {item["classification"] for item in record["evidence"]},
                {"observed", "user_declared", "tool_verified", "system_inferred"},
            )
            reconstruction = next(item for item in record["evidence"] if item["id"] == "evidence.workflow.reconstructed")
            self.assertEqual(reconstruction["classification"], "system_inferred")
            self.assertIn("same timestamp", " ".join(reconstruction["limits"]))
            serialized = (output / "provenance.json").read_text(encoding="utf-8")
            self.assertNotIn(str(self.source_fixture), serialized)
            self.assertNotIn("/home/", serialized)
            self.assertTrue((output / "PROVENANCE.md").is_file())

    def test_tampered_output_is_rejected_without_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.copy_fixture(root)
            target = source / "receipt.json"
            target.write_bytes(target.read_bytes() + b"\n")
            output = root / "public-package"
            with self.assertRaisesRegex(importer.ImportError, "integrity mismatch"):
                importer.import_bundle(source, output, REQUEST)
            self.assertFalse(output.exists())

    def test_missing_learning_evidence_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.copy_fixture(root)
            learning_path = source / "learning-package.json"
            learning = json.loads(learning_path.read_text(encoding="utf-8"))
            learning["evidence_summary"]["observations"][0]["evidence_ref_ids"] = ["missing_artifact"]
            learning_bytes = (json.dumps(learning, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            learning_path.write_bytes(learning_bytes)
            digest = importer.hashlib.sha256(learning_bytes).hexdigest()
            manifest_path = source / "producer-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["outputs"]["learning-package.json"] = {"sha256": digest, "size_bytes": len(learning_bytes)}
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            output = root / "public-package"
            with self.assertRaisesRegex(importer.ImportError, "unresolved learning evidence references"):
                importer.import_bundle(source, output, REQUEST)
            self.assertFalse(output.exists())

    def test_learning_plan_is_not_reported_as_learning(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.copy_fixture(root)
            output = root / "public-package"
            record = importer.import_bundle(source, output, REQUEST)
            boundary = next(item for item in record["evidence"] if item["id"] == "evidence.learning.package.boundary")
            self.assertEqual(boundary["classification"], "observed")
            self.assertIn("does not show", " ".join(boundary["limits"]))
            self.assertNotIn("learning_score", json.dumps(record))
            self.assertEqual(record["decisions"], [])

    def test_import_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.copy_fixture(root)
            first, second = root / "first", root / "second"
            importer.import_bundle(source, first, REQUEST)
            importer.import_bundle(source, second, REQUEST)
            self.assertEqual((first / "provenance.json").read_bytes(), (second / "provenance.json").read_bytes())
            self.assertEqual((first / "PROVENANCE.md").read_bytes(), (second / "PROVENANCE.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
