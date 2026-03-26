from ..config import Colors
from ..engine.session import SessionManager
from ..engine.template import TemplateEngine
from ..providers.llm import Vault
from ..ui import format_prompt_list, format_tag_list


def list_prompts_handler(tag: str | None = None, prompts_dir: str | None = None):
    """Lists all available prompts, optionally filtered by tag."""
    engine = TemplateEngine(prompts_dir) if prompts_dir else TemplateEngine()
    prompts = engine.get_all_prompts()
    if tag:
        prompts = [p for p in prompts if tag.lower() in [t.lower() for t in p["tags"]]]

    grouped = {}
    for p in prompts:
        name = p["name"]
        if name not in grouped:
            grouped[name] = []
        grouped[name].append(p)

    format_prompt_list(grouped)


def list_tags_handler(raw: bool = False, prompts_dir: str | None = None):
    """Lists all unique tags across all prompts."""
    engine = TemplateEngine(prompts_dir) if prompts_dir else TemplateEngine()
    prompts = engine.get_all_prompts()
    unique_tags = {}
    for p in prompts:
        for tag in p["tags"]:
            tag_lower = tag.lower()
            unique_tags[tag_lower] = unique_tags.get(tag_lower, 0) + 1

    if raw:
        for tag in sorted(unique_tags.keys()):
            print(tag)
    else:
        format_tag_list(unique_tags)


def list_names_handler(prompts_dir: str | None = None):
    """Hidden helper for shell completion."""
    engine = TemplateEngine(prompts_dir) if prompts_dir else TemplateEngine()
    prompts = engine.get_all_prompts()
    names = set()
    for p in prompts:
        names.add(f"{p['name']}:{p['version_id']}" if p["version_id"] else p["name"])
    for name in sorted(list(names)):
        print(name)


def search_prompts_handler(term: str, tag: str | None = None, prompts_dir: str | None = None):
    """Searches across prompt names, descriptions, and tags with fuzzy matching."""
    import difflib

    engine = TemplateEngine(prompts_dir) if prompts_dir else TemplateEngine()
    prompts = engine.get_all_prompts()
    term = term.lower()

    # Get unique prompts first
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
            scores = [difflib.SequenceMatcher(None, term, part).ratio() for part in name.split("-")]
            scores.append(difflib.SequenceMatcher(None, term, name).ratio())
            score = max(scores) if scores else 0

        if score > 0.6:
            if not tag or tag.lower() in [t.lower() for t in p["tags"]]:
                scored_results.append((score, p))

    scored_results.sort(key=lambda x: x[0], reverse=True)
    results = [item[1] for item in scored_results]

    if not results:
        msg = f"No prompts found matching '{term}'"
        if tag:
            msg += f" with tag '{tag}'"
        print(msg)
        return

    # Re-group matching prompts to show all versions
    matching_names = {p["name"] for p in results}
    grouped = {}
    for p in prompts:
        if p["name"] in matching_names:
            if p["name"] not in grouped:
                grouped[p["name"]] = []
            grouped[p["name"]].append(p)

    format_prompt_list(grouped)


def use_prompt_handler(
    name: str,
    version: str | None = None,
    profile: str | None = None,
    no_copy: bool = False,
    yes: bool = False,
    mask: bool = False,
    json_output: bool = False,
    provided_vars: dict[str, str] | None = None,
):
    """Handles the 'use' command logic."""
    from ..core import use_prompt

    use_prompt(
        name,
        provided_vars=provided_vars,
        version_hint=version,
        no_copy=no_copy,
        auto_confirm=yes,
        mask=mask,
        json_output=json_output,
        profile_name=profile,
    )


def chain_handler(prompts: list[str], initial_args: str | None = None, profile: str | None = None):
    """Handles the 'chain' command logic."""
    from ..core import chain_prompts

    chain_prompts(prompts, initial_args=initial_args, profile_name=profile)


def vault_handler(command: str, provider: str | None = None, key: str | None = None):
    """Handles secure key management."""
    if command == "set" and provider and key:
        Vault.set_key(provider, key)
        print(f" {Colors.GREEN}[Done] API key for '{provider}' secured in vault.{Colors.RESET}")
    elif command == "list":
        keys = Vault.list_keys()
        if not keys:
            print("No keys found in vault.")
        else:
            print(f"{Colors.BOLD}Providers in Vault:{Colors.RESET}")
            for k in keys:
                print(f"  - {k}")
    elif command == "delete" and provider:
        if Vault.delete_key(provider):
            print(f" {Colors.GREEN}[Done] API key for '{provider}' deleted.{Colors.RESET}")
        else:
            print(f" {Colors.YELLOW}Warning: Provider '{provider}' not found.{Colors.RESET}")


def profile_handler(command: str, name: str | None = None, variables: dict[str, str] | None = None):
    """Handles context profiles."""
    manager = SessionManager()
    if command == "set" and name and variables is not None:
        manager.save_profile(name, variables)
        print(
            f" {Colors.GREEN}[Done] Profile '{name}' saved with {len(variables)} variables.{Colors.RESET}"
        )
    elif command == "list":
        profiles = manager.list_profiles()
        if not profiles:
            print("No profiles found.")
        else:
            print(f"{Colors.BOLD}Context Profiles:{Colors.RESET}")
            for p in profiles:
                print(f"  - {p}")
    elif command == "delete" and name:
        if manager.delete_profile(name):
            print(f" {Colors.GREEN}[Done] Profile '{name}' deleted.{Colors.RESET}")
        else:
            print(f" {Colors.YELLOW}Warning: Profile '{name}' not found.{Colors.RESET}")


def generate_completion_logic(shell: str):
    """Generates shell completion scripts."""
    if shell == "zsh":
        print(
            """#compdef pop promptbook
_pop() {
    local line
    _arguments -C \\
        "1: :((list\\:\"List all prompts\" tags\\:\"List all tags\" search\\:\"Search prompts\" use\\:\"Use a prompt\" completion\\:\"Generate shell completion\"))" \\
        "*::arg:->args"
    if [[ $state == args ]]; then
        case $words[1] in
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
