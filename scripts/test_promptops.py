import unittest
import os
import sys
import tempfile
import shutil
import io
from unittest.mock import patch

# Import the core logic directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from promptops import core, utils, cli  # noqa: E402


class TestPromptOps(unittest.TestCase):
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
        self.create_prompt(
            "gamma-helper", "Other desc.", ["tag3"], "# Title Three\nNo vars."
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_prompt(self, name, description, tags, prompt_content):
        path = os.path.join(self.test_dir, f"{name}.toml")
        with open(path, "w") as f:
            f.write(f'description = "{description}"\n')
            f.write('version     = "1.0.0"\n')
            f.write('last_updated = "2026-03-21"\n')
            tags_str = str(tags).replace("'", '"')
            f.write(f"tags         = {tags_str}\n\n")
            f.write(f'prompt      = """\n{prompt_content}\n"""\n')

    def test_get_prompts(self):
        prompts = core.get_prompts(self.test_dir)
        self.assertEqual(len(prompts), 3)
        self.assertEqual(prompts[0]["name"], "alpha-prompt")

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

    def test_search_prompts_fuzzy(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            # "alph" should match "alpha-prompt"
            core.search_prompts("alph", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)

    def test_use_prompt_with_flags(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.use_prompt(
                "alpha-prompt", {"args": "hello world"}, prompts_dir=self.test_dir
            )
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

    def test_get_prompts_invalid_toml(self):
        # Create an invalid TOML file
        path = os.path.join(self.test_dir, "invalid.toml")
        with open(path, "w") as f:
            f.write("this is not toml")

        prompts = core.get_prompts(self.test_dir)
        # Should skip the invalid one and still find the others
        self.assertEqual(len(prompts), 3)
        self.assertNotIn("invalid", [p["name"] for p in prompts])

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
                core.use_prompt(
                    "beta-tool", {"args": "flag_val"}, prompts_dir=self.test_dir
                )
                output = fake_out.getvalue().strip()
                self.assertEqual(output, "# Title Two\nflag_val and interactive_val")

    def test_use_prompt_empty_content(self):
        # Create a prompt with empty prompt field
        path = os.path.join(self.test_dir, "empty.toml")
        with open(path, "w") as f:
            f.write('description = "Empty"\nprompt = ""\n')

        with patch("sys.stderr", new=io.StringIO()) as fake_err:
            with self.assertRaises(SystemExit):
                core.use_prompt("empty", prompts_dir=self.test_dir)
            self.assertIn("has no content", fake_err.getvalue())

    def test_search_prompts_no_matches(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.search_prompts("non-existent-search-term", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("No prompts found", output)

    def test_search_prompts_with_tag_no_matches(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.search_prompts(
                "alpha", tag_filter="non-existent-tag", prompts_dir=self.test_dir
            )
            output = fake_out.getvalue()
            self.assertIn("No prompts found", output)
            self.assertIn("with tag 'non-existent-tag'", output)

    def test_list_prompts_empty_tag(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.list_prompts(tag_filter="empty-tag", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("No prompts found with criteria", output)

    def test_list_tags_raw(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            core.list_tags(prompts_dir=self.test_dir, raw=True)
            output = fake_out.getvalue()
            # Raw output should be one tag per line, sorted
            self.assertEqual(output, "common\ntag1\ntag2\ntag3\n")

    def test_list_names(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            cli.list_names(prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            # Should list prompt names, sorted
            self.assertEqual(output, "alpha-prompt\nbeta-tool\ngamma-helper\n")

    def test_hydrate_prompt_escaped_backslash(self):
        # Test that we can't easily escape the escape char yet,
        # but let's see how it behaves with double backslash
        template = "\\\\{{name}}"
        vars = {"name": "Alice"}
        result = core.hydrate_prompt(template, vars)
        # Current logic: group 1 matches the first \, then we return {{name}}
        # The first \ remains. So \{{name}} -> \Alice? No, let's check.
        # Actually our logic: if escape_char == '\', return '{{var}}'.
        # So \\{{name}} -> \ + {{name}} -> \{{name}}
        self.assertEqual(result, "\\{{name}}")

    def test_get_prompts_non_existent_dir(self):
        prompts = core.get_prompts("/non/existent/path")
        self.assertEqual(len(prompts), 0)

    def test_hydrate_prompt_escaping(self):
        template = "Hello {{name}}, usage: \\{{literal}}"
        vars = {"name": "Alice"}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "Hello Alice, usage: {{literal}}")

    def test_hydrate_prompt_whitespace(self):
        template = "Hello {{ name }}, code: {{code}}"
        vars = {"name": "Alice", "code": "print()"}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "Hello Alice, code: print()")

    def test_hydrate_prompt_missing_var(self):
        template = "Hello {{name}}, {{missing}}"
        vars = {"name": "Alice"}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "Hello Alice, {{missing}}")

    def test_hydrate_prompt_multiple_same(self):
        template = "{{name}} and {{name}}"
        vars = {"name": "Alice"}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "Alice and Alice")

    def test_hydrate_prompt_numeric_underscore(self):
        template = "{{var_1}}"
        vars = {"var_1": "success"}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "success")

    def test_hydrate_prompt_no_vars(self):
        template = "No variables here."
        vars = {"name": "Alice"}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "No variables here.")

    def test_hydrate_prompt_empty_value(self):
        template = "[{{empty}}]"
        vars = {"empty": ""}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "[]")

    def test_search_prompts_description(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            # Search for "Other" which is in gamma-helper description
            core.search_prompts("Other", prompts_dir=self.test_dir)
            output = fake_out.getvalue()
            self.assertIn("gamma-helper", output)

    def test_search_prompts_with_tag_filter(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            # Search for "Description" but filter by tag "tag1"
            core.search_prompts(
                "Description", tag_filter="tag1", prompts_dir=self.test_dir
            )
            output = fake_out.getvalue()
            self.assertIn("alpha-prompt", output)
            self.assertNotIn("beta-tool", output)  # has tag2

    def test_generate_completion(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            cli.generate_completion("zsh")
            output = fake_out.getvalue()
            self.assertIn("#compdef pop", output)
            self.assertIn("zsh", output)

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

    def test_resolve_file_injection_missing_file(self):
        val = "@/non/existent/file"
        with patch("sys.stderr", new=io.StringIO()) as fake_err:
            result = utils.resolve_file_injection(val)
            self.assertEqual(result, "@/non/existent/file")
            self.assertIn("not found", fake_err.getvalue())

    def test_resolve_file_injection_glob(self):
        # Create two temp files
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f1:
            f1.write("C1")
            p1 = f1.name
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f2:
            f2.write("C2")
            p2 = f2.name

        try:
            # Match both using a glob (using the common prefix/suffix)
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

    def test_hydrate_prompt_missing_var_with_spaces(self):
        template = "Hello {{ name }}, {{ missing }}"
        vars = {"name": "Alice"}
        result = core.hydrate_prompt(template, vars)
        # Should leave the missing placeholder intact
        self.assertEqual(result, "Hello Alice, {{ missing }}")

    def test_resolve_file_injection_recursive_glob(self):
        # Create a nested structure
        sub_dir = os.path.join(self.test_dir, "nest")
        os.makedirs(sub_dir)
        with open(os.path.join(sub_dir, "deep.txt"), "w") as f:
            f.write("DEEP")

        try:
            pattern = os.path.join(self.test_dir, "**", "*.txt")
            val = f"@{pattern}"
            result = utils.resolve_file_injection(val)
            self.assertIn("DEEP", result)
        finally:
            shutil.rmtree(sub_dir)

    def test_use_prompt_invalid_version(self):
        with patch("sys.stderr", new=io.StringIO()) as fake_err:
            with self.assertRaises(SystemExit):
                core.use_prompt(
                    "alpha-prompt", version_hint="v999", prompts_dir=self.test_dir
                )
            self.assertIn(
                "Version 'v999' for prompt 'alpha-prompt' not found",
                fake_err.getvalue(),
            )


if __name__ == "__main__":
    unittest.main()
