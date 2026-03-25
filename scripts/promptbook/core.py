import os
import sys
import re
import datetime
import json
import difflib

try:
    import tomllib
except ImportError:
    import tomli as tomllib
import subprocess
import shlex
from .utils import PROMPTS_DIR, Colors, copy_to_clipboard, AuditLogger, BASE_DIR
from .ui import format_prompt_list, format_tag_list, print_interactive_header


import shutil
import platform

if platform.system() != "Windows":
    import termios
    import tty
else:
    import msvcrt


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
        [
            d
            for d in os.listdir(prompts_dir)
            if os.path.isdir(os.path.join(prompts_dir, d))
        ]
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
    print(
        f"\n{Colors.BOLD}4. Tags{Colors.RESET} (comma-separated, e.g., engineering, security):"
    )
    tags_input = input("   Tags: ").strip()
    tags = [t.strip().lower() for t in tags_input.split(",") if t.strip()]
    if category not in tags:
        tags.append(category)
    tags = sorted(list(set(tags)))

    # 5. Prompt Content
    print(f"\n{Colors.BOLD}5. Prompt Instructions{Colors.RESET}")
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

    if not prompt_content:
        print(
            f"\n{Colors.RED}Error: Prompt content cannot be empty. Aborting.{Colors.RESET}"
        )
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

prompt           = \"\"\"
# {name.replace("-", " ").title()}
{prompt_content}
\"\"\"
"""

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(toml_content)
        print(f"\n{Colors.GREEN}✓ Created {filepath}{Colors.RESET}")
        # 7. Sync documentation
        print(f"{Colors.CYAN}Syncing documentation...{Colors.RESET}")
        # Import sync here to avoid circular dependencies if any
        import subprocess

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
        print(
            f"  {Colors.GREEN}✓{Colors.RESET} Python {py_ver.major}.{py_ver.minor} detected."
        )
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
        print(
            f"  {Colors.GREEN}✓{Colors.RESET} {os_name} native clipboard support verified."
        )

    # 2. Rust/TUI Check
    print(f"\n{Colors.BOLD}[2/4] Rust TUI Explorer...{Colors.RESET}")
    cargo_path = shutil.which("cargo")
    if cargo_path:
        print(f"  {Colors.GREEN}✓{Colors.RESET} Rust (cargo) detected.")
        confirm = input(
            "  Would you like to build the Rust TUI now for faster browsing? (y/N): "
        ).lower()
        if confirm == "y":
            print(
                f"  {Colors.CYAN}Building TUI (this may take a minute)...{Colors.RESET}"
            )
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
            from .cli import generate_completion

            try:
                # Get the completion script
                import io
                from contextlib import redirect_stdout

                f = io.StringIO()
                with redirect_stdout(f):
                    generate_completion(shell)
                completion_script = f.getvalue()

                if shell == "zsh":
                    config_path = os.path.expanduser("~/.zshrc")
                    marker = "# promptbook completions"
                    if os.path.exists(config_path):
                        with open(config_path, "r") as config_file:
                            if marker in config_file.read():
                                print(
                                    f"  {Colors.YELLOW}⚠{Colors.RESET} Completions already in .zshrc."
                                )
                            else:
                                with open(config_path, "a") as config_file:
                                    config_file.write(
                                        f"\n{marker}\nsource <(pop completion zsh)\n"
                                    )
                                print(
                                    f"  {Colors.GREEN}✓{Colors.RESET} Added completion source to .zshrc."
                                )
                elif shell == "bash":
                    config_path = os.path.expanduser("~/.bashrc")
                    marker = "# promptbook completions"
                    with open(config_path, "a") as config_file:
                        config_file.write(
                            f"\n{marker}\nsource <(pop completion bash)\n"
                        )
                    print(
                        f"  {Colors.GREEN}✓{Colors.RESET} Added completion source to .bashrc."
                    )
                elif shell == "fish":
                    config_dir = os.path.expanduser("~/.config/fish/completions")
                    os.makedirs(config_dir, exist_ok=True)
                    with open(os.path.join(config_dir, "pop.fish"), "w") as config_file:
                        config_file.write(completion_script)
                    print(
                        f"  {Colors.GREEN}✓{Colors.RESET} Created completion file in {config_dir}."
                    )
            except Exception as e:
                print(
                    f"  {Colors.YELLOW}✗{Colors.RESET} Failed to install completions: {e}"
                )
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


def get_prompts(prompts_dir=None):
    if prompts_dir is None:
        prompts_dir = PROMPTS_DIR

    groups = {}
    if not os.path.exists(prompts_dir):
        return []

    # Walk through the directory structure recursively
    for root, dirs, files in os.walk(prompts_dir):
        # Calculate relative path from prompts_dir to root to identify categories
        rel_path = os.path.relpath(root, prompts_dir)
        category = None if rel_path == "." else rel_path

        for filename in files:
            if not filename.endswith(".toml"):
                continue

            full_path = os.path.join(root, filename)

            # 1. Simple Case: prompt.toml
            # 2. Category Case: category/prompt.toml
            # 3. Versioned Case: prompt/version.toml or category/prompt/version.toml

            # If the immediate parent is NOT prompts_dir, check if the parent name matches filename (sans .toml)
            # This handles the existing versioning logic: prompts/name/version.toml
            parent_name = os.path.basename(root)
            file_base = filename.replace(".toml", "")

            if category and parent_name == file_base:
                # This is likely a versioned file (e.g. category/name/name.toml)
                # But our current structure is category/name.toml
                # Let's adjust to be robust
                name = file_base
                version_id = None
            elif category:
                # Check if this file is in a subdirectory named after it (versioning)
                # e.g., commands/prompts/testing/my-prompt/v1.toml
                # In our new structure, it's commands/prompts/testing/my-prompt.toml

                # If we are deeper than 1 level, we might have versioning
                depth = rel_path.count(os.sep) + 1
                if depth >= 2:
                    # Rel path might be "testing/my-prompt"
                    parts = rel_path.split(os.sep)
                    name = parts[-1]
                    version_id = file_base
                else:
                    # Rel path is "testing", filename is "my-prompt.toml"
                    name = file_base
                    version_id = None
            else:
                # Root level
                name = file_base
                version_id = None

            _process_prompt_file(full_path, name, version_id, groups)

    all_versions = []
    for name in sorted(groups.keys()):
        versions = groups[name]
        versions.sort(
            key=lambda x: (x["version_id"] is not None, x["version_id"] or "")
        )
        all_versions.extend(versions)

    return sorted(all_versions, key=lambda x: x["display_name"])


def _process_prompt_file(path, name, version_id, groups):
    try:
        with open(path, "rb") as file:
            data = tomllib.load(file)
            if name not in groups:
                groups[name] = []

            display_name = f"{name}:{version_id}" if version_id else name
            groups[name].append(
                {
                    "name": name,
                    "display_name": display_name,
                    "version_id": version_id,
                    "description": data.get("description", "No description provided"),
                    "version": data.get("version", "N/A"),
                    "last_updated": data.get("last_updated", "N/A"),
                    "tags": data.get("tags", []),
                    "sensitive": data.get("sensitive", False),
                    "args_description": data.get("args_description", "Input Data"),
                    "prompt": data.get("prompt", ""),
                    "path": path,
                }
            )
    except Exception:
        pass


def list_prompts(tag_filter=None, prompts_dir=None):
    prompts = get_prompts(prompts_dir)
    grouped = {}
    for p in prompts:
        if p["name"] not in grouped:
            grouped[p["name"]] = []
        grouped[p["name"]].append(p)

    if tag_filter:
        new_grouped = {}
        for name, versions in grouped.items():
            if any(tag_filter in v["tags"] for v in versions):
                new_grouped[name] = versions
        grouped = new_grouped

    if not grouped:
        print("No prompts found with criteria.")
        return

    format_prompt_list(grouped)


def list_tags(prompts_dir=None, raw=False):
    prompts = get_prompts(prompts_dir)
    tags = set()
    for p in prompts:
        tags.update(p["tags"])
    if raw:
        for tag in sorted(list(tags)):
            print(tag)
        return

    unique_names = {}
    for tag in tags:
        names = {p["name"] for p in prompts if tag in p["tags"]}
        unique_names[tag] = len(names)

    format_tag_list(unique_names)


def search_prompts(term, tag_filter=None, prompts_dir=None):
    prompts = get_prompts(prompts_dir)
    term = term.lower()

    # We search across unique prompt groups first
    seen_names = set()
    unique_prompts = []
    for p in prompts:
        if p["name"] not in seen_names:
            unique_prompts.append(p)
            seen_names.add(p["name"])

    scored_results = []
    for p in unique_prompts:
        name = p["name"].lower()
        desc = p["description"].lower()

        if term in name:
            score = 2.0 + (len(term) / len(name))
        elif term in desc:
            score = 1.5 + (len(term) / len(desc))
        else:
            scores = [
                difflib.SequenceMatcher(None, term, part).ratio()
                for part in name.split("-")
            ]
            scores.append(difflib.SequenceMatcher(None, term, name).ratio())
            score = max(scores) if scores else 0

        if score > 0.6:
            scored_results.append((score, p))

    scored_results.sort(key=lambda x: x[0], reverse=True)
    results = [item[1] for item in scored_results]

    if tag_filter:
        results = [p for p in results if tag_filter in p["tags"]]

    if not results:
        msg = f"No prompts found matching '{term}'"
        if tag_filter:
            msg += f" with tag '{tag_filter}'"
        print(msg)
        return

    # Re-group matching prompts to show all versions
    all_prompts = get_prompts(prompts_dir)
    matching_names = {p["name"] for p in results}
    grouped = {}
    for p in all_prompts:
        if p["name"] in matching_names:
            if p["name"] not in grouped:
                grouped[p["name"]] = []
            grouped[p["name"]].append(p)

    format_prompt_list(grouped)


def hydrate_prompt(template, variables_map):
    def handle_conditionals(text):
        cond_pattern = r"<if\s+(\w+)\s*=\s*\"([^\"]+)\"\s*>(.*?)</if>"

        def cond_substitute(match):
            key, expected_val, content = match.group(1), match.group(2), match.group(3)
            actual_val = variables_map.get(key, "").strip().lower()
            return content if actual_val == expected_val.strip().lower() else ""

        return re.sub(cond_pattern, cond_substitute, text, flags=re.DOTALL)

    template = handle_conditionals(template)

    # 1. Find all shell blocks {{$( ... )}} using balanced braces to handle nesting
    def find_shell_ranges(text):
        ranges = []
        stack = 0
        start = -1
        i = 0
        while i < len(text):
            if text[i : i + 2] == "{{":
                # Check if escaped
                if i > 0 and text[i - 1] == "\\":
                    i += 2
                    continue
                # Check if it's a shell block or we're already inside one
                if text[i : i + 4] == "{{$(":
                    if stack == 0:
                        start = i
                    stack += 1
                    i += 4
                    continue
                if stack > 0:
                    stack += 1
                i += 2
            elif text[i : i + 2] == "}}":
                if stack > 0:
                    stack -= 1
                    if stack == 0:
                        ranges.append((start, i + 2))
                i += 2
            else:
                i += 1
        return ranges

    shell_ranges = find_shell_ranges(template)

    # 2. Tokenize shell blocks to protect them during standard variable resolution
    tokenized_template = ""
    last_pos = 0
    token_map = {}
    for i, (s, e) in enumerate(shell_ranges):
        token = f"__PB_SHELL_{i}__"
        token_map[token] = template[s + 2 : e - 2]  # Content inside {{ }}
        tokenized_template += template[last_pos:s] + token
        last_pos = e
    tokenized_template += template[last_pos:]

    # 3. Resolve standard variables and env vars in the protected template
    # Regex for standard blocks: no {{ or }} inside
    std_pattern = r"(\\)?\{\{\s*([^{}]+?)\s*\}\}"

    def resolve_std_block(m):
        escape_char, content = m.group(1), m.group(2).strip()
        if escape_char == "\\":
            return f"{{{{{content}}}}}"

        if content.startswith("env."):
            return os.environ.get(
                content[4:].strip(), f"[Env var {content[4:].strip()} not found]"
            )

        return variables_map.get(content, m.group(0))

    # Single pass for standard variables to respect escaping rules
    hydrated_text = re.sub(std_pattern, resolve_std_block, tokenized_template)

    # 4. Resolve shell blocks and replace tokens
    for token, shell_content in token_map.items():
        # shell_content is e.g. "$(echo {{args}})"
        inner_cmd = shell_content[2:-1].strip()

        # Resolve any {{var}} inside the shell command WITH quoting for security
        def quote_fn(mm):
            v_name = mm.group(1).strip()
            if v_name.startswith("env."):
                val = os.environ.get(v_name[4:].strip(), "")
            else:
                val = variables_map.get(v_name, "")
            return shlex.quote(val)

        safe_cmd = re.sub(r"\{\{\s*(.*?)\s*\}\}", quote_fn, inner_cmd)

        try:
            res = subprocess.check_output(
                safe_cmd, shell=True, stderr=subprocess.STDOUT, text=True
            ).strip()
        except Exception as e:
            res = f"[Error: {str(e)}]"

        hydrated_text = hydrated_text.replace(token, res)

    return hydrated_text


def _get_char():
    """Reads a single character from stdin in raw mode."""
    if platform.system() != "Windows":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    else:
        return msvcrt.getch().decode("utf-8", "ignore")


def _collect_variables(display_name, variables, data, provided_vars):
    """Interactively or via flags collects values for template variables."""
    final_vars = {}
    piped_data = sys.stdin.read().strip() if not sys.stdin.isatty() else None

    try:
        # Recursively find all standard user variables
        user_vars_set = set()

        def find_vars(text):
            # Use greedy to find outer blocks, then look inside
            found = re.findall(r"\{\{\s*(.*?)\s*\}\}", text)
            for v in found:
                v = v.strip()
                if v.startswith("$(") and v.endswith(")"):
                    find_vars(v[2:-1])
                elif v.startswith("env."):
                    pass
                else:
                    if "{{" not in v:
                        user_vars_set.add(v)
                    else:
                        find_vars(v)

        for v in variables:
            v = v.strip()
            if v.startswith("$(") and v.endswith(")"):
                find_vars(v[2:-1])
            elif v.startswith("env."):
                pass
            else:
                if "{{" not in v:
                    user_vars_set.add(v)
                else:
                    find_vars(v)

        user_vars = sorted(list(user_vars_set))
        i = 0
        while i < len(user_vars):
            var = user_vars[i]

            if var in provided_vars:
                final_vars[var] = provided_vars[var]
                i += 1
            elif piped_data is not None:
                final_vars[var] = piped_data
                piped_data = None
                i += 1
            else:
                label = (
                    data.get("args_description", "Input Data")
                    if var == "args"
                    else var.replace("_", " ").title()
                )
                print_interactive_header(display_name, label)

                # Multi-line input handler with Ctrl+G (finish) and Ctrl+B (back)
                lines = []
                current_line = ""

                sys.stderr.write(
                    f" {Colors.BOLD}[Input mode: Type normally. Ctrl+G: Finish, Ctrl+B: Back, Ctrl+C: Cancel]{Colors.RESET}\n"
                )
                sys.stderr.write(f" {Colors.YELLOW}> {Colors.RESET}")
                sys.stderr.flush()

                should_go_back = False
                while True:
                    ch = _get_char()

                    if ch == "\x03":  # Ctrl+C
                        raise KeyboardInterrupt
                    elif ch in ("\x07", "\x04"):  # Ctrl+G or Ctrl+D
                        lines.append(current_line)
                        break
                    elif ch == "\x02":  # Ctrl+B
                        should_go_back = True
                        break
                    elif ch in ("\r", "\n"):
                        sys.stderr.write("\n")
                        sys.stderr.write(f" {Colors.YELLOW}> {Colors.RESET}")
                        sys.stderr.flush()
                        lines.append(current_line)
                        current_line = ""
                    elif ch in ("\x7f", "\x08"):  # Backspace
                        if len(current_line) > 0:
                            current_line = current_line[:-1]
                            sys.stderr.write("\b \b")
                            sys.stderr.flush()
                    else:
                        current_line += ch
                        sys.stderr.write(ch)
                        sys.stderr.flush()

                if should_go_back:
                    if i > 0:
                        i -= 1
                        # Clear current var if moving back
                        if user_vars[i] in final_vars:
                            del final_vars[user_vars[i]]
                        print(
                            f"\n{Colors.CYAN} [Back] Returning to previous variable...{Colors.RESET}",
                            file=sys.stderr,
                        )
                        continue
                    else:
                        print(
                            f"\n{Colors.YELLOW} [Info] Already at first variable.{Colors.RESET}",
                            file=sys.stderr,
                        )
                        continue

                final_vars[var] = "\n".join(lines).strip()
                i += 1

                print(
                    "\n"
                    + f"{Colors.BOLD}{Colors.YELLOW}"
                    + "─" * 70
                    + f"{Colors.RESET}"
                    + "\n",
                    file=sys.stderr,
                )
    except KeyboardInterrupt:
        print(
            f"\n\n{Colors.YELLOW}Operation cancelled by user.{Colors.RESET}",
            file=sys.stderr,
        )
        sys.exit(0)

    return final_vars


def _confirm_sensitive_copy(name):
    """Asks for confirmation before copying sensitive data to clipboard."""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  SECURITY WARNING:{Colors.RESET}")
    print(
        f"{Colors.YELLOW}This prompt is marked as SENSITIVE and will be copied to your clipboard.{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}Proceed with caution if it contains secrets or proprietary data.{Colors.RESET}"
    )
    try:
        confirm = input("\nCopy to clipboard? (y/N): ").lower()
        if confirm != "y":
            print(
                f" {Colors.YELLOW}[Skip] Clipboard copy cancelled.{Colors.RESET}",
                file=sys.stderr,
            )
            return False
        return True
    except (KeyboardInterrupt, EOFError):
        print(
            f"\n {Colors.YELLOW}[Skip] Clipboard copy cancelled.{Colors.RESET}",
            file=sys.stderr,
        )
        return False


def use_prompt(
    name,
    provided_vars=None,
    prompts_dir=None,
    return_only=False,
    version_hint=None,
    no_copy=False,
    auto_confirm=False,
    mask=False,
):
    if provided_vars is None:
        provided_vars = {}
    all_prompts = get_prompts(prompts_dir)
    versions = [p for p in all_prompts if p["name"] == name]

    if not versions:
        print(f"Error: Prompt '{name}' not found.", file=sys.stderr)
        sys.exit(1)

    selected = None
    if version_hint:
        selected = next((v for v in versions if v["version_id"] == version_hint), None)
        if not selected:
            print(
                f"Error: Version '{version_hint}' for prompt '{name}' not found.",
                file=sys.stderr,
            )
            sys.exit(1)
    elif len(versions) == 1:
        selected = versions[0]
    else:
        if not sys.stdin.isatty():
            selected = versions[0]
        else:
            print(f"\n{Colors.BOLD}Multiple versions found for '{name}':{Colors.RESET}")
            for i, v in enumerate(versions):
                print(
                    f"  {i + 1}) {Colors.GREEN}{(v['version_id'] or 'default'):<10}{Colors.RESET} | {v['description']}"
                )
            try:
                choice = input(f"\nSelect version (1-{len(versions)}): ")
                selected = versions[int(choice) - 1]
            except (ValueError, IndexError, KeyboardInterrupt, EOFError):
                print("\nCancelled.", file=sys.stderr)
                sys.exit(1)

    with open(selected["path"], "rb") as f:
        data = tomllib.load(f)
        prompt_content = data.get("prompt", "")
        is_sensitive = selected.get("sensitive", False)

        if not prompt_content:
            print(f"Error: Prompt '{name}' has no content.", file=sys.stderr)
            sys.exit(1)

        display_name = (
            f"{name}:{selected['version_id']}" if selected["version_id"] else name
        )

        # Recursive variable discovery
        variables_set = set()

        def discover_vars(text):
            # Find innermost blocks first (no {{ or }} inside)
            innermost = re.findall(r"\{\{\s*([^{}]+?)\s*\}\}", text)
            for v in innermost:
                v = v.strip()
                variables_set.add(v)

            # Now replace innermost blocks with placeholders and recurse to find outer blocks
            if innermost:
                # Simple placeholder replacement to avoid infinite recursion
                remaining_text = re.sub(r"\{\{\s*[^{}]+?\s*\}\}", "VAR", text)
                if remaining_text != text:
                    # Also need to capture the outer block itself if it was a shell block
                    # Let's use a greedy regex for outer blocks now that we know we have them
                    outer_blocks = re.findall(r"\{\{\s*(.+)\s*\}\}", text)
                    for ob in outer_blocks:
                        variables_set.add(ob.strip())
                        # If outer block is shell, recurse on its content
                        if ob.strip().startswith("$(") and ob.strip().endswith(")"):
                            discover_vars(ob.strip()[2:-1])

                    discover_vars(remaining_text)

        discover_vars(prompt_content)
        variables = sorted(list(variables_set))

        if return_only:
            return prompt_content, variables

        final_vars = _collect_variables(display_name, variables, data, provided_vars)

        # PII Masking (GDPR/Compliance)
        if mask:
            try:
                import scrubadub

                for var_name, var_val in final_vars.items():
                    if isinstance(var_val, str):
                        final_vars[var_name] = scrubadub.clean(var_val)
            except ImportError:
                print(
                    f"{Colors.YELLOW}Warning: 'scrubadub' not installed. Masking skipped.{Colors.RESET}",
                    file=sys.stderr,
                )

        # Log sensitive prompt execution
        if is_sensitive:
            AuditLogger.log(name, selected.get("version_id"), final_vars)

        prompt_content = hydrate_prompt(prompt_content, final_vars)

        do_copy = not no_copy
        if do_copy and is_sensitive and not auto_confirm:
            do_copy = _confirm_sensitive_copy(name)

        if do_copy:
            if copy_to_clipboard(prompt_content):
                print(
                    f" {Colors.GREEN}[Done] Prompt copied to clipboard!{Colors.RESET}",
                    file=sys.stderr,
                )

        print(prompt_content)
