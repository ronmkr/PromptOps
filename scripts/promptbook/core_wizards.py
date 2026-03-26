import datetime
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from contextlib import redirect_stdout

from .config import BASE_DIR, PROMPTS_DIR, Colors


def create_wizard():
    """Interactive wizard to create a new prompt template."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}✨ New Prompt Template Wizard{Colors.RESET}")
    print("-------------------------------------------------------\n")

    # 1. Name
    name = ""
    while not name:
        name = (
            input(f"{Colors.BOLD}1. Prompt Name{Colors.RESET} (e.g., my-new-tool): ")
            .strip()
            .lower()
        )
        name = re.sub(r"[^a-z0-9-]", "-", name)
        if not name:
            print(f"{Colors.YELLOW}Name is required.{Colors.RESET}")

    # 2. Category
    prompts_dir = PROMPTS_DIR
    categories = sorted(
        [d for d in os.listdir(prompts_dir) if os.path.isdir(os.path.join(prompts_dir, d))]
    )

    print(f"\n{Colors.BOLD}2. Select Category:{Colors.RESET}")
    for i, cat in enumerate(categories):
        print(f"  {i + 1}) {cat}")
    print(f"  {len(categories) + 1}) [Create New Category]")

    cat_choice = 0
    category = ""
    while cat_choice < 1 or cat_choice > len(categories) + 1:
        try:
            choice = input(f"\nChoice (1-{len(categories) + 1}): ")
            cat_choice = int(choice)
        except ValueError:
            continue

    if cat_choice == len(categories) + 1:
        category = input("New category name: ").strip().lower()
        category = re.sub(r"[^a-z0-9-]", "-", category)
    else:
        category = categories[cat_choice - 1]

    # 3. Metadata
    print(f"\n{Colors.BOLD}3. Metadata{Colors.RESET}")
    description = input("   Description: ").strip()
    if not description.endswith("."):
        description += "."

    args_desc = (
        input("   Arguments Description (e.g., 'Source Code', 'JSON Data'): ").strip()
        or "Input Data"
    )

    # 4. Tags
    print(f"\n{Colors.BOLD}4. Tags{Colors.RESET} (comma-separated, e.g., engineering, security):")
    tags_input = input("   Tags: ").strip()
    tags = [t.strip().lower() for t in tags_input.split(",") if t.strip()]
    if category not in tags:
        tags.append(category)
    tags = sorted(list(set(tags)))

    # 5. Prompt Mode
    print(f"\n{Colors.BOLD}5. Prompt Mode{Colors.RESET}")
    print("  1) Single Prompt (Standard)")
    print("  2) Multi-Message Prompt (System + User)")

    prompt_mode = 0
    while prompt_mode < 1 or prompt_mode > 2:
        try:
            choice = input("\nChoice (1-2): ")
            prompt_mode = int(choice)
        except ValueError:
            continue

    prompt_content = ""
    system_prompt = ""
    user_prompt = ""

    if prompt_mode == 1:
        # 5.1 Single Prompt Content
        print(f"\n{Colors.BOLD}5.1 Prompt Instructions{Colors.RESET}")
        print("   Enter your prompt below. Use {{args}} for primary input.")
        print("   Press Ctrl+D (Mac/Linux) or Ctrl+Z+Enter (Win) when finished.")
        print(f"{Colors.YELLOW}   " + "─" * 40 + f"{Colors.RESET}")

        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        prompt_content = "\n".join(lines).strip()
    else:
        # 5.1 System Prompt Content
        print(f"\n{Colors.BOLD}5.1 System Prompt{Colors.RESET}")
        print("   Define the persona and global rules.")
        print("   Press Ctrl+D (Mac/Linux) or Ctrl+Z+Enter (Win) when finished.")
        print(f"{Colors.YELLOW}   " + "─" * 40 + f"{Colors.RESET}")

        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        system_prompt = "\n".join(lines).strip()

        # 5.2 User Prompt Content
        print(f"\n{Colors.BOLD}5.2 User Prompt{Colors.RESET}")
        print("   Define the specific instruction. Use {{args}} for primary input.")
        print("   Press Ctrl+D (Mac/Linux) or Ctrl+Z+Enter (Win) when finished.")
        print(f"{Colors.YELLOW}   " + "─" * 40 + f"{Colors.RESET}")

        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        user_prompt = "\n".join(lines).strip()

    if not prompt_content and not (system_prompt or user_prompt):
        print(f"\n{Colors.RED}Error: Prompt content cannot be empty. Aborting.{Colors.RESET}")
        return

    # 6. Generate File
    dest_dir = os.path.join(prompts_dir, category)
    os.makedirs(dest_dir, exist_ok=True)

    filepath = os.path.join(dest_dir, f"{name}.toml")
    if os.path.exists(filepath):
        confirm = input(
            f"\n{Colors.YELLOW}Warning: {filepath} already exists. Overwrite? (y/N): {Colors.RESET}"
        ).lower()
        if confirm != "y":
            print("Aborted.")
            return

    timestamp = datetime.date.today().isoformat()

    # Construct TOML
    toml_content = f"""description      = "{description}"
args_description = "{args_desc}"
version          = "1.0.0"
last_updated     = "{timestamp}"
tags             = {json.dumps(tags)}
"""
    if prompt_mode == 1:
        toml_content += f"""
prompt           = \"\"\"
# {name.replace("-", " ").title()}
{prompt_content}
\"\"\"
"""
    else:
        toml_content += f"""
system_prompt    = \"\"\"
{system_prompt}
\"\"\"

user_prompt      = \"\"\"
{user_prompt}
\"\"\"
"""

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(toml_content)
        print(f"\n{Colors.GREEN}✓ Created {filepath}{Colors.RESET}")
        # 7. Sync documentation
        print(f"{Colors.CYAN}Syncing documentation...{Colors.RESET}")

        subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "scripts", "sync_all_docs.py")],
            check=True,
        )
        print(f"{Colors.GREEN}✓ Documentation synchronized.{Colors.RESET}")

    except Exception as e:
        print(f"{Colors.RED}Error saving file: {e}{Colors.RESET}")

    print(
        f"\n{Colors.BOLD}Done!{Colors.RESET} You can now use your new tool with: {Colors.CYAN}pop use {name}{Colors.RESET}\n"
    )


def init_wizard():
    """Unified setup wizard to check requirements, build TUI, and install completions."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🚀 Promptbook Setup Wizard{Colors.RESET}")
    print("-------------------------------------------------------\n")

    # 1. System Check
    print(f"{Colors.BOLD}[1/4] Checking system requirements...{Colors.RESET}")

    # Python Check
    py_ver = sys.version_info
    if py_ver.major >= 3 and py_ver.minor >= 8:
        print(f"  {Colors.GREEN}✓{Colors.RESET} Python {py_ver.major}.{py_ver.minor} detected.")
    else:
        print(
            f"  {Colors.YELLOW}⚠{Colors.RESET} Warning: Python 3.8+ recommended (you have {py_ver.major}.{py_ver.minor})."
        )

    # Git Check
    if shutil.which("git"):
        print(f"  {Colors.GREEN}✓{Colors.RESET} Git detected.")
    else:
        print(
            f"  {Colors.YELLOW}⚠{Colors.RESET} Warning: Git not found. Auto-updates will be disabled."
        )

    # Clipboard Check
    os_name = platform.system()
    if os_name == "Linux":
        if shutil.which("xclip") or shutil.which("xsel"):
            print(f"  {Colors.GREEN}✓{Colors.RESET} Clipboard utility found.")
        else:
            print(
                f"  {Colors.YELLOW}⚠{Colors.RESET} Warning: No clipboard utility (xclip/xsel) found. Copying might fail."
            )
    else:
        print(f"  {Colors.GREEN}✓{Colors.RESET} {os_name} native clipboard support verified.")

    # 2. Rust/TUI Check
    print(f"\n{Colors.BOLD}[2/4] Rust TUI Explorer...{Colors.RESET}")
    cargo_path = shutil.which("cargo")
    if cargo_path:
        print(f"  {Colors.GREEN}✓{Colors.RESET} Rust (cargo) detected.")
        confirm = input(
            "  Would you like to build the Rust TUI now for faster browsing? (y/N): "
        ).lower()
        if confirm == "y":
            print(f"  {Colors.CYAN}Building TUI (this may take a minute)...{Colors.RESET}")
            try:
                tui_dir = os.path.join(BASE_DIR, "promptbook-tui")
                subprocess.run(["cargo", "build", "--release"], cwd=tui_dir, check=True)
                print(f"  {Colors.GREEN}✓{Colors.RESET} TUI built successfully.")
            except Exception as e:
                print(f"  {Colors.YELLOW}✗{Colors.RESET} TUI build failed: {e}")
    else:
        print("  - Rust not detected. Skipping TUI build.")
        print("    (You can still use the Python CLI helpers).")

    # 3. Shell Completions
    print(f"\n{Colors.BOLD}[3/4] Installing Shell Completions...{Colors.RESET}")
    shell_path = os.environ.get("SHELL", "")
    shell = ""
    if "zsh" in shell_path:
        shell = "zsh"
    elif "bash" in shell_path:
        shell = "bash"
    elif "fish" in shell_path:
        shell = "fish"

    if shell:
        print(f"  Detected {Colors.CYAN}{shell}{Colors.RESET} shell.")
        confirm = input(f"  Install completions for {shell}? (y/N): ").lower()
        if confirm == "y":
            from .cli.handlers import generate_completion_logic  # We'll need to move this

            try:
                f = io.StringIO()
                with redirect_stdout(f):
                    generate_completion_logic(shell)
                completion_script = f.getvalue()

                if shell == "zsh":
                    config_path = os.path.expanduser("~/.zshrc")
                    marker = "# promptbook completions"
                    if os.path.exists(config_path):
                        with open(config_path) as cf:
                            if marker in cf.read():
                                print(
                                    f"  {Colors.YELLOW}⚠{Colors.RESET} Completions already in .zshrc."
                                )
                            else:
                                with open(config_path, "a") as cf_a:
                                    cf_a.write(f"\n{marker}\nsource <(pop completion zsh)\n")
                                print(
                                    f"  {Colors.GREEN}✓{Colors.RESET} Added completion source to .zshrc."
                                )
                elif shell == "bash":
                    config_path = os.path.expanduser("~/.bashrc")
                    marker = "# promptbook completions"
                    with open(config_path, "a") as cf_a:
                        cf_a.write(f"\n{marker}\nsource <(pop completion bash)\n")
                    print(f"  {Colors.GREEN}✓{Colors.RESET} Added completion source to .bashrc.")
                elif shell == "fish":
                    config_dir = os.path.expanduser("~/.config/fish/completions")
                    os.makedirs(config_dir, exist_ok=True)
                    with open(os.path.join(config_dir, "pop.fish"), "w") as cf_w:
                        cf_w.write(completion_script)
                    print(
                        f"  {Colors.GREEN}✓{Colors.RESET} Created completion file in {config_dir}."
                    )
            except Exception as e:
                print(f"  {Colors.YELLOW}✗{Colors.RESET} Failed to install completions: {e}")
    else:
        print("  - Could not detect current shell. Skip completions.")

    # 4. Final Verification
    print(f"\n{Colors.BOLD}[4/4] Finishing up...{Colors.RESET}")
    print(f"  {Colors.GREEN}✓{Colors.RESET} Setup complete!")

    restart_cmd = "source ~/.zshrc"
    if shell == "bash":
        restart_cmd = "source ~/.bashrc"
    elif shell == "fish":
        restart_cmd = "exec fish"

    print("\n-------------------------------------------------------")
    print(f"{Colors.BOLD}Next Steps:{Colors.RESET}")
    print(f"  1. Restart your terminal (or run '{restart_cmd}')")
    print(f"  2. Type {Colors.CYAN}pop list{Colors.RESET} to get started.")
    print("-------------------------------------------------------\n")
