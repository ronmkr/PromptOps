import os
import glob
import tomllib
import datetime
import re
import json

PROMPTS_DIR = "commands/prompts"
CATALOG_FILE = "CATALOG.ipynb"
README_FILE = "README.md"
GEMINI_FILE = "GEMINI.md"

def get_prompts():
    prompts = []
    files = glob.glob(os.path.join(PROMPTS_DIR, "*.toml"))
    for f in files:
        name = os.path.basename(f).replace(".toml", "")
        try:
            with open(f, "rb") as file:
                data = tomllib.load(file)
                prompts.append({
                    "name": name,
                    "description": data.get("description", "No description provided"),
                    "args_description": data.get("args_description", "Input Data"),
                    "version": data.get("version", "N/A"),
                    "last_updated": data.get("last_updated", "N/A"),
                    "tags": data.get("tags", ["general"]),
                    "prompt": data.get("prompt", "").strip()
                })
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue
    return sorted(prompts, key=lambda x: x["name"])

def generate_catalog_ipynb(prompts):
    # Collect all unique tags
    all_tags = set()
    for p in prompts:
        all_tags.update(p["tags"])
    sorted_tags = sorted(list(all_tags))

    cells = []
    
    # Title Cell
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 📖 PromptOps - Prompt Template Catalog\n\n",
            f"Generated on: {datetime.date.today().isoformat()}\n\n",
            "This notebook contains the full reference for all templates available in the library."
        ]
    })

    # Table of Contents
    toc_lines = ["## 🗂️ Table of Contents\n"]
    for tag in sorted_tags:
        clean_tag = tag.replace('-', ' ').title()
        toc_lines.append(f"- [{clean_tag}](#{tag})\n")
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": toc_lines
    })

    # Content Cells
    for tag in sorted_tags:
        clean_tag = tag.replace('-', ' ').title()
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"---\n\n## {clean_tag} <a name=\"{tag}\"></a>\n"]
        })
        
        tag_prompts = [p for p in prompts if tag in p["tags"]]
        for p in tag_prompts:
            source_lines = [
                f"### {p['name']}\n\n",
                f"> **Description**: {p['description']}\n",
                f"> **Input Needed**: `{p['args_description']}`\n",
                f"> **Version**: `{p['version']}` | **Last Updated**: `{p['last_updated']}`\n",
                f"> **Tags**: {', '.join([f'`{t}`' for t in p['tags']])}\n\n",
                "#### Template Content:\n",
                "```markdown\n",
                p["prompt"] + "\n",
                "```\n"
            ]
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": source_lines
            })

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
    
    print(f"✅ {CATALOG_FILE} updated.")

def update_gemini_md(prompts):
    with open(GEMINI_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    categories = {
        "Code Review & Analysis": ["code-review", "debug"],
        "Documentation": ["docs"],
        "Testing": ["test"],
        "Architecture & Design": ["architecture"],
        "Learning & Explanation": ["learning"],
        "Writing & Communication": ["writing"],
        "Prompt Engineering": ["prompt-engineering"],
        "DevOps & Infrastructure": ["devops", "infra"],
        "Security & Compliance": ["security"],
        "Database & Data Engineering": ["db"],
        "UI / UX & Frontend": ["frontend"],
        "Shell & Scripting": ["shell"],
        "Project Management & Agile": ["agile"]
    }

    new_list = "## Available Prompts\n"
    for cat_name, tags in categories.items():
        cat_prompts = [p for p in prompts if any(t in p['tags'] for t in tags)]
        if cat_prompts:
            seen = set()
            unique_cat_prompts = []
            for p in cat_prompts:
                if p['name'] not in seen:
                    unique_cat_prompts.append(p)
                    seen.add(p['name'])
            
            new_list += f"### {cat_name}\n"
            for p in sorted(unique_cat_prompts, key=lambda x: x['name']):
                new_list += f"- `/prompts:{p['name']}`: {p['description'].rstrip('.')}\n"

    pattern = r"## Available Prompts.*?(?=## How to Use Prompts)"
    new_content = re.sub(pattern, new_list, content, flags=re.DOTALL)
    
    with open(GEMINI_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Update: {GEMINI_FILE} completed.")

def update_readme_md(prompts):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_list = "## Available Templates\n\nTemplates are located in `commands/prompts/`. See the [Prompt Catalog](CATALOG.ipynb) for full template details.\n\n"
    
    categories = {
        "Code Review & Analysis": ["code-review", "debug"],
        "DevOps & Infrastructure": ["devops", "infra"],
        "Security & Compliance": ["security"],
        "Database & Data": ["db"],
        "Testing & Debugging": ["test", "debug"],
        "Frontend & UI/UX": ["frontend"],
        "Architecture & Design": ["architecture"],
        "Shell & Scripting": ["shell"],
        "Project Management": ["agile"],
        "Documentation & Learning": ["docs", "learning", "writing"]
    }

    for cat_name, tags in categories.items():
        cat_prompts = [p for p in prompts if any(t in p['tags'] for t in tags)]
        if cat_prompts:
            seen = set()
            unique_cat_prompts = []
            for p in cat_prompts:
                if p['name'] not in seen:
                    unique_cat_prompts.append(p)
                    seen.add(p['name'])
            
            new_list += f"### {cat_name}\n"
            for p in sorted(unique_cat_prompts, key=lambda x: x['name']):
                new_list += f"- `/prompts:{p['name']}` - {p['description'].rstrip('.')}\n"
            new_list += "\n"

    pattern = r"## Available Templates.*?(?=## Extending the Library)"
    new_content = re.sub(pattern, new_list, content, flags=re.DOTALL)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ {README_FILE} updated.")

if __name__ == "__main__":
    prompts = get_prompts()
    generate_catalog_ipynb(prompts)
    update_gemini_md(prompts)
    update_readme_md(prompts)
    print("\n🚀 Documentation synchronized (Notebook format generated).")
