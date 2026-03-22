import os
import re
import json


def sync_versions(new_version):
    print(f"Syncing all versions to: {new_version}")

    # 1. Update gemini-extension.json
    extension_path = "gemini-extension.json"
    if os.path.exists(extension_path):
        with open(extension_path, "r") as f:
            data = json.load(f)
        data["version"] = new_version
        with open(extension_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Updated {extension_path}")

    # 2. Update Cargo.toml
    cargo_path = "promptops-tui/Cargo.toml"
    if os.path.exists(cargo_path):
        with open(cargo_path, "r") as f:
            content = f.read()
        content = re.sub(
            r'^version\s*=\s*".*?"',
            f'version = "{new_version}"',
            content,
            flags=re.MULTILINE,
        )
        with open(cargo_path, "w") as f:
            f.write(content)
        print(f"Updated {cargo_path}")

    # 3. Update all prompt templates
    prompts_dir = "commands/prompts"
    if os.path.exists(prompts_dir):
        count = 0
        for root, _, fs in os.walk(prompts_dir):
            for f_name in fs:
                if f_name.endswith(".toml"):
                    path = os.path.join(root, f_name)
                    with open(path, "r") as file:
                        content = file.read()
                    # Only replace the top-level version field
                    new_content = re.sub(
                        r'^version\s*=\s*".*?"',
                        f'version = "{new_version}"',
                        content,
                        count=1,
                        flags=re.MULTILINE,
                    )
                    if new_content != content:
                        with open(path, "w") as file:
                            file.write(new_content)
                        count += 1
        print(f"Updated {count} prompt templates in {prompts_dir}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        sync_versions(sys.argv[1])
    else:
        print("Usage: python3 scripts/sync_all_versions.py <version>")
