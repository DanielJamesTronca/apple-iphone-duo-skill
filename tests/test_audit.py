"""CLI boundary tests: findings are candidates, preserve location, never mutate input."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/apple-iphone-duo/scripts/audit_resizability.py"


class AuditCLI(unittest.TestCase):
    def run_audit(self, root, *options):
        return subprocess.run([sys.executable, str(SCRIPT), str(root), *options],
                              capture_output=True, text=True, check=False)

    def test_mixed_project_locations_and_read_only_behavior(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "View.swift").write_text("let size = UIScreen\n  .main.bounds\nlet inset = view.safeAreaInsets.right\n")
            (root / "Legacy.m").write_text("CGRect rect = [UIScreen mainScreen].bounds;\n")
            (root / "App.plist").write_text("<key>UIRequiresFullScreen</key><true/>\n")
            before = {p.name: hashlib.sha256(p.read_bytes()).digest() for p in root.iterdir()}
            result = self.run_audit(root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["files_scanned"], 3)
            locations = {(v["rule"], v["path"], v["line"]) for v in report["candidates"]}
            self.assertEqual(locations, {("main-screen", "View.swift", 1),
                                         ("edge-inset", "View.swift", 3),
                                         ("main-screen", "Legacy.m", 1),
                                         ("full-screen-policy", "App.plist", 1)})
            self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).digest() for p in root.iterdir()})

    def test_comment_and_string_examples_do_not_become_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Demo.swift").write_text('''// UIScreen.main.bounds
/* outer /* UIDevice.current.orientation */ safeAreaInsets.left */
let text = "UIScreen.main.bounds"
let note = """UIRequiresFullScreen
connectedScenes.first"""
let idiom = traitCollection.userInterfaceIdiom
''')
            report = json.loads(self.run_audit(root, "--json").stdout)
            self.assertEqual([(v["rule"], v["line"]) for v in report["candidates"]],
                             [("idiom-assumption", 6)])

    def test_generated_dependencies_and_symlinks_are_not_scanned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Actual.swift").write_text("let x = UIScreen.main.bounds\n")
            for name in ["Pods", "DerivedData", ".build"]:
                (root / name).mkdir()
                (root / name / "Generated.swift").write_text("let x = UIScreen.main.bounds\n")
            (root / "link.swift").symlink_to(root / "Actual.swift")
            (root / "loop").symlink_to(root, target_is_directory=True)
            result = self.run_audit(root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["files_scanned"], 1)
            self.assertEqual(len(report["candidates"]), 1)

    def test_single_file_and_human_output_do_not_fail_for_candidates(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "View.swift"
            source.write_text("let x = UIScreen.main.bounds\n")
            result = self.run_audit(source)
            self.assertEqual(result.returncode, 0)
            self.assertIn("View.swift:1:", result.stdout)
            self.assertIn("not proven bugs", result.stdout)

    def test_invalid_or_unreadable_inputs_are_not_reported_as_clean(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing = self.run_audit(root / "missing")
            self.assertEqual(missing.returncode, 2)
            self.assertIn("does not exist", missing.stderr)
            (root / "Broken.swift").write_bytes(b"\xff\xfe")
            result = self.run_audit(root, "--json")
            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertTrue(report["warnings"])
            self.assertEqual(report["files_scanned"], 0)


if __name__ == "__main__":
    unittest.main()
