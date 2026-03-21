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

    prompts = []
    if not os.path.exists(prompts_dir):
        return prompts

    files = glob.glob(os.path.join(prompts_dir, "*.toml"))
    for f in files:
        name = os.path.basename(f).replace(".toml", "")
        try:
            with open(f, "rb") as file:
                data = tomllib.load(file)
                prompts.append({
                    "name": name,
                    "description": data.get("description", "No description provided"),
                    "version": data.get("version", "N/A"),
                    "tags": data.get("tags", []),
                    "prompt": data.get("prompt", "")
                })
        except Exception:
            continue
    return sorted(prompts, key=lambda x: x["name"])

def list_prompts(tag_filter=None, prompts_dir=None):
    prompts = get_prompts(prompts_dir)
    if tag_filter:
        prompts = [p for p in prompts if tag_filter in p["tags"]]
        if not prompts:
            print(f"No prompts found with tag '{tag_filter}'")
            return

    print(f"{Colors.BOLD}{Colors.CYAN}{'PROMPT NAME':<35} | {'DESCRIPTION'}{Colors.RESET}")
    print("-" * 100)
    for p in prompts:
        print(f"{Colors.GREEN}{p['name']:<35}{Colors.RESET} | {p['description']}")

def list_tags(prompts_dir=None):
    prompts = get_prompts(prompts_dir)
    tags = set()
    for p in prompts:
        tags.update(p["tags"])

    print(f"{Colors.BOLD}{Colors.CYAN}Available Tags:{Colors.RESET}")
    print("-" * 20)
    for tag in sorted(list(tags)):
        count = len([p for p in prompts if tag in p["tags"]])
        print(f"{Colors.YELLOW}{tag:<20}{Colors.RESET} ({count} prompts)")

def copy_to_clipboard(text):
    """Zero-dependency clipboard copy using native OS commands."""
    try:
        os_name = platform.system()
        if os_name == "Darwin": # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        elif os_name == "Linux":
            # Try xclip then xsel
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
        # Fail silently if no clipboard tool is found
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

        # 1. Direct substring match (highest priority)
        if term in name:
            score = 2.0 + (len(term) / len(name))
        elif term in desc:
            score = 1.5 + (len(term) / len(desc))
        else:
            # 2. Fuzzy match against words and whole strings
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
def use_prompt(name, provided_vars=None, prompts_dir=None, return_only=False):
    if provided_vars is None:
        provided_vars = {}

    if prompts_dir is None:
        prompts_dir = PROMPTS_DIR

    filepath = os.path.join(prompts_dir, f"{name}.toml")
    if not os.path.exists(filepath):
        print(f"Error: Prompt '{name}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filepath, "rb") as f:
            data = tomllib.load(f)
            prompt_content = data.get("prompt", "")
            if not prompt_content:
                print(f"Error: Prompt '{name}' has no content.", file=sys.stderr)
                sys.exit(1)

            # Get variable descriptions from metadata
            args_desc = data.get("args_description", "Input Data")

            variables = sorted(list(set(re.findall(r"\{\{(\w+)\}\}", prompt_content))))

            # If return_only is true, we just return the raw template and variables
            # Let the caller handle the injection
            if return_only:
                return prompt_content, variables

            final_vars = {}
            for var in variables:
                if var in provided_vars:
                    final_vars[var] = provided_vars[var]
                else:
                    # Interactive mode UX - High Quality Redesign
                    label = args_desc if var == "args" else var.replace("_", " ").title()

                    print("\n" + f"{Colors.BOLD}{Colors.YELLOW}" + "╭" + "─"*68 + "╮" + f"{Colors.RESET}", file=sys.stderr)
                    print(f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.CYAN}✨ PromptOps Interactive: {Colors.BOLD}{name}{Colors.RESET}", file=sys.stderr)
                    print(f"{Colors.BOLD}{Colors.YELLOW}├" + "─"*68 + "┤" + f"{Colors.RESET}", file=sys.stderr)
                    print(f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.BOLD}Required:{Colors.RESET} {Colors.GREEN}{label}{Colors.RESET}", file=sys.stderr)
                    print(f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.BOLD}Finish:{Colors.RESET}   Press {Colors.BOLD}Ctrl+D{Colors.RESET} (Mac/Linux) or {Colors.BOLD}Ctrl+Z+Enter{Colors.RESET} (Win)", file=sys.stderr)
                    print(f"{Colors.BOLD}{Colors.YELLOW}╰" + "─"*68 + "╯" + f"{Colors.RESET}", file=sys.stderr)
                    print(f" {Colors.BOLD}[Paste {label} below]{Colors.RESET} ↓\n", file=sys.stderr)

                    try:
                        val = sys.stdin.read().strip()
                        if not val:
                            print(f"\n {Colors.YELLOW}Warning: No input provided for {label}.{Colors.RESET}", file=sys.stderr)
                        final_vars[var] = val
                        print("\n" + f"{Colors.BOLD}{Colors.YELLOW}" + "─"*70 + f"{Colors.RESET}" + "\n", file=sys.stderr)
                    except EOFError:
                        print(f"\n{Colors.YELLOW}Error: Input interrupted.{Colors.RESET}", file=sys.stderr)
                        sys.exit(1)

            # Substitute variables

            for var, val in final_vars.items():
                prompt_content = prompt_content.replace(f"{{{{{var}}}}}", val)

            # Copy to clipboard automatically for better web/chat app UX
            if copy_to_clipboard(prompt_content):
                print(f" {Colors.GREEN}📋 Prompt copied to clipboard!{Colors.RESET}", file=sys.stderr)

            print(prompt_content)

    except Exception as e:
        print(f"Error reading prompt: {e}", file=sys.stderr)
        sys.exit(1)
def main():
    if len(sys.argv) == 1:
        sys.argv.append("-h")
        
    parser = argparse.ArgumentParser(description="PromptOps CLI Helper")
    subparsers = parser.add_subparsers(dest="command")
    # list
    list_parser = subparsers.add_parser("list", help="List all available prompts")
    list_parser.add_argument("--tag", help="Filter by tag")
    # tags
    subparsers.add_parser("tags", help="List all unique tags in the library")
    # search
    search_parser = subparsers.add_parser("search", help="Search for prompts by name or description")
    search_parser.add_argument("term", help="Search term")
    search_parser.add_argument("--tag", help="Filter search results by tag")
    # use
    use_parser = subparsers.add_parser("use", help="Output prompt content for use in other tools")
    use_parser.add_argument("name", help="Name of the prompt to use")
    if len(sys.argv) > 1 and sys.argv[1] == "use":
        args, unknown = parser.parse_known_args()
        provided_vars = {}
        for i in range(0, len(unknown), 2):
            if unknown[i].startswith("--") and i + 1 < len(unknown):
                var_name = unknown[i][2:]
                val = unknown[i+1]
                
                # Native File Support: If value starts with @, treat as file path
                if val.startswith("@"):
                    filepath = val[1:]
                    if os.path.exists(filepath):
                        try:
                            with open(filepath, "r", encoding="utf-8") as f:
                                val = f.read().strip()
                        except Exception as e:
                            print(f"{Colors.YELLOW}Warning: Could not read file {filepath} ({e}). Using raw string.{Colors.RESET}", file=sys.stderr)
                    else:
                        print(f"{Colors.YELLOW}Warning: File {filepath} not found. Using raw string.{Colors.RESET}", file=sys.stderr)
                
                provided_vars[var_name] = val
        use_prompt(args.name, provided_vars)
    else:
        args = parser.parse_args()
        if args.command == "list":
            list_prompts(args.tag)
        elif args.command == "tags":
            list_tags()
        elif args.command == "search":
            search_prompts(args.term, args.tag)
        else:
            parser.print_help()
