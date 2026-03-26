import os
import sys
import unittest

# Add scripts to path
base_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.append(os.path.join(base_dir, "scripts"))

from promptbook.engine.template import TemplateEngine  # noqa: E402


class TestEngine(unittest.TestCase):
    # --- 1. Hydration & Nesting ---

    def test_hydrate_prompt_nested_shell(self):
        """Test nested variables inside a shell block."""
        template = "Output: {{$(echo {{args}})}}"
        vars = {"args": "hello-world"}
        result = TemplateEngine.hydrate(template, vars)
        self.assertEqual(result, "Output: hello-world")

    def test_hydrate_prompt_multiple_nested(self):
        """Test multiple nested blocks."""
        template = "{{$(echo {{a}} {{b}})}}"
        vars = {"a": "part1", "b": "part2"}
        result = TemplateEngine.hydrate(template, vars)
        self.assertEqual(result, "part1 part2")

    def test_hydrate_prompt_shell_injection_prevention(self):
        """Test that malicious payloads are safely quoted in shell blocks."""
        template = "Result: {{$(echo {{args}})}}"
        # Malicious payload: tries to execute echo INJECTED
        vars = {"args": "safe; echo INJECTED"}
        result = TemplateEngine.hydrate(template, vars)
        # Expected: echo 'safe; echo INJECTED' -> Literal output
        self.assertEqual(result, "Result: safe; echo INJECTED")

    def test_hydrate_prompt_balanced_braces(self):
        """Test that balanced braces handle complex structures correctly."""
        # A template that looks like it has nested blocks but they are just text
        template = 'JSON: {{$(echo \'{"key": "{{args}}"}\')}}'
        vars = {"args": "val"}
        result = TemplateEngine.hydrate(template, vars)
        # Quoting will make it: echo '{"key": "val"}'
        self.assertEqual(result, 'JSON: {"key": "val"}')

    def test_discover_variables_nested(self):
        """Test variable discovery with nested shell blocks."""
        template = "Output: {{$(echo {{args}} {{code}})}}"
        vars = TemplateEngine.discover_variables(template)
        self.assertEqual(vars, {"args", "code"})


if __name__ == "__main__":
    unittest.main()
