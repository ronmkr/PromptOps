import unittest
import os
import sys
import tempfile
import shutil
import io
from unittest.mock import patch, MagicMock

# Import the core logic directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import promptops_core

class TestPromptOps(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for prompts
        self.test_dir = tempfile.mkdtemp()
        
        # Create some sample prompts
        self.create_prompt("alpha-prompt", "Description one.", ["tag1", "common"], "# Title One\n{{args}}")
        self.create_prompt("beta-tool", "Description two.", ["tag2", "common"], "# Title Two\n{{args}} and {{code}}")
        self.create_prompt("gamma-helper", "Other desc.", ["tag3"], "# Title Three\nNo vars.")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_prompt(self, name, description, tags, prompt_content):
        path = os.path.join(self.test_dir, f"{name}.toml")
        with open(path, "w") as f:
            f.write(f'description = "{description}"\n')
            f.write(f'version     = "1.0.0"\n')
            f.write(f'last_updated = "2026-03-21"\n')
            f.write(f'tags         = {str(tags).replace("\'", "\"")}\n\n')
            f.write(f'prompt      = """\n{prompt_content}\n"""\n')

    def test_get_prompts(self):
        prompts = promptops_core.get_prompts(self.test_dir)
        self.assertEqual(len(prompts), 3)
        self.assertEqual(prompts[0]["name"], "alpha-prompt")

    def test_list_prompts_no_filter(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.list_prompts(prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)
            self.assertIn("beta-tool", output)
            self.assertIn("gamma-helper", output)

    def test_list_prompts_with_filter(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.list_prompts(tag_filter="tag1", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)
            self.assertNotIn("beta-tool", output)

    def test_list_tags(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.list_tags(prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("tag1", output)
            self.assertIn("common", output)
            self.assertIn("(2 prompts)", output)

    def test_search_prompts_direct(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.search_prompts("alpha", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)
            self.assertNotIn("gamma-helper", output)

    def test_search_prompts_fuzzy(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            # "alph" should match "alpha-prompt"
            promptops_core.search_prompts("alph", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)

    def test_use_prompt_with_flags(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.use_prompt("alpha-prompt", {"args": "hello world"}, prompts_dir=self.test_dir)
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "# Title One\nhello world")

    @patch('sys.stdin', io.StringIO("multi-line\ninput\n"))
    def test_use_prompt_interactive(self):
        with patch('sys.stderr', new=io.StringIO()):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                promptops_core.use_prompt("alpha-prompt", prompts_dir=self.test_dir)
                output = fake_out.getvalue().strip()
                self.assertEqual(output, "# Title One\nmulti-line\ninput")

    def test_use_prompt_not_found(self):
        with patch('sys.stderr', new=io.StringIO()) as fake_err:
            with self.assertRaises(SystemExit):
                promptops_core.use_prompt("non-existent", prompts_dir=self.test_dir)
            self.assertIn("not found", fake_err.getvalue())

    def test_get_prompts_empty_dir(self):
        empty_dir = tempfile.mkdtemp()
        prompts = promptops_core.get_prompts(empty_dir)
        self.assertEqual(len(prompts), 0)
        shutil.rmtree(empty_dir)

    def test_get_prompts_invalid_toml(self):
        # Create an invalid TOML file
        path = os.path.join(self.test_dir, "invalid.toml")
        with open(path, "w") as f:
            f.write("this is not toml")
        
        prompts = promptops_core.get_prompts(self.test_dir)
        # Should skip the invalid one and still find the others
        self.assertEqual(len(prompts), 3)
        self.assertNotIn("invalid", [p["name"] for p in prompts])

    def test_use_prompt_multiple_variables(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.use_prompt("beta-tool", {"args": "val1", "code": "val2"}, prompts_dir=self.test_dir)
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "# Title Two\nval1 and val2")

    @patch('sys.stdin', io.StringIO("interactive_val\n"))
    def test_use_prompt_partial_flags(self):
        # Pass 'args' via flag, but let 'code' be interactive
        with patch('sys.stderr', new=io.StringIO()):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                promptops_core.use_prompt("beta-tool", {"args": "flag_val"}, prompts_dir=self.test_dir)
                output = fake_out.getvalue().strip()
                self.assertEqual(output, "# Title Two\nflag_val and interactive_val")

    def test_use_prompt_empty_content(self):
        # Create a prompt with empty prompt field
        path = os.path.join(self.test_dir, "empty.toml")
        with open(path, "w") as f:
            f.write('description = "Empty"\nprompt = ""\n')
        
        with patch('sys.stderr', new=io.StringIO()) as fake_err:
            with self.assertRaises(SystemExit):
                promptops_core.use_prompt("empty", prompts_dir=self.test_dir)
            self.assertIn("has no content", fake_err.getvalue())

    def test_search_prompts_no_matches(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.search_prompts("non-existent-search-term", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("No prompts found", output)

    def test_search_prompts_with_tag_no_matches(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.search_prompts("alpha", tag_filter="non-existent-tag", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("No prompts found", output)
            self.assertIn("with tag 'non-existent-tag'", output)

    def test_list_prompts_empty_tag(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            promptops_core.list_prompts(tag_filter="empty-tag", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("No prompts found with tag 'empty-tag'", output)

    def test_get_prompts_non_existent_dir(self):
        prompts = promptops_core.get_prompts("/non/existent/path")
        self.assertEqual(len(prompts), 0)

if __name__ == "__main__":
    unittest.main()
