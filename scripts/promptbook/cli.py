import sys
import argparse
from .core import (
    list_prompts,
    list_tags,
    search_prompts,
    use_prompt,
    get_prompts,
    init_wizard,
)
from .ui import print_help
from .utils import resolve_file_injection, Vault, Colors


def list_names(prompts_dir=None):
    """Hidden helper for shell completion."""
    prompts = get_prompts(prompts_dir)
    names = set()
    for p in prompts:
        names.add(p["name"])
        if p["version_id"]:
            names.add(f"{p['name']}:{p['version_id']}")
    for name in sorted(list(names)):
        print(name)


def generate_completion(shell):
    """Generates shell completion scripts for Zsh, Bash, and Fish."""
    # ... (Keeping the implementation from previous core logic)
    # Note: Using 'pop' as the command name in completions.
    if shell == "zsh":
        print(
            """#compdef pop promptbook
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
"""
        )
    elif shell == "bash":
        print(
            """_pop_completion() {
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
complete -F _pop_completion pop promptbook
"""
        )
    elif shell == "fish":
        print(
            """# pop fish completion
complete -c pop -f
complete -c pop -n " __fish_use_subcommand" -a list -d "List all available prompts"
complete -c pop -n " __fish_use_subcommand" -a tags -d "List all unique tags"
complete -c pop -n " __fish_use_subcommand" -a search -d "Search prompts"
complete -c pop -n " __fish_use_subcommand" -a use -d "Use a prompt"
complete -c pop -n " __fish_use_subcommand" -a completion -d "Generate shell completion"
complete -c pop -n "__fish_seen_subcommand_from use" -a "(pop _list_names)"
complete -c pop -n "__fish_seen_subcommand_from list search" -l tag -a "(pop _list_tags)"
complete -c pop -n "__fish_seen_subcommand_from completion" -a "zsh bash fish"
"""
        )


def main():
    if len(sys.argv) == 1:
        print_help()
        sys.argv.append("-h")

    parser = argparse.ArgumentParser(
        description="promptbook CLI Helper", add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true")

    if len(sys.argv) > 1 and (sys.argv[1] in ("-h", "--help")):
        print_help()

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List all available prompts").add_argument(
        "--tag", help="Filter by tag"
    )
    subparsers.add_parser("tags", help="List all unique tags in the library")
    subparsers.add_parser(
        "init", help="Unified setup wizard (check deps, build TUI, completions)"
    )

    search_p = subparsers.add_parser(
        "search", help="Search for prompts by name or description"
    )
    search_p.add_argument("term", help="Search term")
    search_p.add_argument("--tag", help="Filter search results by tag")

    use_p = subparsers.add_parser(
        "use", help="Output prompt content for use in other tools"
    )
    use_p.add_argument("name", help="Name of the prompt to use")
    use_p.add_argument("--language", help="Specify the programming language context")
    use_p.add_argument(
        "--no-copy", action="store_true", help="Do not copy the prompt to the clipboard"
    )
    use_p.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Automatically confirm sensitive prompt warnings",
    )
    use_p.add_argument(
        "--mask",
        action="store_true",
        help="Mask PII (emails, phones, etc.) in input variables",
    )

    keys_p = subparsers.add_parser("keys", help="Manage secure API keys in the vault")
    keys_sub = keys_p.add_subparsers(dest="keys_command")

    keys_set = keys_sub.add_parser("set", help="Set an API key for a provider")
    keys_set.add_argument("provider", help="Provider name (e.g., openai, gemini)")
    keys_set.add_argument("key", help="API key value")

    keys_sub.add_parser("list", help="List providers with stored keys")

    keys_del = keys_sub.add_parser("delete", help="Delete a key from the vault")
    keys_del.add_argument("provider", help="Provider name to delete")

    comp_p = subparsers.add_parser(
        "completion", help="Generate shell completion script"
    )
    comp_p.add_argument("shell", choices=["zsh", "bash", "fish"], help="Target shell")

    subparsers.add_parser("_list_names", add_help=False)
    subparsers.add_parser("_list_tags", add_help=False)

    if len(sys.argv) > 1 and sys.argv[1] == "use":
        args, unknown = parser.parse_known_args()
        target_name = args.name
        version_hint = None
        if ":" in target_name:
            target_name, version_hint = target_name.split(":", 1)

        provided_vars = {}
        if args.language:
            provided_vars["language"] = args.language

        # Extract remaining variables from unknown args (like --code "...", etc)
        for i in range(0, len(unknown), 2):
            if unknown[i].startswith("--") and i + 1 < len(unknown):
                var_name = unknown[i][2:]
                provided_vars[var_name] = resolve_file_injection(unknown[i + 1])

        use_prompt(
            target_name,
            provided_vars=provided_vars,
            version_hint=version_hint,
            no_copy=args.no_copy,
            auto_confirm=args.yes,
            mask=args.mask,
        )
    else:
        args = parser.parse_args()
        if args.command == "list":
            list_prompts(args.tag)
        elif args.command == "tags":
            list_tags()
        elif args.command == "init":
            init_wizard()
        elif args.command == "search":
            search_prompts(args.term, args.tag)
        elif args.command == "completion":
            generate_completion(args.shell)
        elif args.command == "keys":
            if args.keys_command == "set":
                Vault.set_key(args.provider, args.key)
                print(
                    f" {Colors.GREEN}[Done] API key for '{args.provider}' secured in vault.{Colors.RESET}"
                )
            elif args.keys_command == "list":
                providers = Vault.list_keys()
                if not providers:
                    print("No keys stored in vault.")
                else:
                    print(f"{Colors.BOLD}Providers in vault:{Colors.RESET}")
                    for p in providers:
                        print(f"  - {p}")
            elif args.keys_command == "delete":
                if Vault.delete_key(args.provider):
                    print(
                        f" {Colors.GREEN}[Done] Key for '{args.provider}' removed.{Colors.RESET}"
                    )
                else:
                    print(
                        f" {Colors.Colors.YELLOW}Warning: Key for '{args.provider}' not found in vault.{Colors.RESET}"
                    )
            else:
                keys_p.print_help()
        elif args.command == "_list_names":
            list_names()
        elif args.command == "_list_tags":
            list_tags(raw=True)
        elif args.command is None:
            parser.print_help()


if __name__ == "__main__":
    main()
