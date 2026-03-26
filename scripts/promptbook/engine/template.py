import os
import re
import sys

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from ..config import PROMPTS_DIR, Colors


class TemplateEngine:
    """Handles prompt template discovery, loading, and hydration."""

    def __init__(self, prompts_dir: str = PROMPTS_DIR):
        self.prompts_dir = prompts_dir

    def get_all_prompts(self) -> list[dict]:
        """Loads and returns all prompt templates with metadata."""
        all_prompts = []
        if not os.path.exists(self.prompts_dir):
            return []

        for root, _dirs, files in os.walk(self.prompts_dir):
            rel_path = os.path.relpath(root, self.prompts_dir)
            category = None if rel_path == "." else rel_path

            for filename in files:
                if filename.endswith(".toml"):
                    full_path = os.path.join(root, filename)
                    name = filename[:-5]
                    version_id = None

                    # Handle versioned naming: name.v1.toml
                    if "." in name:
                        parts = name.split(".")
                        name = parts[0]
                        version_id = parts[1]

                    try:
                        with open(full_path, "rb") as f:
                            data = tomllib.load(f)

                        metadata = {
                            "name": name,
                            "display_name": f"{name}:{version_id}" if version_id else name,
                            "description": data.get("description", ""),
                            "args_description": data.get("args_description", "Input Data"),
                            "version": data.get("version", "1.0.0"),
                            "last_updated": data.get("last_updated", ""),
                            "tags": data.get("tags", []),
                            "sensitive": data.get("sensitive", False),
                            "version_id": version_id,
                            "path": full_path,
                            "category": category,
                        }
                        all_prompts.append(metadata)
                    except Exception as e:
                        print(
                            f"{Colors.YELLOW}Warning: Could not load {full_path}: {e}{Colors.RESET}",
                            file=sys.stderr,
                        )

        return all_prompts

    def find_prompt_versions(self, name: str) -> list[dict]:
        """Finds all available versions of a prompt by name."""
        all_prompts = self.get_all_prompts()
        return [p for p in all_prompts if p["name"] == name]

    @staticmethod
    def discover_variables(text: str | None) -> set[str]:
        """Recursively discovers variables in template text."""
        variables = set()
        if not text:
            return variables

        # Iteratively find all blocks {{ ... }} and recurse into them
        # to handle nested variables like {{$(echo {{args}})}}
        def find_vars(content):
            # Find innermost matches first to avoid greedy matching across blocks
            found = re.findall(r"\{\{\s*([^{}]+?)\s*\}\}", content)
            for v in found:
                v = v.strip()
                if v.startswith("$(") and v.endswith(")"):
                    # Recurse into shell block content
                    find_vars(v[2:-1])
                elif v.startswith("env."):
                    pass
                else:
                    variables.add(v)

            # If there might be more nested blocks, remove what we found and try again
            remaining = re.sub(r"\{\{\s*([^{}]+?)\s*\}\}", "V", content)
            if remaining != content:
                find_vars(remaining)

        find_vars(text)
        return variables

    @staticmethod
    def hydrate(template: str, variables: dict[str, str]) -> str:
        """Hydrates a template string with provided variables, including shell blocks and conditionals."""
        import shlex
        import subprocess

        def handle_conditionals(text):
            cond_pattern = r"<if\s+(\w+)\s*=\s*\"([^\"]+)\"\s*>(.*?)</if>"

            def cond_substitute(match):
                key, expected_val, content = match.group(1), match.group(2), match.group(3)
                actual_val = str(variables.get(key, "")).strip().lower()
                return content if actual_val == expected_val.strip().lower() else ""

            return re.sub(cond_pattern, cond_substitute, text, flags=re.DOTALL)

        def handle_existence_conditionals(text):
            exist_pattern = r"<if\s+(\w+)\s*>(.*?)</if>"

            def exist_substitute(match):
                key, content = match.group(1), match.group(2)
                return content if variables.get(key) else ""

            return re.sub(exist_pattern, exist_substitute, text, flags=re.DOTALL)

        # 1. Resolve conditionals first
        template = handle_conditionals(template)
        template = handle_existence_conditionals(template)

        # 2. Find and protect shell blocks {{$( ... )}} using balanced braces stack
        def find_shell_ranges(text):
            ranges = []
            stack = 0
            start = -1
            i = 0
            while i < len(text):
                if text[i : i + 2] == "{{":
                    if i > 0 and text[i - 1] == "\\":
                        i += 2
                        continue
                    if text[i : i + 4] == "{{$(":
                        if stack == 0:
                            start = i
                        stack += 1
                        i += 4
                        continue
                    if stack > 0:
                        stack += 1
                    i += 2
                elif text[i : i + 2] == "}}":
                    if stack > 0:
                        stack -= 1
                        if stack == 0:
                            ranges.append((start, i + 2))
                    i += 2
                else:
                    i += 1
            return ranges

        shell_ranges = find_shell_ranges(template)
        tokenized_template = ""
        last_pos = 0
        token_map = {}
        for i, (s, e) in enumerate(shell_ranges):
            token = f"__PB_SHELL_{i}__"
            token_map[token] = template[s + 2 : e - 2]
            tokenized_template += template[last_pos:s] + token
            last_pos = e
        tokenized_template += template[last_pos:]

        # 3. Resolve standard variables and env vars in protected template
        std_pattern = r"(\\)?\{\{\s*([^{}]+?)\s*\}\}"

        def resolve_std_block(m):
            escape_char, content = m.group(1), m.group(2).strip()
            if escape_char == "\\":
                return f"{{{{{content}}}}}"
            if content.startswith("env."):
                return os.environ.get(
                    content[4:].strip(), f"[Env var {content[4:].strip()} not found]"
                )
            return str(variables.get(content, m.group(0)))

        hydrated_text = re.sub(std_pattern, resolve_std_block, tokenized_template)

        # 4. Resolve shell blocks and replace tokens
        for token, shell_content in token_map.items():
            inner_cmd = shell_content[2:-1].strip()

            def quote_fn(mm):
                v_name = mm.group(1).strip()
                if v_name.startswith("env."):
                    val = os.environ.get(v_name[4:].strip(), "")
                else:
                    val = str(variables.get(v_name, ""))
                return shlex.quote(val)

            safe_cmd = re.sub(r"\{\{\s*(.*?)\s*\}\}", quote_fn, inner_cmd)
            try:
                res = subprocess.check_output(
                    safe_cmd, shell=True, stderr=subprocess.STDOUT, text=True
                ).strip()
            except Exception as e:
                res = f"[Error: {str(e)}]"
            hydrated_text = hydrated_text.replace(token, res)

        return hydrated_text.strip()
