import unittest
import os
import sys
import tempfile
import shutil
import io
import json
from unittest.mock import patch

# Add scripts to path so we can import our package
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, "scripts"))
from promptbook import core, utils  # noqa: E402


class TestFeaturesExtended(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.user_config_dir = tempfile.mkdtemp()
        # Mock USER_CONFIG_DIR in utils
        self.patcher_config = patch(
            "promptbook.utils.USER_CONFIG_DIR", self.user_config_dir
        )
        self.patcher_config.start()
        # Mock AuditLogger log file path
        utils.AuditLogger.LOG_FILE = os.path.join(self.user_config_dir, "audit.log")
        utils.Vault.VAULT_FILE = os.path.join(self.user_config_dir, "vault.json")

    def tearDown(self):
        self.patcher_config.stop()
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.user_config_dir)

    # --- 1. Hydration & Nesting ---

    def test_hydrate_prompt_nested_shell(self):
        """Test nested variables inside a shell block."""
        template = "Output: {{$(echo {{args}})}}"
        vars = {"args": "hello-world"}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "Output: hello-world")

    def test_hydrate_prompt_multiple_nested(self):
        """Test multiple nested blocks."""
        template = "{{$(echo {{a}} {{b}})}}"
        vars = {"a": "part1", "b": "part2"}
        result = core.hydrate_prompt(template, vars)
        self.assertEqual(result, "part1 part2")

    def test_hydrate_prompt_shell_injection_prevention(self):
        """Test that malicious payloads are safely quoted in shell blocks."""
        template = "Result: {{$(echo {{args}})}}"
        # Malicious payload: tries to execute echo INJECTED
        vars = {"args": "safe; echo INJECTED"}
        result = core.hydrate_prompt(template, vars)
        # Expected: echo 'safe; echo INJECTED' -> Literal output
        self.assertEqual(result, "Result: safe; echo INJECTED")

    def test_hydrate_prompt_balanced_braces(self):
        """Test that balanced braces handle complex structures correctly."""
        # A template that looks like it has nested blocks but they are just text
        template = 'JSON: {{$(echo \'{"key": "{{args}}"}\')}}'
        vars = {"args": "val"}
        result = core.hydrate_prompt(template, vars)
        # Quoting will make it: echo '{"key": "val"}'
        self.assertEqual(result, 'JSON: {"key": "val"}')

    # --- 2. Interactive Mode & State Machine ---

    @patch("promptbook.core._get_char")
    def test_collect_variables_back_navigation(self, mock_get_char):
        """Test that Ctrl+B (\\x02) correctly navigates back in the state machine."""
        display_name = "test-prompt"
        variables = ["var1", "var2"]
        data = {}
        provided_vars = {}

        # Sequence of characters:
        # 1. 'val1' for var1, then Ctrl+G (\x07) to finish
        # 2. Ctrl+B (\x02) to go back from var2 to var1
        # 3. 'new1' for var1, then Ctrl+G (\x07)
        # 4. 'val2' for var2, then Ctrl+G (\x07)
        chars = list("val1\x07\x02new1\x07val2\x07")
        mock_get_char.side_effect = chars

        # We need to mock sys.stdin.isatty to True for interactive mode
        with patch("sys.stdin.isatty", return_value=True):
            with patch("sys.stderr", new=io.StringIO()):
                final_vars = core._collect_variables(
                    display_name, variables, data, provided_vars
                )

        self.assertEqual(final_vars["var1"], "new1")
        self.assertEqual(final_vars["var2"], "val2")

    @patch("promptbook.core._get_char")
    def test_collect_variables_finish_ctrl_d(self, mock_get_char):
        """Test that Ctrl+D (\\x04) also finishes input."""
        mock_get_char.side_effect = list("test\x04")
        with patch("sys.stdin.isatty", return_value=True):
            with patch("sys.stderr", new=io.StringIO()):
                final_vars = core._collect_variables("test", ["args"], {}, {})
        self.assertEqual(final_vars["args"], "test")

    # --- 3. Secure Vault ---

    def test_vault_operations(self):
        """Test setting and getting keys from the vault."""
        try:
            # import cryptography to generate a key
            from cryptography.fernet import Fernet
        except ImportError:
            self.skipTest("Vault dependencies (cryptography) missing")

        # Generate a valid key for testing
        valid_key = Fernet.generate_key()

        # Patch the master key retrieval to return our valid test key
        with patch("promptbook.utils.Vault._get_master_key", return_value=valid_key):
            utils.Vault.set_key("openai", "sk-test-key")

            # Check if vault.json was created
            self.assertTrue(os.path.exists(utils.Vault.VAULT_FILE))

            # Verify we can retrieve it
            retrieved = utils.Vault.get_key("openai")
            self.assertEqual(retrieved, "sk-test-key")

            # Test listing
            providers = utils.Vault.list_keys()
            self.assertIn("openai", providers)

            # Test delete
            utils.Vault.delete_key("openai")
            self.assertNotIn("openai", utils.Vault.list_keys())

    # --- 4. PII Masking ---

    def test_pii_masking_enabled(self):
        """Test that --mask correctly anonymizes PII."""
        # Create a test prompt file
        prompt_path = os.path.join(self.test_dir, "pii-test.toml")
        with open(prompt_path, "w") as f:
            f.write(
                'description = "PII Test"\ntags = ["test"]\nprompt = "Email: {{args}}"'
            )

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.stderr", new=io.StringIO()):
                # We need scrubadub to be available for this test to be meaningful
                # but we can also mock it if needed.
                try:
                    import scrubadub

                    assert scrubadub is not None

                    core.use_prompt(
                        "pii-test",
                        {"args": "test@example.com"},
                        prompts_dir=self.test_dir,
                        mask=True,
                        no_copy=True,
                    )
                    output = fake_out.getvalue().strip()
                    self.assertIn("Email: {{EMAIL}}", output)
                    self.assertNotIn("test@example.com", output)
                except ImportError:
                    self.skipTest("scrubadub not installed")

    # --- 5. Audit Logging ---

    def test_audit_logging(self):
        """Test that sensitive prompts are logged correctly."""
        prompt_path = os.path.join(self.test_dir, "sensitive-test.toml")
        with open(prompt_path, "w") as f:
            f.write(
                'description = "Sensitive"\nsensitive = true\ntags = ["test"]\nprompt = "Code: {{args}}"'
            )

        with patch("sys.stdout", new=io.StringIO()):
            with patch("sys.stderr", new=io.StringIO()):
                core.use_prompt(
                    "sensitive-test",
                    {"args": "secret-code"},
                    prompts_dir=self.test_dir,
                    no_copy=True,
                    auto_confirm=True,
                )

        # Verify log entry
        self.assertTrue(os.path.exists(utils.AuditLogger.LOG_FILE))
        with open(utils.AuditLogger.LOG_FILE, "r") as f:
            log_line = f.readline()
            log_entry = json.loads(log_line)
            self.assertEqual(log_entry["prompt"], "sensitive-test")
            self.assertEqual(log_entry["variables"], ["args"])
            # Values should NOT be in the log
            self.assertNotIn("secret-code", log_line)


if __name__ == "__main__":
    unittest.main()
