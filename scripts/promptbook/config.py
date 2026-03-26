import os
import platform

# Resolve base directory to be robust against symlinks and direct calls
_current_dir = os.path.dirname(os.path.realpath(__file__))


def _find_project_root():
    curr = _current_dir
    while curr != os.path.dirname(curr):
        if os.path.exists(os.path.join(curr, "commands")) and os.path.exists(
            os.path.join(curr, "scripts")
        ):
            return curr
        curr = os.path.dirname(curr)
    return os.path.dirname(os.path.dirname(_current_dir))


BASE_DIR = _find_project_root()
PROMPTS_DIR = os.path.join(BASE_DIR, "commands", "prompts")
USER_CONFIG_DIR = os.path.expanduser("~/.promptbook")


class Colors:
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


class InjectionConfig:
    MAX_FILES = 100
    MAX_CHARS = 500000  # ~125k tokens
    TRUNCATION_MARKER = "\n... [TRUNCATED due to length limit] ..."


class StoragePaths:
    VAULT_FILE = os.path.join(USER_CONFIG_DIR, "vault.json")
    PROFILES_FILE = os.path.join(USER_CONFIG_DIR, "profiles.json")
    LOG_FILE = os.path.join(USER_CONFIG_DIR, "audit.log")


class SystemInfo:
    OS = platform.system()
    IS_WINDOWS = OS == "Windows"
    IS_MACOS = OS == "Darwin"
    IS_LINUX = OS == "Linux"
