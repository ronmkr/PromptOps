import os
import sys
import re
import difflib
import tomllib
from .utils import PROMPTS_DIR, Colors, copy_to_clipboard
from .ui import format_prompt_list, format_tag_list, print_interactive_header


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
    def substitute(match):
        escape_char = match.group(1)
        var_name = match.group(2)
        if escape_char == "\\":
            return f"{{{{{var_name}}}}}"
        return variables_map.get(var_name, match.group(0))

    pattern = r"(\\)?\{\{\s*(\w+)\s*\}\}"
    return re.sub(pattern, substitute, template)


def _collect_variables(display_name, variables, data, provided_vars):
    """Interactively or via flags collects values for template variables."""
    final_vars = {}
    piped_data = sys.stdin.read().strip() if not sys.stdin.isatty() else None

    try:
        for var in variables:
            if var in provided_vars:
                final_vars[var] = provided_vars[var]
            elif piped_data is not None:
                final_vars[var] = piped_data
                piped_data = None
            else:
                label = (
                    data.get("args_description", "Input Data")
                    if var == "args"
                    else var.replace("_", " ").title()
                )
                print_interactive_header(display_name, label)
                # Use input() for a better interactive experience instead of sys.stdin.read()
                lines = []
                while True:
                    try:
                        line = input()
                        lines.append(line)
                    except (EOFError, KeyboardInterrupt):
                        break
                final_vars[var] = "\n".join(lines).strip()
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
                    f"  {i+1}) {Colors.GREEN}{(v['version_id'] or 'default'):<10}{Colors.RESET} | {v['description']}"
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
        variables = sorted(
            list(set(re.findall(r"\{\{\s*(\w+)\s*\}\}", prompt_content)))
        )

        if return_only:
            return prompt_content, variables

        final_vars = _collect_variables(display_name, variables, data, provided_vars)
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
