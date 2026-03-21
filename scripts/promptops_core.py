import os
import sys
import glob
import tomllib
import argparse
import json
import difflib
import re
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
    print(f"{'PROMPT NAME':<35} | {'DESCRIPTION'}")
    print("-" * 100)
    for p in prompts:
        print(f"{p['name']:<35} | {p['description']}")
def list_tags(prompts_dir=None):
    prompts = get_prompts(prompts_dir)
    tags = set()
    for p in prompts:
        tags.update(p["tags"])
    print("Available Tags:")
    print("-" * 20)
    for tag in sorted(list(tags)):
        count = len([p for p in prompts if tag in p["tags"]])
        print(f"{tag:<20} ({count} prompts)")
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
    print(f"{'PROMPT NAME':<35} | {'DESCRIPTION'}")
    print("-" * 100)
    for p in results[:15]:
        print(f"{p['name']:<35} | {p['description']}")
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
                    # Interactive mode UX
                    print("\n" + "="*70, file=sys.stderr)
                    print(" ✨ PromptOps Interactive Mode", file=sys.stderr)
                    print("-" * 70, file=sys.stderr)
                    print(f" The template requires a value for: {{{{{var}}}}}\n", file=sys.stderr)
                    print(" INSTRUCTIONS:", file=sys.stderr)
                    print(" 1. Paste your code or text below.", file=sys.stderr)
                    print(" 2. Press Enter to go to a new line if needed.", file=sys.stderr)
                    print(" 3. When you are completely finished, press Ctrl+D (Mac/Linux) or", file=sys.stderr)
                    print("    Ctrl+Z then Enter (Windows) to submit.", file=sys.stderr)
                    print("-" * 70, file=sys.stderr)
                    print(f" [Paste your content for {{{{{var}}}}}] >\n", file=sys.stderr)
                    try:
                        val = sys.stdin.read().strip()
                        if not val:
                            print(f"\n Warning: No input provided for {var}.", file=sys.stderr)
                        final_vars[var] = val
                        print("\n" + "="*70 + "\n", file=sys.stderr)
                    except EOFError:
                        print("\nError: Input interrupted.", file=sys.stderr)
                        sys.exit(1)
            # Substitute variables
            for var, val in final_vars.items():
                prompt_content = prompt_content.replace(f"{{{{{var}}}}}", val)
            print(prompt_content)
    except Exception as e:
        print(f"Error reading prompt: {e}", file=sys.stderr)
        sys.exit(1)
def main():
    if len(sys.argv) == 1:
        try:
            import promptops_tui
            promptops_tui.main()
            return
        except ImportError as e:
            print(f"Warning: Could not load TUI ({e}). Falling back to CLI mode.", file=sys.stderr)
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
                provided_vars[var_name] = unknown[i+1]
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
