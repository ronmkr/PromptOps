import os
import re
import sys
import tomllib
from datetime import datetime


class PromptValidator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.errors = []
        self.data = {}

    def validate(self):
        if not self._check_filename():
            return self.errors

        if not self._check_toml_syntax():
            return self.errors

        self._check_required_fields()
        self._check_version()
        self._check_date()
        self._check_tags()
        self._check_prompt_content()
        self._check_description()

        return self.errors

    def _check_filename(self):
        if not re.match(r"^[a-z0-9-]+\.toml$", self.filename):
            self.errors.append(
                f"Filename '{self.filename}' must be lowercase kebab-case (e.g., my-prompt.toml)"
            )
            return False
        return True

    def _check_toml_syntax(self):
        try:
            with open(self.filepath, "rb") as f:
                self.data = tomllib.load(f)
            return True
        except Exception as e:
            self.errors.append(f"Invalid TOML syntax: {e}")
            return False

    def _check_required_fields(self):
        required = [
            "description",
            "args_description",
            "version",
            "last_updated",
            "tags",
        ]
        for field in required:
            if field not in self.data:
                self.errors.append(f"Missing required field: '{field}'")
            else:
                val = self.data[field]
                if field == "tags":
                    if not isinstance(val, list):
                        self.errors.append("Field 'tags' must be a list of strings")
                elif not isinstance(val, str) or not val.strip():
                    self.errors.append(f"Field '{field}' must be a non-empty string")

        # Check for at least one prompt field
        if not any(f in self.data for f in ["prompt", "system_prompt", "user_prompt"]):
            self.errors.append(
                "Must provide at least one of: 'prompt', 'system_prompt', or 'user_prompt'"
            )

    def _check_version(self):
        version = self.data.get("version")
        if isinstance(version, str):
            if not re.match(r"^\d+\.\d+\.\d+$", version):
                self.errors.append(f"Invalid version '{version}'. Must follow SemVer (e.g., 1.0.0)")

    def _check_date(self):
        date_str = self.data.get("last_updated")
        if isinstance(date_str, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                self.errors.append(f"Invalid date format '{date_str}'. Use YYYY-MM-DD")
            else:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    self.errors.append(f"Date '{date_str}' is not a valid calendar date")

    def _check_tags(self):
        tags = self.data.get("tags")
        if isinstance(tags, list):
            if not tags:
                self.errors.append("Tags list cannot be empty")

            seen = set()
            for tag in tags:
                if not isinstance(tag, str) or not tag.strip():
                    self.errors.append("Tags must be non-empty strings")
                    continue

                if tag != tag.lower() or " " in tag:
                    self.errors.append(f"Tag '{tag}' must be lowercase and contain no spaces")

                if tag in seen:
                    self.errors.append(f"Duplicate tag found: '{tag}'")
                seen.add(tag)

    def _check_description(self):
        desc = self.data.get("description")
        if isinstance(desc, str):
            if len(desc) > 150:
                self.errors.append("Description is too long (max 150 characters)")
            if not desc.endswith("."):
                self.errors.append("Description should end with a period for consistency")

    def _check_prompt_content(self):
        # Gather all prompt content
        contents = [
            self.data.get(f, "")
            for f in ["prompt", "system_prompt", "user_prompt"]
            if isinstance(self.data.get(f), str)
        ]
        full_content = "\n".join(contents)

        if not any(re.search(r"^\s*#", c, re.MULTILINE) for c in contents):
            self.errors.append(
                "Prompt content must contain at least one Markdown header (e.g., # Title)"
            )

        # Find all variables like {{var}} or {{$(cmd)}} or {{env.VAR}}
        # Updated regex to match more complex variable patterns
        vars_found = re.findall(r"\{\{\s*(.+?)\s*\}\}", full_content)
        if not vars_found:
            self.errors.append("Prompt contains no variables. Did you forget '{{args}}'?")


def main():
    prompt_dir = "commands/prompts"
    prompt_files = []
    for root, _, files in os.walk(prompt_dir):
        for f in files:
            if f.endswith(".toml"):
                prompt_files.append(os.path.join(root, f))

    if not prompt_files:
        print(f"No prompt files found in {prompt_dir}")
        sys.exit(0)

    total_files_with_errors = 0
    total_errors = 0

    for filepath in sorted(prompt_files):
        validator = PromptValidator(filepath)
        errors = validator.validate()

        if errors:
            print(f"❌ {filepath}:")
            for err in errors:
                print(f"  - {err}")
            total_files_with_errors += 1
            total_errors += len(errors)

    if total_files_with_errors > 0:
        print(
            f"\nValidation failed: {total_files_with_errors} file(s) contained {total_errors} total error(s)."
        )
        sys.exit(1)
    else:
        print(f"✅ All {len(prompt_files)} prompts validated successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
