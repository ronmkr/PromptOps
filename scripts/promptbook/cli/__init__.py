import sys

from ..core import create_wizard, init_wizard
from ..ui import print_help
from ..utils import resolve_file_injection
from .handlers import (
    chain_handler,
    generate_completion_logic,
    list_names_handler,
    list_prompts_handler,
    list_tags_handler,
    profile_handler,
    search_prompts_handler,
    use_prompt_handler,
    vault_handler,
)
from .parser import create_parser


def main():
    parser = create_parser()

    # Special handling for hidden internal commands used by completion
    if len(sys.argv) > 1:
        if sys.argv[1] == "_list_names":
            list_names_handler()
            return
        if sys.argv[1] == "_list_tags":
            list_tags_handler(raw=True)
            return

    if len(sys.argv) == 1:
        print_help()
        return

    # Handle 'use' separately because of arbitrary variable flags
    if len(sys.argv) > 1 and sys.argv[1] == "use":
        args, unknown = parser.parse_known_args()
        provided_vars = {}
        for i in range(len(unknown)):
            if unknown[i].startswith("--") and i + 1 < len(unknown):
                var_name = unknown[i][2:]
                provided_vars[var_name] = resolve_file_injection(unknown[i + 1])

        use_prompt_handler(
            name=args.name,
            version=args.version,
            profile=args.profile,
            no_copy=args.no_copy,
            yes=args.yes,
            mask=args.mask,
            json_output=args.json,
            provided_vars=provided_vars,
        )
        return

    args = parser.parse_args()

    if args.command == "list":
        list_prompts_handler(args.tag)
    elif args.command == "tags":
        list_tags_handler()
    elif args.command == "search":
        search_prompts_handler(args.term, args.tag)
    elif args.command == "profile":
        variables = {}
        if hasattr(args, "vars") and args.vars:
            for v in args.vars:
                if "=" in v:
                    k, val = v.split("=", 1)
                    variables[k.strip()] = val.strip()
        profile_handler(
            args.profile_command, args.name if hasattr(args, "name") else None, variables
        )
    elif args.command == "chain":
        chain_handler(args.prompts, initial_args=args.args, profile=args.profile)
    elif args.command == "keys":
        vault_handler(
            args.keys_command,
            provider=args.provider if hasattr(args, "provider") else None,
            key=args.key if hasattr(args, "key") else None,
        )
    elif args.command == "init":
        init_wizard()
    elif args.command == "create":
        create_wizard()
    elif args.command == "completion":
        generate_completion_logic(args.shell)
    else:
        parser.print_help()
