import argparse


def create_parser() -> argparse.ArgumentParser:
    """Creates and returns the main CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="promptbook — AI CLI Prompt Template Library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # List
    list_p = subparsers.add_parser("list", help="List all available templates")
    list_p.add_argument("--tag", help="Filter by category tag")

    # Search
    search_p = subparsers.add_parser("search", help="Search templates by name or description")
    search_p.add_argument("term", help="Search term")
    search_p.add_argument("--tag", help="Filter search by category tag")

    # Use
    use_p = subparsers.add_parser("use", help="Interactively run a prompt template")
    use_p.add_argument("name", help="Template name (e.g., refactor-suggestions)")
    use_p.add_argument("--version", help="Specific version to use (e.g., 1.0.0)")
    use_p.add_argument("--no-copy", action="store_true", help="Skip copying output to clipboard")
    use_p.add_argument("-y", "--yes", action="store_true", help="Skip sensitive confirmations")
    use_p.add_argument(
        "--mask", action="store_true", help="Mask PII in variables (GDPR compliance)"
    )
    use_p.add_argument(
        "--json",
        action="store_true",
        help="Output hydrated prompt as JSON (useful for multi-message prompts)",
    )
    use_p.add_argument(
        "--profile",
        help="Named context profile to use for pre-filling variables",
    )

    # Chain
    chain_p = subparsers.add_parser("chain", help="Sequentially execute multiple prompts")
    chain_p.add_argument("prompts", nargs="+", help="List of prompt names to chain")
    chain_p.add_argument("--args", help="Initial input for the first prompt (assigned to {{args}})")
    chain_p.add_argument("--profile", help="Context profile for the entire chain")

    # Profile
    profile_p = subparsers.add_parser("profile", help="Manage named context profiles")
    profile_sub = profile_p.add_subparsers(dest="profile_command")
    profile_set = profile_sub.add_parser("set", help="Create or update a profile")
    profile_set.add_argument("name", help="Profile name")
    profile_set.add_argument(
        "vars", nargs="+", help="Variable assignments (e.g., project=PB lang=py)"
    )
    profile_sub.add_parser("list", help="List available profiles")
    profile_del = profile_sub.add_parser("delete", help="Delete a profile")
    profile_del.add_argument("name", help="Profile name to delete")

    # Keys (Vault)
    keys_p = subparsers.add_parser("keys", help="Manage secure API keys in the vault")
    keys_sub = keys_p.add_subparsers(dest="keys_command")
    keys_set = keys_sub.add_parser("set", help="Set an API key for a provider")
    keys_set.add_argument("provider", help="Provider name (e.g., openai, gemini)")
    keys_set.add_argument("key", help="API Key value")
    keys_sub.add_parser("list", help="List providers with keys in the vault")
    keys_del = keys_sub.add_parser("delete", help="Delete a key from the vault")
    keys_del.add_argument("provider", help="Provider name to delete")

    # Tags
    subparsers.add_parser("tags", help="List all unique category tags")

    # Wizards
    subparsers.add_parser("init", help="Setup promptbook (completions, TUI, etc.)")
    subparsers.add_parser("create", help="Interactive prompt authoring wizard")

    # Hidden
    completion_p = subparsers.add_parser("completion", help=argparse.SUPPRESS)
    completion_p.add_argument("shell", choices=["zsh", "bash", "fish"])

    return parser
