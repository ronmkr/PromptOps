import os
import sys
import platform
import subprocess
import glob
import datetime
import getpass
import json


# ANSI Colors for better UX
class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# Constants
# Resolve script directory to be robust against symlinks and direct calls
_script_dir = os.path.dirname(os.path.realpath(__file__))


# scripts/promptbook/utils.py -> BASE_DIR is 2 levels up from 'scripts/promptbook'
# Let's find the project root by looking for '.git' or 'commands'
def find_project_root():
    curr = _script_dir
    while curr != os.path.dirname(curr):
        if os.path.exists(os.path.join(curr, "commands")) and os.path.exists(
            os.path.join(curr, "scripts")
        ):
            return curr
        curr = os.path.dirname(curr)
    return os.path.dirname(os.path.dirname(_script_dir))


BASE_DIR = find_project_root()
PROMPTS_DIR = os.path.join(BASE_DIR, "commands", "prompts")
USER_CONFIG_DIR = os.path.expanduser("~/.promptbook")


class AuditLogger:
    """Logs sensitive prompt executions for compliance and auditing."""

    LOG_FILE = os.path.join(USER_CONFIG_DIR, "audit.log")

    @staticmethod
    def log(prompt_name, version, variables, status="success"):
        try:
            os.makedirs(USER_CONFIG_DIR, exist_ok=True)
            timestamp = datetime.datetime.now().isoformat()
            user = getpass.getuser()

            # Mask variables for privacy in logs - only log keys
            var_keys = list(variables.keys())

            log_entry = {
                "timestamp": timestamp,
                "user": user,
                "prompt": prompt_name,
                "version": version or "default",
                "variables": var_keys,
                "status": status,
            }

            with open(AuditLogger.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            # Don't let logging failures crash the main application
            print(
                f"{Colors.YELLOW}Warning: Audit logging failed: {e}{Colors.RESET}",
                file=sys.stderr,
            )


class Vault:
    """Securely manages API keys using OS-level keyring and encryption."""

    VAULT_FILE = os.path.join(USER_CONFIG_DIR, "vault.json")
    SERVICE_NAME = "promptbook"
    KEY_NAME = "master_vault_key"

    @staticmethod
    def _get_master_key():
        """Retrieves or generates a master encryption key stored in the OS keyring."""
        import keyring
        from cryptography.fernet import Fernet

        key = keyring.get_password(Vault.SERVICE_NAME, Vault.KEY_NAME)
        if not key:
            # Generate a new master key
            key = Fernet.generate_key().decode()
            keyring.set_password(Vault.SERVICE_NAME, Vault.KEY_NAME, key)
        return key.encode()

    @staticmethod
    def set_key(provider, api_key):
        """Encrypts and saves an API key for a specific provider."""
        from cryptography.fernet import Fernet

        master_key = Vault._get_master_key()
        f = Fernet(master_key)
        encrypted_key = f.encrypt(api_key.encode()).decode()

        vault_data = {}
        if os.path.exists(Vault.VAULT_FILE):
            with open(Vault.VAULT_FILE, "r") as f_vault:
                try:
                    vault_data = json.load(f_vault)
                except json.JSONDecodeError:
                    pass

        vault_data[provider] = encrypted_key
        os.makedirs(USER_CONFIG_DIR, exist_ok=True)
        with open(Vault.VAULT_FILE, "w") as f_vault:
            json.dump(vault_data, f_vault)

    @staticmethod
    def get_key(provider):
        """Decrypts and retrieves an API key for a provider."""
        from cryptography.fernet import Fernet

        if not os.path.exists(Vault.VAULT_FILE):
            return None

        with open(Vault.VAULT_FILE, "r") as f_vault:
            try:
                vault_data = json.load(f_vault)
            except json.JSONDecodeError:
                return None

        if provider not in vault_data:
            return None

        encrypted_key = vault_data[provider]
        master_key = Vault._get_master_key()
        f = Fernet(master_key)
        try:
            return f.decrypt(encrypted_key.encode()).decode()
        except Exception:
            return None

    @staticmethod
    def list_keys():
        """Lists providers that have keys stored in the vault."""
        if not os.path.exists(Vault.VAULT_FILE):
            return []
        with open(Vault.VAULT_FILE, "r") as f_vault:
            try:
                vault_data = json.load(f_vault)
                return list(vault_data.keys())
            except json.JSONDecodeError:
                return []

    @staticmethod
    def delete_key(provider):
        """Removes a provider's key from the vault."""
        if not os.path.exists(Vault.VAULT_FILE):
            return False

        with open(Vault.VAULT_FILE, "r") as f_vault:
            try:
                vault_data = json.load(f_vault)
            except json.JSONDecodeError:
                return False

        if provider in vault_data:
            del vault_data[provider]
            with open(Vault.VAULT_FILE, "w") as f_vault:
                json.dump(vault_data, f_vault)
            return True
        return False


class InjectionConfig:
    """Central configuration for file injection and context limits."""

    MAX_FILES = 100
    MAX_CHARS = 500000  # ~125k tokens
    TRUNCATION_MARKER = "\n... [TRUNCATED due to length limit] ..."


def copy_to_clipboard(text):
    """Zero-dependency clipboard copy using native OS commands."""
    try:
        os_name = platform.system()
        if os_name == "Darwin":  # macOS
            process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            process.communicate(input=text.encode("utf-8"))
        elif os_name == "Linux":
            try:
                process = subprocess.Popen(
                    ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
                )
                process.communicate(input=text.encode("utf-8"))
            except FileNotFoundError:
                process = subprocess.Popen(
                    ["xsel", "--clipboard", "--input"], stdin=subprocess.PIPE
                )
                process.communicate(input=text.encode("utf-8"))
        elif os_name == "Windows":
            process = subprocess.Popen(["clip.exe"], stdin=subprocess.PIPE)
            process.communicate(input=text.encode("utf-8"))
        return True
    except Exception:
        return False


def resolve_file_injection(val):
    """
    Resolves file injection. Supports:
    - @path/to/file (Single file)
    - @path/to/*.py (Glob pattern)
    Concatenates multiple files with headers.
    """
    if not val.startswith("@"):
        return val

    pattern = val[1:]
    matches = glob.glob(pattern, recursive=True)

    if not matches:
        if any(char in pattern for char in "*?[]"):
            print(
                f"{Colors.YELLOW}Warning: No files matched glob '{pattern}'. Using raw string.{Colors.RESET}",
                file=sys.stderr,
            )
        elif not os.path.exists(pattern):
            print(
                f"{Colors.YELLOW}Warning: File {pattern} not found. Using raw string.{Colors.RESET}",
                file=sys.stderr,
            )
        return val

    files = sorted([m for m in matches if os.path.isfile(m)])
    if not files:
        return val

    # Safety check for large number of files
    if len(files) > InjectionConfig.MAX_FILES:
        print(
            f"{Colors.YELLOW}⚠️  Warning: Glob pattern '{pattern}' matched {len(files)} files.{Colors.RESET}",
            file=sys.stderr,
        )
        print(
            f"{Colors.YELLOW}Truncating to first {InjectionConfig.MAX_FILES} files to prevent context overflow.{Colors.RESET}",
            file=sys.stderr,
        )
        files = files[: InjectionConfig.MAX_FILES]

    contents = []
    total_chars = 0

    for f_path in files:
        try:
            if total_chars >= InjectionConfig.MAX_CHARS:
                print(
                    f"{Colors.YELLOW}⚠️  Warning: Maximum character limit reached ({InjectionConfig.MAX_CHARS}). Truncating further files.{Colors.RESET}",
                    file=sys.stderr,
                )
                break

            with open(f_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                file_text = (
                    f"--- File: {f_path} ---\n{content}" if len(files) > 1 else content
                )

                if total_chars + len(file_text) > InjectionConfig.MAX_CHARS:
                    # Truncate this file to fit the limit
                    remaining = InjectionConfig.MAX_CHARS - total_chars
                    if remaining > 50:
                        file_text = (
                            file_text[:remaining] + InjectionConfig.TRUNCATION_MARKER
                        )
                        contents.append(file_text)
                    print(
                        f"{Colors.YELLOW}⚠️  Warning: Maximum character limit reached. Truncated {f_path}.{Colors.RESET}",
                        file=sys.stderr,
                    )
                    break

                contents.append(file_text)
                total_chars += len(file_text)
        except Exception as e:
            print(
                f"{Colors.YELLOW}Warning: Could not read file {f_path} ({e}).{Colors.RESET}",
                file=sys.stderr,
            )

    return "\n\n".join(contents).strip()
