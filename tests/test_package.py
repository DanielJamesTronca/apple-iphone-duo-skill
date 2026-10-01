"""Package CLI contracts for independently installed skills and plugin catalogs."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageCLI(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name) / "package"
        shutil.copytree(ROOT, self.root,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))

    def validate(self):
        return subprocess.run([sys.executable, str(self.root / "scripts/validate_package.py")],
                              capture_output=True, text=True, check=False)

    def update_json(self, path, update):
        target = self.root / path
        value = json.loads(target.read_text())
        update(value)
        target.write_text(json.dumps(value))

    def test_shipped_package_is_valid(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_portable_and_compatibility_versions_cannot_diverge(self):
        self.update_json("plugin.json", lambda value: value.update(version="9.9.9"))
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("version", result.stderr)

    def test_codex_catalog_must_resolve_the_plugin_and_declare_install_policy(self):
        for fault in ("missing-source", "missing-policy"):
            with self.subTest(fault=fault):
                target = self.root / ".agents/plugins/marketplace.json"
                original = target.read_text()
                value = json.loads(original)
                plugin = value["plugins"][0]
                if fault == "missing-source":
                    plugin["source"]["path"] = "./missing-plugin"
                else:
                    plugin.pop("policy")
                target.write_text(json.dumps(value))
                result = self.validate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("marketplace", result.stderr)
                target.write_text(original)

    def test_skill_references_cannot_depend_on_uninstalled_repository_files(self):
        entry = self.root / "skills/apple-iphone-duo/SKILL.md"
        with entry.open("a") as stream:
            stream.write("\nRead [repository license](../../LICENSE).\n")
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("installed skill", result.stderr)


if __name__ == "__main__":
    unittest.main()
