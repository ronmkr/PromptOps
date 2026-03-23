import os
import datetime
import re
import json
import sys

# Add current directory to path so we can import our package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from promptops import core  # noqa: E402

README_FILE = "README.md"
GEMINI_FILE = "GEMINI.md"
CATALOG_DIR = "docs/catalog"


def get_prompts():
    """Wrapper around core.get_prompts to match the expected format for this script."""
    return core.get_prompts()


def generate_domain_notebook(tag_name, display_name, prompts):
    cells = []
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# 📖 PromptOps - {display_name} Catalog\n\n",
                f"Generated on: {datetime.date.today().isoformat()}\n\n",
                f"This notebook contains the reference for all **{display_name}** templates.",
            ],
        }
    )

    for p in prompts:
        source_lines = [
            f"### {p['display_name']}\n\n",
            f"> **Description**: {p['description']}\n",
            f"> **Input Needed**: `{p['args_description']}`\n",
            f"> **Version**: `{p['version']}` | **Last Updated**: `{p['last_updated']}`\n",
            f"> **Tags**: {', '.join([f'`{t}`' for t in p['tags']])}\n\n",
            "#### Template Content:\n",
            "````markdown\n",
            p["prompt"] + "\n",
            "````\n",
        ]
        cells.append({"cell_type": "markdown", "metadata": {}, "source": source_lines})

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    os.makedirs(CATALOG_DIR, exist_ok=True)
    # Sanitize filename: replace spaces, slashes, and ampersands
    filename = tag_name.lower().replace(" ", "-").replace("&", "and").replace("/", "-")
    filename = re.sub(r"-+", "-", filename)  # Remove double dashes
    filename += ".ipynb"
    filepath = os.path.join(CATALOG_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
        f.write("\n")
    return filename


def update_docs(prompts):
    # Domain configuration for both README and Gemini
    # Key: Display Name, Values: list of tags, link_filename (filled dynamically)
    domains = {
        "Code Review & Analysis": {"tags": ["code-review", "debug"], "links": []},
        "DevOps & Infrastructure": {"tags": ["devops", "infra"], "links": []},
        "Security & Compliance": {"tags": ["security"], "links": []},
        "Database & Data Engineering": {"tags": ["db"], "links": []},
        "Testing & Debugging": {"tags": ["test", "debug"], "links": []},
        "UI / UX & Frontend": {"tags": ["frontend"], "links": []},
        "Architecture & Design": {"tags": ["architecture"], "links": []},
        "Shell & Scripting": {"tags": ["shell"], "links": []},
        "Project Management & Agile": {"tags": ["agile"], "links": []},
        "Documentation & Learning": {
            "tags": ["docs", "learning", "writing"],
            "links": [],
        },
    }

    # 1. Generate Domain Notebooks
    for domain_name, config in domains.items():
        domain_prompts = [
            p for p in prompts if any(t in p["tags"] for t in config["tags"])
        ]
        if domain_prompts:
            # Deduplicate by display_name
            seen = set()
            unique_prompts = []
            for p in domain_prompts:
                if p["display_name"] not in seen:
                    unique_prompts.append(p)
                    seen.add(p["display_name"])

            nb_filename = generate_domain_notebook(
                domain_name,
                domain_name,
                sorted(unique_prompts, key=lambda x: x["display_name"]),
            )
            config["filename"] = nb_filename
            config["prompts"] = sorted(unique_prompts, key=lambda x: x["display_name"])

    # 2. Update GEMINI.md
    with open(GEMINI_FILE, "r", encoding="utf-8") as f:
        gemini_content = f.read()

    gemini_list = "## Available Prompts\n"
    for domain_name, config in domains.items():
        if "prompts" in config:
            gemini_list += f"### {domain_name}\n"
            for p in config["prompts"]:
                gemini_list += f"- `/prompts:{p['display_name']}`: {p['description'].rstrip('.')}\n"

    gemini_pattern = r"## Available Prompts.*?(?=## How to Use Prompts)"
    gemini_content = re.sub(
        gemini_pattern, gemini_list, gemini_content, flags=re.DOTALL
    )
    with open(GEMINI_FILE, "w", encoding="utf-8") as f:
        f.write(gemini_content)

    # 3. Update README.md
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme_content = f.read()

    readme_list = "## Available Templates\n\nTemplates are categorized by domain. Click a category to view its full reference notebook.\n\n"
    for domain_name, config in domains.items():
        if "prompts" in config:
            readme_list += f"### [{domain_name}]({CATALOG_DIR}/{config['filename']})\n"
            for p in config["prompts"]:
                readme_list += f"- `/prompts:{p['display_name']}` - {p['description'].rstrip('.')}\n"
            readme_list += "\n"

    readme_pattern = r"## Available Templates.*?(?=## 🤝 Contributing)"
    readme_content = re.sub(
        readme_pattern, readme_list, readme_content, flags=re.DOTALL
    )
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(readme_content)


if __name__ == "__main__":
    prompts = get_prompts()
    update_docs(prompts)
    print(f"\n🚀 Distributed documentation synchronized in {CATALOG_DIR}/")
