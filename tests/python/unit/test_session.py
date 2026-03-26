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

from promptbook.engine.session import SessionManager  # noqa: E402


class TestSession(unittest.TestCase):
    def setUp(self):
        self.user_config_dir = tempfile.mkdtemp()
        self.profiles_file = os.path.join(self.user_config_dir, "profiles.json")

        # Mock storage paths in config
        self.patcher_profiles = patch(
            "promptbook.config.StoragePaths.PROFILES_FILE", self.profiles_file
        )
        self.patcher_user_dir = patch("promptbook.config.USER_CONFIG_DIR", self.user_config_dir)

        self.patcher_profiles.start()
        self.patcher_user_dir.start()

        self.session_manager = SessionManager(self.profiles_file)

    def tearDown(self):
        self.patcher_profiles.stop()
        self.patcher_user_dir.stop()
        shutil.rmtree(self.user_config_dir)

    def test_profile_management(self):
        """Test creating, listing, loading, and deleting profiles."""
        profile_name = "test-prof"
        vars = {"project": "PB", "lang": "rust"}

        # Save
        self.session_manager.save_profile(profile_name, vars)
        self.assertTrue(os.path.exists(self.profiles_file))

        # List
        profiles = self.session_manager.list_profiles()
        self.assertIn(profile_name, profiles)

        # Load
        loaded_vars = self.session_manager.load_profile(profile_name)
        self.assertEqual(loaded_vars, vars)

        # Delete
        self.session_manager.delete_profile(profile_name)
        self.assertNotIn(profile_name, self.session_manager.list_profiles())


if __name__ == "__main__":
    unittest.main()
