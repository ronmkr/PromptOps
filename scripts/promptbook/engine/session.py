import json
import os
import sys

from ..config import USER_CONFIG_DIR, Colors, StoragePaths


class SessionManager:
    """Manages context profiles and multi-step prompt chains."""

    def __init__(self, profiles_file: str = StoragePaths.PROFILES_FILE):
        self.profiles_file = profiles_file

    def save_profile(self, name: str, variables: dict[str, str]) -> bool:
        """Saves a named profile of variables."""
        os.makedirs(USER_CONFIG_DIR, exist_ok=True)
        profiles = self.get_all_profiles()
        profiles[name] = variables
        try:
            with open(self.profiles_file, "w", encoding="utf-8") as f:
                json.dump(profiles, f, indent=2)
            return True
        except Exception as e:
            print(f"{Colors.RED}Error saving profile: {e}{Colors.RESET}", file=sys.stderr)
            return False

    def load_profile(self, name: str) -> dict[str, str] | None:
        """Loads a named profile of variables."""
        profiles = self.get_all_profiles()
        return profiles.get(name)

    def get_all_profiles(self) -> dict[str, dict[str, str]]:
        """Returns all saved profiles."""
        if not os.path.exists(self.profiles_file):
            return {}
        try:
            with open(self.profiles_file, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def list_profiles(self) -> list[str]:
        """Lists available context profile names."""
        return list(self.get_all_profiles().keys())

    def delete_profile(self, name: str) -> bool:
        """Deletes a named profile."""
        profiles = self.get_all_profiles()
        if name in profiles:
            del profiles[name]
            try:
                with open(self.profiles_file, "w", encoding="utf-8") as f:
                    json.dump(profiles, f, indent=2)
                return True
            except Exception as e:
                print(f"{Colors.RED}Error deleting profile: {e}{Colors.RESET}", file=sys.stderr)
                return False
        return False
