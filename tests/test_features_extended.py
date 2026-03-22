import unittest
import os
import sys
import tempfile
import shutil
import io
from unittest.mock import patch

# Import the core logic directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from promptops import core, utils  # noqa: E402


class TestFeaturesExtended(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create a regular prompt
        self.create_prompt("normal", "Normal prompt.", ["tag1"], "Hello {{args}}")
        # Create a sensitive prompt
        self.create_prompt(
            "secret",
            "Sensitive prompt.",
            ["security"],
            "Secret: {{args}}",
            sensitive=True,
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_prompt(self, name, description, tags, prompt_content, sensitive=False):
        path = os.path.join(self.test_dir, f"{name}.toml")
        with open(path, "w") as f:
            f.write(f'description = "{description}"\n')
            f.write('version     = "1.0.0"\n')
            f.write('last_updated = "2026-03-21"\n')
            tags_str = str(tags).replace("'", '"')
            f.write(f"tags         = {tags_str}\n")
            if sensitive:
                f.write("sensitive    = true\n")
            f.write(f'prompt      = """\n{prompt_content}\n"""\n')

    @patch("promptops.core.copy_to_clipboard")
    def test_use_prompt_no_copy_flag(self, mock_copy):
        mock_copy.return_value = True
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            # Set no_copy=True
            core.use_prompt(
                "normal", {"args": "data"}, prompts_dir=self.test_dir, no_copy=True
            )
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "Hello data")
            # Should NOT have called copy_to_clipboard
            mock_copy.assert_not_called()

    @patch("promptops.core.copy_to_clipboard")
    @patch("builtins.input", return_value="y")
    def test_sensitive_prompt_warning_confirm(self, mock_input, mock_copy):
        mock_copy.return_value = True
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.stderr", new=io.StringIO()) as fake_err:
                core.use_prompt(
                    "secret", {"args": "my-password"}, prompts_dir=self.test_dir
                )
                output = fake_out.getvalue().strip()
                # Should contain warning and the final prompt
                self.assertIn("SECURITY WARNING", output)
                self.assertTrue(output.endswith("Secret: my-password"))
                mock_copy.assert_called_once()
                self.assertIn("Prompt copied to clipboard", fake_err.getvalue())

    @patch("promptops.core.copy_to_clipboard")
    @patch("builtins.input", return_value="n")
    def test_sensitive_prompt_warning_decline(self, mock_input, mock_copy):
        mock_copy.return_value = True
        with patch("sys.stdout", new=io.StringIO()):
            with patch("sys.stderr", new=io.StringIO()) as fake_err:
                core.use_prompt(
                    "secret", {"args": "my-password"}, prompts_dir=self.test_dir
                )
                # Should NOT have called copy
                mock_copy.assert_not_called()
                self.assertIn("Clipboard copy cancelled", fake_err.getvalue())

    @patch("promptops.core.copy_to_clipboard")
    def test_sensitive_prompt_auto_confirm(self, mock_copy):
        mock_copy.return_value = True
        with patch("sys.stdout", new=io.StringIO()):
            # Pass auto_confirm=True
            core.use_prompt(
                "secret",
                {"args": "my-password"},
                prompts_dir=self.test_dir,
                auto_confirm=True,
            )
            # Should have called copy WITHOUT asking (no input mock needed)
            mock_copy.assert_called_once()

    def test_glob_file_limit(self):
        # Create 110 small files
        glob_dir = tempfile.mkdtemp(dir=self.test_dir)
        for i in range(110):
            with open(os.path.join(glob_dir, f"file_{i:03}.txt"), "w") as f:
                f.write(f"content {i}")

        try:
            pattern = os.path.join(glob_dir, "*.txt")
            val = f"@{pattern}"
            with patch("sys.stderr", new=io.StringIO()) as fake_err:
                result = utils.resolve_file_injection(val)
                # Should contain exactly 100 headers (default MAX_FILES_LIMIT)
                self.assertEqual(result.count("--- File:"), 100)
                self.assertIn("Truncating to first 100 files", fake_err.getvalue())
        finally:
            shutil.rmtree(glob_dir)

    def test_glob_char_limit(self):
        # Create 2 files that together exceed 500k limit
        # Each around 300k
        large_content = "A" * 300000
        f1_path = os.path.join(self.test_dir, "large1.txt")
        f2_path = os.path.join(self.test_dir, "large2.txt")
        with open(f1_path, "w") as f:
            f.write(large_content)
        with open(f2_path, "w") as f:
            f.write(large_content)

        try:
            pattern = os.path.join(self.test_dir, "large*.txt")
            val = f"@{pattern}"
            with patch("sys.stderr", new=io.StringIO()) as fake_err:
                result = utils.resolve_file_injection(val)
                # Total length should be close to 500,000
                self.assertTrue(
                    len(result) <= 500000 + 1000
                )  # small buffer for headers
                self.assertIn("Maximum character limit reached", fake_err.getvalue())
                self.assertIn("TRUNCATED", result)
        finally:
            os.remove(f1_path)
            os.remove(f2_path)

    def test_glob_char_limit_single_huge_file(self):
        huge_content = "A" * 600000
        f_path = os.path.join(self.test_dir, "huge.txt")
        with open(f_path, "w") as f:
            f.write(huge_content)

        try:
            val = f"@{f_path}"
            with patch("sys.stderr", new=io.StringIO()) as fake_err:
                result = utils.resolve_file_injection(val)
                self.assertTrue(len(result) <= 500000 + 1000)
                self.assertIn("Maximum character limit reached", fake_err.getvalue())
                self.assertIn("TRUNCATED", result)
        finally:
            os.remove(f_path)


if __name__ == "__main__":
    unittest.main()
