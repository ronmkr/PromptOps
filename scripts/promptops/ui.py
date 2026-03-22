import sys
from .utils import Colors


def print_help():
    header_line = "+" + "-" * 68 + "+"
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


def format_prompt_list(grouped):
    print(
        f"{Colors.BOLD}{Colors.CYAN}{'PROMPT NAME':<35} | {'DESCRIPTION'}{Colors.RESET}"
    )
    print("-" * 100)
    for name in sorted(grouped.keys()):
        versions = grouped[name]
        v_ids = [v["version_id"] for v in versions if v["version_id"]]
        v_str = f" [{', '.join(v_ids)}]" if v_ids else ""
        desc = versions[0]["description"]
        print(f"{Colors.GREEN}{name + v_str:<35}{Colors.RESET} | {desc}")


def format_tag_list(unique_names):
    print(f"{Colors.BOLD}{Colors.CYAN}Available Tags:{Colors.RESET}")
    print("-" * 20)
    for tag in sorted(unique_names.keys()):
        print(f"{Colors.YELLOW}{tag:<20}{Colors.RESET} ({unique_names[tag]} prompts)")


def print_interactive_header(display_name, label):
    print(
        "\n"
        + f"{Colors.BOLD}{Colors.YELLOW}"
        + "╭"
        + "─" * 68
        + "╮"
        + f"{Colors.RESET}",
        file=sys.stderr,
    )
    print(
        f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.CYAN}PromptOps Interactive: {Colors.BOLD}{display_name}{Colors.RESET}",
        file=sys.stderr,
    )
    print(
        f"{Colors.BOLD}{Colors.YELLOW}├" + "─" * 68 + "┤" + f"{Colors.RESET}",
        file=sys.stderr,
    )
    print(
        f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.BOLD}Required:{Colors.RESET} {Colors.GREEN}{label}{Colors.RESET}",
        file=sys.stderr,
    )
    print(
        f"{Colors.BOLD}{Colors.YELLOW}│{Colors.RESET} {Colors.BOLD}Finish:{Colors.RESET}   Press {Colors.BOLD}Ctrl+D{Colors.RESET} (Mac/Linux) or {Colors.BOLD}Ctrl+Z+Enter{Colors.RESET} (Win)",
        file=sys.stderr,
    )
    print(
        f"{Colors.BOLD}{Colors.YELLOW}╰" + "─" * 68 + "╯" + f"{Colors.RESET}",
        file=sys.stderr,
    )
    print(f" {Colors.BOLD}[Paste {label} below]{Colors.RESET}\n", file=sys.stderr)
