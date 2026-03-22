import unittest
import os
import sys
import tempfile
import shutil

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import validate_prompts  # noqa: E402


class TestPromptValidation(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_prompt_file(self, filename, content):
        path = os.path.join(self.test_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        return path

    def test_valid_prompt(self):
        content = """
description      = "A valid description."
args_description = "Valid input"
version          = "1.0.0"
last_updated     = "2026-03-21"
tags             = ["test"]
prompt           = "# Title\\n{{args}}"
"""
        path = self.create_prompt_file("valid-prompt.toml", content)
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertEqual(len(errors), 0)

    def test_invalid_filename(self):
        path = self.create_prompt_file("Invalid_Name.toml", "")
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertIn("must be lowercase kebab-case", errors[0])

    def test_missing_fields(self):
        content = 'description = "Missing others."'
        path = self.create_prompt_file("missing.toml", content)
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        # Should catch missing version, last_updated, prompt, tags, args_description
        self.assertTrue(len(errors) >= 5)

    def test_invalid_version(self):
        content = """
description      = "Desc."
args_description = "Input"
version          = "1.0"
last_updated     = "2026-03-21"
tags             = ["test"]
prompt           = "# Title\\n{{args}}"
"""
        path = self.create_prompt_file("bad-version.toml", content)
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertIn("Invalid version", errors[0])

    def test_invalid_date(self):
        content = """
description      = "Desc."
args_description = "Input"
version          = "1.0.0"
last_updated     = "2026-99-99"
tags             = ["test"]
prompt           = "# Title\\n{{args}}"
"""
        path = self.create_prompt_file("bad-date.toml", content)
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertIn("not a valid calendar date", errors[0])

    def test_description_no_period(self):
        content = """
description      = "No period here"
args_description = "Input"
version          = "1.0.0"
last_updated     = "2026-03-21"
tags             = ["test"]
prompt           = "# Title\\n{{args}}"
"""
        path = self.create_prompt_file("no-period.toml", content)
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertIn("end with a period", errors[0])

    def test_duplicate_tags(self):
        content = """
description      = "Desc."
args_description = "Input"
version          = "1.0.0"
last_updated     = "2026-03-21"
tags             = ["test", "test"]
prompt           = "# Title\\n{{args}}"
"""
        path = self.create_prompt_file("dup-tags.toml", content)
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertIn("Duplicate tag found", errors[0])

    def test_no_markdown_header(self):
        content = """
description      = "Desc."
args_description = "Input"
version          = "1.0.0"
last_updated     = "2026-03-21"
tags             = ["test"]
prompt           = "No header here {{args}}"
"""
        path = self.create_prompt_file("no-header.toml", content)
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertIn("contain at least one Markdown header", errors[0])

    def test_no_variables(self):
        content = """
description      = "Desc."
args_description = "Input"
version          = "1.0.0"
last_updated     = "2026-03-21"
tags             = ["test"]
prompt           = "# Title\\nNo vars here."
"""
        path = self.create_prompt_file("no-vars.toml", content)
        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertIn("contains no variables", errors[0])

    def test_nested_invalid_name(self):
        # Create a subdirectory
        sub_dir = os.path.join(self.test_dir, "nested-tool")
        os.makedirs(sub_dir)
        # Create a file with invalid name in it (e.g. spaces)
        path = os.path.join(sub_dir, "Invalid Version.toml")
        with open(path, "w") as f:
            f.write("")

        validator = validate_prompts.PromptValidator(path)
        errors = validator.validate()
        self.assertIn("must be lowercase kebab-case", errors[0])


if __name__ == "__main__":
    unittest.main()
