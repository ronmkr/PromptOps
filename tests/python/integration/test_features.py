import io
import json
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

from promptbook import config, core  # noqa: E402
from promptbook.providers.llm import Vault  # noqa: E402


class TestFeatures(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.user_config_dir = tempfile.mkdtemp()
        # Mock storage paths in config
        self.patcher_vault = patch(
            "promptbook.config.StoragePaths.VAULT_FILE",
            os.path.join(self.user_config_dir, "vault.json"),
        )
        self.patcher_profiles = patch(
            "promptbook.config.StoragePaths.PROFILES_FILE",
            os.path.join(self.user_config_dir, "profiles.json"),
        )
        self.patcher_log = patch(
            "promptbook.config.StoragePaths.LOG_FILE",
            os.path.join(self.user_config_dir, "audit.log"),
        )
        self.patcher_user_dir = patch("promptbook.config.USER_CONFIG_DIR", self.user_config_dir)

        self.patcher_vault.start()
        self.patcher_profiles.start()
        self.patcher_log.start()
        self.patcher_user_dir.start()

    def tearDown(self):
        self.patcher_vault.stop()
        self.patcher_profiles.stop()
        self.patcher_log.stop()
        self.patcher_user_dir.stop()
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.user_config_dir)

    # --- 1. Interactive Mode & State Machine ---

    @patch("promptbook.core._get_char")
    def test_collect_variables_back_navigation(self, mock_get_char):
        """Test that Ctrl+B (\\x02) correctly navigates back in the state machine."""
        display_name = "test-prompt"
        variables = ["var1", "var2"]
        data = {}
        provided_vars = {}

        # Sequence: val1 -> G (finish var1) -> B (back) -> new1 -> G (finish var1) -> val2 -> G (finish var2)
        chars = list("val1\x07\x02new1\x07val2\x07")
        mock_get_char.side_effect = chars

        with patch("sys.stdin.isatty", return_value=True):
            with patch("sys.stderr", new=io.StringIO()):
                final_vars = core._collect_variables(display_name, variables, data, provided_vars)

        self.assertEqual(final_vars["var1"], "new1")
        self.assertEqual(final_vars["var2"], "val2")

    # --- 2. Secure Vault ---

    def test_vault_operations(self):
        """Test setting and getting keys from the vault."""
        Vault.set_key("openai", "sk-test-key")
        retrieved = Vault.get_key("openai")
        self.assertEqual(retrieved, "sk-test-key")
        self.assertIn("openai", Vault.list_keys())
        Vault.delete_key("openai")
        self.assertNotIn("openai", Vault.list_keys())

    # ---  PI Masking ---

    def test_pii_masking_enabled(self):
        """Test that --mask correctly anonymizes PII."""
        prompt_path = os.path.join(self.test_dir, "pii-test.toml")
        with open(prompt_path, "w") as f:
            f.write(
                'description = "PII Test"\ntags = ["test"]\nprompt = "Email: {{args}}"\nlast_updated="2024-01-01"'
            )

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.stderr", new=io.StringIO()):
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
                except ImportError:
                    self.skipTest("scrubadub not installed")

    # --- Audit Logging ---

    def test_audit_logging(self):
        """Test that sensitive prompts are logged correctly."""
        prompt_path = os.path.join(self.test_dir, "sensitive-test.toml")
        with open(prompt_path, "w") as f:
            f.write(
                'description = "Sensitive"\nsensitive = true\ntags = ["test"]\nprompt = "Code: {{args}}"\nlast_updated = "2024-01-01"'
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

        log_file = config.StoragePaths.LOG_FILE
        self.assertTrue(os.path.exists(log_file))
        with open(log_file) as f:
            log_line = f.readline()
            log_entry = json.loads(log_line)
            self.assertEqual(log_entry["prompt"], "sensitive-test")
            self.assertIn("args", log_entry["variables"])
            self.assertNotIn("secret-code", log_line)

    @patch("promptbook.core.use_prompt")
    @patch("promptbook.providers.llm.LLMProvider.execute")
    def test_prompt_chaining(self, mock_execute, mock_use_prompt):
        """Test that prompt chaining calls use_prompt and execute correctly."""
        mock_use_prompt.side_effect = [
            {"legacy": "prompt1", "system": "", "user": "", "vars": {}},
            {"legacy": "prompt2", "system": "", "user": "", "vars": {}},
        ]
        mock_execute.side_effect = ["output1", "output2"]

        with patch("sys.stdout", new=io.StringIO()):
            core.chain_prompts(["p1", "p2"], initial_args="start")

        # First call should have initial args
        self.assertEqual(mock_use_prompt.call_args_list[0][0][0], "p1")
        self.assertEqual(mock_use_prompt.call_args_list[0][1]["provided_vars"]["args"], "start")

        # Second call should have output of first call as args
        self.assertEqual(mock_use_prompt.call_args_list[1][0][0], "p2")
        self.assertEqual(mock_use_prompt.call_args_list[1][1]["provided_vars"]["args"], "output1")

        self.assertEqual(mock_execute.call_count, 2)


if __name__ == "__main__":
    unittest.main()
