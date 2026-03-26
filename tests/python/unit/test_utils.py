import os
import sys
import tempfile
import unittest

# Add scripts to path
base_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.append(os.path.join(base_dir, "scripts"))

from promptbook import utils  # noqa: E402


class TestUtils(unittest.TestCase):
    def test_resolve_file_injection_valid(self):
        # Create a temp file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("FILE_CONTENT")
            temp_path = f.name

        try:
            val = f"@{temp_path}"
            result = utils.resolve_file_injection(val)
            self.assertEqual(result, "FILE_CONTENT")
        finally:
            os.remove(temp_path)

    def test_resolve_file_injection_no_prefix(self):
        val = "JUST_STRING"
        result = utils.resolve_file_injection(val)
        self.assertEqual(result, "JUST_STRING")

    def test_resolve_file_injection_glob(self):
        # Create two temp files
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f1:
            f1.write("C1")
            p1 = f1.name
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f2:
            f2.write("C2")
            p2 = f2.name

        try:
            # Match both using a glob
            common_pattern = os.path.join(os.path.dirname(p1), "tmp*.txt")
            val = f"@{common_pattern}"
            result = utils.resolve_file_injection(val)

            # Should contain headers and contents
            self.assertIn("--- File:", result)
            self.assertIn("C1", result)
            self.assertIn("C2", result)
        finally:
            os.remove(p1)
            os.remove(p2)


if __name__ == "__main__":
    unittest.main()
