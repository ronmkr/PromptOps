import os
import sys
import glob
import tomllib
import argparse
import json
import difflib
import re
import subprocess
import platform
# ANSI Colors for better UX
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
# Get the directory where the script/module is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_DIR = os.path.join(BASE_DIR, "commands", "prompts")
def get_prompts(prompts_dir=None):
    if prompts_dir is None:
        prompts_dir = PROMPTS_DIR
    
    # Map: name -> list of versions
    groups = {}
    
    if not os.path.exists(prompts_dir):
        return []

    # 1. Look for flat files at root
    for entry in os.listdir(prompts_dir):
        full_path = os.path.join(prompts_dir, entry)
        if os.path.isfile(full_path) and entry.endswith(".toml"):
            name = entry.replace(".toml", "")
            _process_prompt_file(full_path, name, None, groups)
        elif os.path.isdir(full_path):
            # 2. Look for versioned files in subdirectories
            name = entry
            for sub_entry in sorted(os.listdir(full_path)):
                if sub_entry.endswith(".toml"):
                    version_id = sub_entry.replace(".toml", "")
                    _process_prompt_file(os.path.join(full_path, sub_entry), name, version_id, groups)

    # Flatten into a list of all versions
    all_versions = []
    for name in sorted(groups.keys()):
        versions = groups[name]
        # Sort versions: None (default) first, then by ID
        versions.sort(key=lambda x: (x["version_id"] is not None, x["version_id"] or ""))
        all_versions.extend(versions)
        
    return all_versions

def _process_prompt_file(path, name, version_id, groups):
    try:
        with open(path, "rb") as file:
            data = tomllib.load(file)
            if name not in groups:
                groups[name] = []
            
            groups[name].append({
                "name": name,
                "version_id": version_id, # e.g. "v1" or None
                "description": data.get("description", "No description provided"),
                "version": data.get("version", "N/A"),
                "tags": data.get("tags", []),
                "args_description": data.get("args_description", "Input Data"),
                "prompt": data.get("prompt", ""),
                "path": path
            })
    except Exception:
        pass

def list_prompts(tag_filter=None, prompts_dir=None):
    prompts = get_prompts(prompts_dir)
    
    # Group by name for display
    grouped = {}
    for p in prompts:
        if p["name"] not in grouped:
            grouped[p["name"]] = []
        grouped[p["name"]].append(p)
    
    # Filter groups by tag
    if tag_filter:
        new_grouped = {}
        for name, versions in grouped.items():
            if any(tag_filter in v["tags"] for v in versions):
                new_grouped[name] = versions
        grouped = new_grouped

    if not grouped:
        print(f"No prompts found with criteria.")
        return

    print(f"{Colors.BOLD}{Colors.CYAN}{'PROMPT NAME':<35} | {'DESCRIPTION'}{Colors.RESET}")
    print("-" * 100)
    for name in sorted(grouped.keys()):
        versions = grouped[name]
        # Collect version identifiers (v1, v2...)
        v_ids = [v["version_id"] for v in versions if v["version_id"]]
        v_str = f" [{', '.join(v_ids)}]" if v_ids else ""
        
        # Use first version's description as representative
        desc = versions[0]["description"]
        print(f"{Colors.GREEN}{name + v_str:<35}{Colors.RESET} | {desc}")

def list_tags(prompts_dir=None, raw=False):
    prompts = get_prompts(prompts_dir)
    tags = set()
    for p in prompts:
        tags.update(p["tags"])
    if raw:
        for tag in sorted(list(tags)):
            print(tag)
        return
    print(f"{Colors.BOLD}{Colors.CYAN}Available Tags:{Colors.RESET}")
    print("-" * 20)
    
    # Unique names count per tag
    unique_names = {}
    for tag in tags:
        names = {p["name"] for p in prompts if tag in p["tags"]}
        unique_names[tag] = len(names)

    for tag in sorted(list(tags)):
        print(f"{Colors.YELLOW}{tag:<20}{Colors.RESET} ({unique_names[tag]} prompts)")

def list_names(prompts_dir=None):
    """Hidden helper for shell completion."""
    prompts = get_prompts(prompts_dir)
    # Return unique prompt names + name:version shorthand
    names = set()
    for p in prompts:
        names.add(p["name"])
        if p["version_id"]:
            names.add(f"{p['name']}:{p['version_id']}")
    for name in sorted(list(names)):
        print(name)
def generate_completion(shell):
    """Generates shell completion scripts for Zsh, Bash, and Fish."""
    if shell == "zsh":
        print("""#compdef pop promptops
_pop() {
    local -a commands
    commands=(
        'list:List all available prompts'
        'tags:List all unique tags'
        'search:Search prompts'
        'use:Use a prompt'
        'completion:Generate shell completion'
    )
    if (( CURRENT == 2 )); then
        _describe -t commands 'pop commands' commands
    elif (( CURRENT == 3 )); then
        case $words[2] in
            use)
                local -a prompts
                prompts=($($words[1] _list_names))
                _describe -t prompts 'available prompts' prompts
                ;;
            list|search)
                if [[ $words[CURRENT-1] == "--tag" ]]; then
                    local -a tags
                    tags=($($words[1] _list_tags))
                    _describe -t tags 'available tags' tags
                else
                    _arguments '--tag[Filter by tag]'
                fi
                ;;
            completion)
                _describe -t shells 'shells' "(zsh bash fish)"
                ;;
        esac
    fi
}
_pop "$@"
""")
    elif shell == "bash":
        print("""_pop_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="list tags search use completion"
    case "${prev}" in
        use)
            local prompts=$(pop _list_names)
            COMPREPLY=( $(compgen -W "${prompts}" -- ${cur}) )
            return 0
            ;;
        list|search)
            COMPREPLY=( $(compgen -W "--tag" -- ${cur}) )
            return 0
            ;;
        completion)
            COMPREPLY=( $(compgen -W "zsh bash fish" -- ${cur}) )
            return 0
            ;;
        --tag)
            local tags=$(pop _list_tags)
            COMPREPLY=( $(compgen -W "${tags}" -- ${cur}) )
            return 0
            ;;
    esac
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
}
complete -F _pop_completion pop promptops
""")
    elif shell == "fish":
        print("""# pop fish completion
complete -c pop -f
complete -c pop -n " __fish_use_subcommand" -a list -d "List all available prompts"
complete -c pop -n " __fish_use_subcommand" -a tags -d "List all unique tags"
complete -c pop -n " __fish_use_subcommand" -a search -d "Search prompts"
complete -c pop -n " __fish_use_subcommand" -a use -d "Use a prompt"
complete -c pop -n " __fish_use_subcommand" -a completion -d "Generate shell completion"
complete -c pop -n "__fish_seen_subcommand_from use" -a "(pop _list_names)"
complete -c pop -n "__fish_seen_subcommand_from list search" -l tag -a "(pop _list_tags)"
complete -c pop -n "__fish_seen_subcommand_from completion" -a "zsh bash fish"
""")
def copy_to_clipboard(text):
    """Zero-dependency clipboard copy using native OS commands."""
    try:
        os_name = platform.system()
        if os_name == "Darwin": # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        elif os_name == "Linux":
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(input=text.encode('utf-8'))
            except FileNotFoundError:
                process = subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE)
                process.communicate(input=text.encode('utf-8'))
        elif os_name == "Windows":
            process = subprocess.Popen(['clip.exe'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        return False
def search_prompts(term, tag_filter=None, prompts_dir=None):
    prompts = get_prompts(prompts_dir)
    term = term.lower()
    scored_results = []
    for p in prompts:
        name = p["name"].lower()
        desc = p["description"].lower()
        name_parts = name.split("-")
        desc_words = desc.split()
        if term in name:
            score = 2.0 + (len(term) / len(name))
        elif term in desc:
            score = 1.5 + (len(term) / len(desc))
        else:
            scores = []
            for part in name_parts:
                scores.append(difflib.SequenceMatcher(None, term, part).ratio())
            for word in desc_words:
                if len(word) > 3:
                    scores.append(difflib.SequenceMatcher(None, term, word).ratio())
            scores.append(difflib.SequenceMatcher(None, term, name).ratio())
            scores.append(difflib.SequenceMatcher(None, term, desc).ratio())
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
    print(f"Found {len(results)} matches for '{term}':\n")
    print(f"{Colors.BOLD}{Colors.CYAN}{'PROMPT NAME':<35} | {'DESCRIPTION'}{Colors.RESET}")
    print("-" * 100)
    for p in results[:15]:
        print(f"{Colors.GREEN}{p['name']:<35}{Colors.RESET} | {p['description']}")
def hydrate_prompt(template, variables_map):
    r"""
    Hydrates a prompt template with provided variables.
    Supports escaping literal placeholders with a backslash: \{{var}} -> {{var}}
    Supports whitespace inside braces: {{ var }} -> value
    """
    def substitute(match):
        escape_char = match.group(1)
        var_name = match.group(2)
        
        if escape_char == '\\':
            # This was escaped, return the literal placeholder without the backslash
            return f"{{{{{var_name}}}}}"
        
        # Return the variable value if it exists, otherwise leave the placeholder alone
        return variables_map.get(var_name, match.group(0))

    # Pattern matches optional backslash + {{ variable_name }}
    # group 1: optional backslash
    # group 2: variable name (stripped of whitespace)
    pattern = r'(\\)?\{\{\s*(\w+)\s*\}\}'
    return re.sub(pattern, substitute, template)

def use_prompt(name, provided_vars=None, prompts_dir=None, return_only=False, version_hint=None):
    if provided_vars is None:
        provided_vars = {}
    
    # Find available versions
    all_prompts = get_prompts(prompts_dir)
    versions = [p for p in all_prompts if p["name"] == name]
    
    if not versions:
        print(f"Error: Prompt '{name}' not found.", file=sys.stderr)
        sys.exit(1)
        
    selected = None
    if version_hint:
        selected = next((v for v in versions if v["version_id"] == version_hint), None)
        if not selected:
            print(f"Error: Version '{version_hint}' for prompt '{name}' not found.", file=sys.stderr)
            avail = [v["version_id"] or "default" for v in versions]
            print(f"Available versions: {', '.join(avail)}", file=sys.stderr)
            sys.exit(1)
    elif len(versions) == 1:
        selected = versions[0]
    else:
        if not sys.stdin.isatty():
            # Non-interactive: default to first one
            selected = versions[0]
        else:
            print(f"\n{Colors.BOLD}Multiple versions found for '{name}':{Colors.RESET}")
            for i, v in enumerate(versions):
                v_id = v["version_id"] or "default"
                print(f"  {i+1}) {Colors.GREEN}{v_id:<10}{Colors.RESET} | {v['description']}")
            
            try:
                choice = input(f"\nSelect version (1-{len(versions)}): ")
                idx = int(choice) - 1
                if 0 <= idx < len(versions):
                    selected = versions[idx]
                else:
                    print("Invalid selection.", file=sys.stderr)
                    sys.exit(1)
            except (ValueError, KeyboardInterrupt, EOFError):
                print("\nCancelled.", file=sys.stderr)
                sys.exit(1)

    filepath = selected["path"]
    try:
        with open(filepath, "rb") as f:
            data = tomllib.load(f)
            prompt_content = data.get("prompt", "")
            if not prompt_content:
                print(f"Error: Prompt '{name}' has no content.", file=sys.stderr)
                sys.exit(1)
            
            display_name = f"{name}:{selected['version_id']}" if selected["version_id"] else name
            args_desc = data.get("args_description", "Input Data")
            variables = sorted(list(set(re.findall(r"\{\{(\w+)\}\}", prompt_content))))
            if return_only:
                return prompt_content, variables
            final_vars = {}
            piped_data = None
            if not sys.stdin.isatty():
                piped_data = sys.stdin.read().strip()

            try:
                for var in variables:
                    if var in provided_vars:
                        final_vars[var] = provided_vars[var]
                    elif piped_data is not None:
                        # Use piped data for the first missing variable
                        final_vars[var] = piped_data
                        piped_data = None # Only use it once
                    else:
                        label = args_desc if var == "args" else var.replace("_", " ").title()

                        print("\n" + f"{Colors.BOLD}{Colors.YELLOW}" + "╭" + "─"*68 + "╮" + f"{Colors.RESET}", file=sys.stderr)
                        print(f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.CYAN}PromptOps Interactive: {Colors.BOLD}{display_name}{Colors.RESET}", file=sys.stderr)
                        print(f"{Colors.BOLD}{Colors.YELLOW}├" + "─"*68 + "┤" + f"{Colors.RESET}", file=sys.stderr)
                        print(f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.BOLD}Required:{Colors.RESET} {Colors.GREEN}{label}{Colors.RESET}", file=sys.stderr)
                        print(f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.BOLD}Finish:{Colors.RESET}   Press {Colors.BOLD}Ctrl+D{Colors.RESET} (Mac/Linux) or {Colors.BOLD}Ctrl+Z+Enter{Colors.RESET} (Win)", file=sys.stderr)
                        print(f"{Colors.BOLD}{Colors.YELLOW}╰" + "─"*68 + "╯" + f"{Colors.RESET}", file=sys.stderr)
                        print(f" {Colors.BOLD}[Paste {label} below]{Colors.RESET}\n", file=sys.stderr)

                        try:
                            val = sys.stdin.read().strip()
                            if not val:
                                print(f"\n {Colors.YELLOW}Warning: No input provided for {label}.{Colors.RESET}", file=sys.stderr)
                            final_vars[var] = val
                            print("\n" + f"{Colors.BOLD}{Colors.YELLOW}" + "─"*70 + f"{Colors.RESET}" + "\n", file=sys.stderr)
                        except EOFError:
                            print(f"\n{Colors.YELLOW}Error: Input interrupted.{Colors.RESET}", file=sys.stderr)
                            sys.exit(1)
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Operation cancelled by user.{Colors.RESET}", file=sys.stderr)
                sys.exit(0)

            # Substitute variables

            prompt_content = hydrate_prompt(prompt_content, final_vars)

            if copy_to_clipboard(prompt_content):
                print(f" {Colors.GREEN}[Done] Prompt copied to clipboard!{Colors.RESET}", file=sys.stderr)
            print(prompt_content)
    except Exception as e:
        print(f"Error reading prompt: {e}", file=sys.stderr)
        sys.exit(1)
def print_help():
    header_line = "+" + "-"*68 + "+"
    help_text = f"""
{Colors.BOLD}{Colors.YELLOW}{header_line}
| [ PromptOps: Your AI Command Center ]                              |
{header_line}{Colors.RESET}
{Colors.BOLD}TL;DR:{Colors.RESET}
  Find and use the best AI prompts directly from your terminal.
  Automatically copies results to your clipboard for easy pasting.
{Colors.BOLD}BEGINNER GUIDE:{Colors.RESET}
  - {Colors.GREEN}pop list{Colors.RESET}          : See everything available.
  - {Colors.GREEN}pop search "term"{Colors.RESET} : Find tools for a specific task.
  - {Colors.GREEN}pop use <tool>{Colors.RESET}    : Run it! (We'll ask for your input).
{Colors.BOLD}POPULAR EXAMPLES:{Colors.RESET}
  {Colors.CYAN}pop use suggest-fixes{Colors.RESET}      # Get code improvements
  {Colors.CYAN}pop use dockerfile-generator{Colors.RESET} # Containerize your app
  {Colors.CYAN}pop use design-api{Colors.RESET}        # Architect a new API
{Colors.BOLD}POWER USER TIPS:{Colors.RESET}
  {Colors.YELLOW}pop use suggest-fixes --args @main.py{Colors.RESET} # Inject a file
  {Colors.YELLOW}pop use explain-code | claude{Colors.RESET}         # Pipe to Claude Code
{Colors.BOLD}{Colors.YELLOW}{"-" * 70}{Colors.RESET}
    """
    print(help_text, file=sys.stderr)
import glob

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
    # Use glob to find matches (supports recursive if ** is used)
    matches = glob.glob(pattern, recursive=True)
    
    if not matches:
        if any(char in pattern for char in "*?[]"):
            print(f"{Colors.YELLOW}Warning: No files matched glob '{pattern}'. Using raw string.{Colors.RESET}", file=sys.stderr)
        elif not os.path.exists(pattern):
            print(f"{Colors.YELLOW}Warning: File {pattern} not found. Using raw string.{Colors.RESET}", file=sys.stderr)
        return val

    contents = []
    # Filter to only files and sort for deterministic output
    files = sorted([m for m in matches if os.path.isfile(m)])
    
    if not files:
        return val

    for f_path in files:
        try:
            with open(f_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if len(files) > 1:
                    contents.append(f"--- File: {f_path} ---\n{content}")
                else:
                    contents.append(content)
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Could not read file {f_path} ({e}).{Colors.RESET}", file=sys.stderr)
    
    return "\n\n".join(contents).strip()

def main():
    if len(sys.argv) == 1:
        print_help()
        sys.argv.append("-h")
    parser = argparse.ArgumentParser(description="PromptOps CLI Helper", add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    if len(sys.argv) > 1 and (sys.argv[1] in ("-h", "--help")):
        print_help()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List all available prompts").add_argument("--tag", help="Filter by tag")
    subparsers.add_parser("tags", help="List all unique tags in the library")
    search_p = subparsers.add_parser("search", help="Search for prompts by name or description")
    search_p.add_argument("term", help="Search term")
    search_p.add_argument("--tag", help="Filter search results by tag")
    use_p = subparsers.add_parser("use", help="Output prompt content for use in other tools")
    use_p.add_argument("name", help="Name of the prompt to use")
    comp_p = subparsers.add_parser("completion", help="Generate shell completion script")
    comp_p.add_argument("shell", choices=["zsh", "bash", "fish"], help="Target shell")
    subparsers.add_parser("_list_names", add_help=False)
    subparsers.add_parser("_list_tags", add_help=False)
    if len(sys.argv) > 1 and sys.argv[1] == "use":
        args, unknown = parser.parse_known_args()
        
        target_name = args.name
        version_hint = None
        if ":" in target_name:
            parts = target_name.split(":", 1)
            target_name = parts[0]
            version_hint = parts[1]

        provided_vars = {}
        for i in range(0, len(unknown), 2):
            if unknown[i].startswith("--") and i + 1 < len(unknown):
                var_name = unknown[i][2:]
                val = resolve_file_injection(unknown[i+1])
                provided_vars[var_name] = val
        use_prompt(target_name, provided_vars, version_hint=version_hint)
    else:
        args = parser.parse_args()
        if args.command == "list":
            list_prompts(args.tag)
        elif args.command == "tags":
            list_tags()
        elif args.command == "search":
            search_prompts(args.term, args.tag)
        elif args.command == "completion":
            generate_completion(args.shell)
        elif args.command == "_list_names":
            list_names()
        elif args.command == "_list_tags":
            list_tags(raw=True)
        elif args.command is None:
            parser.print_help()
if __name__ == "__main__":
    main()
