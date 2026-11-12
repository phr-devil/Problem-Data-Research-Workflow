"""Executable, side-effect-free tests for local declared delivery paths."""
import tempfile
import unittest
from pathlib import Path

from core.delivery_check import check_delivery


class DeliveryPathTests(unittest.TestCase):
    def test_existing_primary_and_secondary_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "final").mkdir()
            (root / "final" / "result.csv").write_text("value\\n1\\n", encoding="utf-8")
            (root / "final" / "README.md").write_text("main", encoding="utf-8")
            got = check_delivery(root, "final/README.md", ["final/result.csv"])
            self.assertEqual(got["result"], "PASS_PATHS_ONLY")
            self.assertEqual(got["verification"], "PATHS_ONLY_NOT_SCIENCE_OR_AUTH")
            self.assertEqual(len(got["checked_paths"]), 2)

    def test_missing_primary_fails_instead_of_claiming_delivery(self):
        with tempfile.TemporaryDirectory() as d:
            got = check_delivery(Path(d), "not_created.zip")
            self.assertEqual(got["result"], "FAIL")
            self.assertTrue(any("PRIMARY_MISSING" in e for e in got["errors"]))

    def test_missing_extra_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "main.txt").write_text("done", encoding="utf-8")
            got = check_delivery(root, "main.txt", ["missing.json"])
            self.assertEqual(got["result"], "FAIL")
            self.assertTrue(any("FILE_MISSING" in e for e in got["errors"]))

    def test_absolute_and_parent_escape_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "main.txt").write_text("done", encoding="utf-8")
            self.assertEqual(check_delivery(root, "/etc/passwd")["result"], "FAIL")
            self.assertEqual(check_delivery(root, "../outside.txt")["result"], "FAIL")

    def test_symlink_outside_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root.parent / (root.name + "-outside.txt")
            target.write_text("not part of delivery", encoding="utf-8")
            try:
                link = root / "external.txt"
                try:
                    link.symlink_to(target)
                except (OSError, NotImplementedError):
                    self.skipTest("symlinks unavailable")
                got = check_delivery(root, "external.txt")
                self.assertEqual(got["result"], "FAIL")
                self.assertTrue(any("OUTSIDE_DELIVERY_ROOT" in e for e in got["errors"]))
            finally:
                target.unlink(missing_ok=True)

    def test_read_only_or_empty_task_is_not_falsely_certified(self):
        with tempfile.TemporaryDirectory() as d:
            got = check_delivery(Path(d), "")
            self.assertEqual(got["result"], "FAIL")
            self.assertTrue(any("PRIMARY_PATH_EMPTY" in e for e in got["errors"]))


if __name__ == "__main__":
    unittest.main()
