import json
import os
import sys

from .config import PROMPTS_DIR, Colors, SystemInfo
from .engine.session import SessionManager
from .engine.template import TemplateEngine
from .providers.llm import LLMProvider
from .ui import (
    print_interactive_header,
)
from .utils import AuditLogger, copy_to_clipboard

if not SystemInfo.IS_WINDOWS:
    import termios
    import tty
else:
    import msvcrt


# --- Interactive Utilities ---


def _get_char():
    """Reads a single character from stdin in raw mode."""
    if not SystemInfo.IS_WINDOWS:
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
        user_vars = sorted(list(variables))
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
            elif var.startswith("env."):
                final_vars[var] = os.environ.get(var[4:], f"[Env var {var[4:]} not found]")
                i += 1
            elif var.startswith("$("):
                # Shell blocks are handled by TemplateEngine.hydrate
                i += 1
            else:
                label = (
                    data.get("args_description", "Input Data")
                    if var == "args"
                    else var.replace("_", " ").title()
                )
                print_interactive_header(display_name, label)

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
                        if user_vars[i] in final_vars:
                            del final_vars[user_vars[i]]
                        continue
                    else:
                        continue

                final_vars[var] = "\n".join(lines).strip()
                i += 1
                print(
                    "\n" + f"{Colors.BOLD}{Colors.YELLOW}" + "─" * 70 + f"{Colors.RESET}" + "\n",
                    file=sys.stderr,
                )
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user.{Colors.RESET}", file=sys.stderr)
        sys.exit(0)

    return final_vars


def _confirm_sensitive_copy(name):
    """Asks for confirmation before copying sensitive data to clipboard."""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  SECURITY WARNING:{Colors.RESET}")
    print(
        f"{Colors.YELLOW}This prompt is marked as SENSITIVE and will be copied to your clipboard.{Colors.RESET}"
    )
    try:
        confirm = input("\nCopy to clipboard? (y/N): ").lower()
        return confirm == "y"
    except (KeyboardInterrupt, EOFError):
        return False


# --- Core Logic ---


def get_prompts(prompts_dir=None):
    engine = TemplateEngine(prompts_dir or PROMPTS_DIR)
    return engine.get_all_prompts()


def list_prompts(tag_filter=None, prompts_dir=None):
    from .cli.handlers import list_prompts_handler

    list_prompts_handler(tag_filter, prompts_dir=prompts_dir)


def list_tags(prompts_dir=None, raw=False):
    from .cli.handlers import list_tags_handler

    if raw:
        engine = TemplateEngine(prompts_dir or PROMPTS_DIR)
        prompts = engine.get_all_prompts()
        tags = set()
        for p in prompts:
            tags.update(p["tags"])
        for tag in sorted(list(tags)):
            print(tag)
    else:
        list_tags_handler(prompts_dir=prompts_dir)


def search_prompts(term, tag_filter=None, prompts_dir=None):
    from .cli.handlers import search_prompts_handler

    search_prompts_handler(term, tag_filter, prompts_dir=prompts_dir)


def use_prompt(
    name,
    provided_vars=None,
    prompts_dir=None,
    return_only=False,
    version_hint=None,
    no_copy=False,
    auto_confirm=False,
    mask=False,
    json_output=False,
    profile_name=None,
    return_hydrated=False,
):
    if provided_vars is None:
        provided_vars = {}

    session = SessionManager()
    if profile_name:
        profile = session.load_profile(profile_name)
        if profile:
            merged = profile.copy()
            merged.update(provided_vars)
            provided_vars = merged

    engine = TemplateEngine(prompts_dir or PROMPTS_DIR)
    versions = engine.find_prompt_versions(name)

    if not versions:
        print(f"Error: Prompt '{name}' not found.", file=sys.stderr)
        sys.exit(1)

    selected = None
    if version_hint:
        selected = next((v for v in versions if v["version_id"] == version_hint), None)
    elif len(versions) == 1:
        selected = versions[0]
    else:
        if not sys.stdin.isatty():
            selected = versions[0]
        else:
            print(f"\n{Colors.BOLD}Multiple versions found for '{name}':{Colors.RESET}")
            for i, v in enumerate(versions):
                print(f"  {i + 1}) {Colors.GREEN}{v['version_id'] or 'default'}{Colors.RESET}")
            choice = input(f"Select (1-{len(versions)}): ")
            selected = versions[int(choice) - 1]

    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    with open(selected["path"], "rb") as f:
        data = tomllib.load(f)

    legacy_p = data.get("prompt", "")
    system_p = data.get("system_prompt", "")
    user_p = data.get("user_prompt", "")

    # Variables
    vars_to_collect = set()
    vars_to_collect.update(engine.discover_variables(legacy_p))
    vars_to_collect.update(engine.discover_variables(system_p))
    vars_to_collect.update(engine.discover_variables(user_p))

    if return_only:
        return (legacy_p or user_p), sorted(list(vars_to_collect))

    final_vars = _collect_variables(selected["display_name"], vars_to_collect, data, provided_vars)

    if mask:
        try:
            import scrubadub

            for k, v in final_vars.items():
                if isinstance(v, str):
                    final_vars[k] = scrubadub.clean(v)
        except ImportError:
            pass

    if selected["sensitive"]:
        AuditLogger.log(name, selected["version_id"], final_vars)

    # Hydrate
    h_legacy = engine.hydrate(legacy_p, final_vars) if legacy_p else ""
    h_system = engine.hydrate(system_p, final_vars) if system_p else ""
    h_user = engine.hydrate(user_p, final_vars) if user_p else ""

    if return_hydrated:
        return {"legacy": h_legacy, "system": h_system, "user": h_user, "vars": final_vars}

    # Output
    output = ""
    copy_text = ""
    if json_output:
        res = {"messages": []}
        if h_system:
            res["messages"].append({"role": "system", "content": h_system})
        if h_user:
            res["messages"].append({"role": "user", "content": h_user})
        if h_legacy:
            res["prompt"] = h_legacy
        output = json.dumps(res, indent=2)
        copy_text = output
    else:
        if h_system or h_user:
            output = (
                f"{Colors.BOLD}{Colors.MAGENTA}--- SYSTEM ---{Colors.RESET}\n{h_system}\n\n"
                f"{Colors.BOLD}{Colors.CYAN}--- USER ---{Colors.RESET}\n{h_user}"
            )
            copy_text = f"--- SYSTEM ---\n{h_system}\n\n--- USER ---\n{h_user}"
        else:
            output = h_legacy
            copy_text = h_legacy

    if not no_copy:
        if not selected["sensitive"] or auto_confirm or _confirm_sensitive_copy(name):
            if copy_to_clipboard(copy_text):
                print(
                    f" {Colors.GREEN}[Done] Prompt copied to clipboard!{Colors.RESET}",
                    file=sys.stderr,
                )

    print(output)


def chain_prompts(prompt_names, initial_args=None, profile_name=None):
    """Sequentially executes a list of prompts."""
    curr_input = initial_args
    print(f"\n{Colors.BOLD}{Colors.CYAN}⛓️ Starting Prompt Chain{Colors.RESET}\n")

    for i, name in enumerate(prompt_names):
        print(f"{Colors.BOLD}Step {i + 1}: {Colors.GREEN}{name}{Colors.RESET}")
        res = use_prompt(
            name,
            provided_vars={"args": curr_input} if curr_input else {},
            profile_name=profile_name,
            return_hydrated=True,
            auto_confirm=True,
        )
        prompt_run = res["legacy"] or res["user"]
        system_run = res["system"]
        response = LLMProvider.execute(prompt_run, system_run)
        if not response:
            print(f"{Colors.RED}Chain broken at {name}{Colors.RESET}")
            break
        curr_input = response

    print(f"\n{Colors.BOLD}{Colors.CYAN}✅ Chain complete!{Colors.RESET}")
    copy_to_clipboard(curr_input)
    print(curr_input)


# --- Wizards ---


def create_wizard():
    from .core_wizards import create_wizard as cw

    cw()


def init_wizard():
    from .core_wizards import init_wizard as iw

    iw()
