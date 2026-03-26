import glob
import os
import platform
import subprocess
import sys

from ..config import Colors, InjectionConfig


def copy_to_clipboard(text: str) -> bool:
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


def resolve_file_injection(val: str) -> str:
    """Resolves @file.txt or @*.py patterns into content."""
    if not val.startswith("@"):
        return val

    pattern = val[1:]
    matches = glob.glob(pattern, recursive=True)

    if not matches:
        return val

    files = sorted([m for m in matches if os.path.isfile(m)])
    if not files:
        return val

    if len(files) > InjectionConfig.MAX_FILES:
        print(
            f"{Colors.YELLOW}Warning: Truncating {len(files)} matches to {InjectionConfig.MAX_FILES}{Colors.RESET}",
            file=sys.stderr,
        )
        files = files[: InjectionConfig.MAX_FILES]

    contents = []
    total_chars = 0

    for f_path in files:
        if total_chars >= InjectionConfig.MAX_CHARS:
            break
        try:
            with open(f_path, encoding="utf-8") as f:
                content = f.read().strip()
                file_text = f"--- File: {f_path} ---\n{content}" if len(files) > 1 else content
                if total_chars + len(file_text) > InjectionConfig.MAX_CHARS:
                    contents.append(file_text[: InjectionConfig.MAX_CHARS - total_chars] + "...")
                    break
                contents.append(file_text)
                total_chars += len(file_text)
        except Exception as e:
            print(f"Warning: Could not read {f_path} ({e})", file=sys.stderr)

    return "\n\n".join(contents).strip()


class AuditLogger:
    """Logs sensitive prompt executions."""

    @staticmethod
    def log(name: str, version_id: str | None, variables: dict):
        import datetime
        import getpass
        import json

        from ..config import StoragePaths

        os.makedirs(os.path.dirname(StoragePaths.LOG_FILE), exist_ok=True)
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": getpass.getuser(),
            "prompt": name,
            "version": version_id,
            "variables": {k: "MASKED" for k in variables.keys()},
        }
        try:
            with open(StoragePaths.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass
