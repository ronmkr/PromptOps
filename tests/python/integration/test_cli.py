import io
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add scripts to path
base_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.append(os.path.join(base_dir, "scripts"))

from promptbook import core  # noqa: E402


class TestCLI(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for prompts
        self.test_dir = tempfile.mkdtemp()

        # Create some sample prompts
        self.create_prompt(
            "alpha-prompt",
            "Description one.",
            ["tag1", "common"],
            "# Title One\n{{args}}",
        )
        self.create_prompt(
            "beta-tool",
            "Description two.",
            ["tag2", "common"],
            "# Title Two\n{{args}} and {{code}}",
        )
        self.create_prompt("gamma-helper", "Other desc.", ["tag3"], "# Title Three\nNo vars.")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_prompt(self, name, description, tags, prompt_content):
        path = os.path.join(self.test_dir, f"{name}.toml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'description = "{description}"\n')
            f.write('version     = "1.0.0"\n')
            f.write('last_updated = "2026-03-21"\n')
            tags_str = str(tags).replace("'", '"')
            f.write(f"tags         = {tags_str}\n\n")
            f.write(f'prompt      = """\n{prompt_content}\n"""\n')

    def test_get_prompts(self):
        prompts = core.get_prompts(self.test_dir)
        self.assertEqual(len(prompts), 3)
        names = sorted([p["name"] for p in prompts])
        self.assertEqual(names, ["alpha-prompt", "beta-tool", "gamma-helper"])

    def test_list_prompts_no_filter(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.list_prompts(prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)
            self.assertIn("beta-tool", output)
            self.assertIn("gamma-helper", output)

    def test_list_prompts_with_filter(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.list_prompts(tag_filter="tag1", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)
            self.assertNotIn("beta-tool", output)

    def test_list_tags(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.list_tags(prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("tag1", output)
            self.assertIn("common", output)
            self.assertIn("(2 prompts)", output)

    def test_search_prompts_direct(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.search_prompts("alpha", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)
            self.assertNotIn("gamma-helper", output)

    def test_use_prompt_with_flags(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.use_prompt("alpha-prompt", {"args": "hello world"}, prompts_dir=self.test_dir)
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "# Title One\nhello world")

    @patch("sys.stdin", io.StringIO("multi-line\ninput\n"))
    def test_use_prompt_interactive(self):
        with patch("sys.stderr", new=io.StringIO()):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                core.use_prompt("alpha-prompt", prompts_dir=self.test_dir)
                output = fake_out.getvalue().strip()
                self.assertEqual(output, "# Title One\nmulti-line\ninput")

    def test_use_prompt_not_found(self):
        with patch("sys.stderr", new=io.StringIO()) as fake_err:
            with self.assertRaises(SystemExit):
                core.use_prompt("non-existent", prompts_dir=self.test_dir)
            self.assertIn("not found", fake_err.getvalue())

    def test_get_prompts_empty_dir(self):
        empty_dir = tempfile.mkdtemp()
        prompts = core.get_prompts(empty_dir)
        self.assertEqual(len(prompts), 0)
        shutil.rmtree(empty_dir)

    def test_use_prompt_multiple_variables(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.use_prompt(
                "beta-tool", {"args": "val1", "code": "val2"}, prompts_dir=self.test_dir
            )
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "# Title Two\nval1 and val2")

    @patch("sys.stdin", io.StringIO("interactive_val\n"))
    def test_use_prompt_partial_flags(self):
        # Pass 'args' via flag, but let 'code' be interactive
        with patch("sys.stderr", new=io.StringIO()):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                core.use_prompt("beta-tool", {"args": "flag_val"}, prompts_dir=self.test_dir)
                output = fake_out.getvalue().strip()
                self.assertEqual(output, "# Title Two\nflag_val and interactive_val")

    def test_search_prompts_no_matches(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.search_prompts("non-existent-search-term", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("No prompts found", output)

    def test_list_tags_raw(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.list_tags(prompts_dir=self.test_dir, raw=True)
            output = fake_out.getvalue()
            # Raw output should be one tag per line, sorted
            self.assertEqual(output, "common\ntag1\ntag2\ntag3\n")

    def test_get_prompts_non_existent_dir(self):
        prompts = core.get_prompts("/non/existent/path")
        self.assertEqual(len(prompts), 0)


if __name__ == "__main__":
    unittest.main()
