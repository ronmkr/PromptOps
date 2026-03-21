import os
import glob
import tomllib
import datetime
import re

PROMPTS_DIR = "commands/prompts"
CATALOG_FILE = "CATALOG.md"
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

def generate_catalog(prompts):
    # Collect all unique tags
    all_tags = set()
    for p in prompts:
        all_tags.update(p["tags"])
    sorted_tags = sorted(list(all_tags))

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write("# PromptOps - Prompt Template Catalog\n\n")
        f.write(f"This catalog is auto-generated on {datetime.date.today().isoformat()}. It contains the reference for all {len(prompts)} templates available in the PromptOps library.\n\n")
        
        f.write("## Table of Contents\n\n")
        for tag in sorted_tags:
            f.write(f"- [{tag.replace('-', ' ').title()}](#{tag})\n")
        f.write("\n---\n\n")

        for tag in sorted_tags:
            f.write(f"## <a name='{tag}'></a> {tag.replace('-', ' ').title()}\n\n")
            tag_prompts = [p for p in prompts if tag in p["tags"]]
            for p in tag_prompts:
                f.write(f"### {p['name']}\n\n")
                f.write(f"> **Description**: {p['description']}\n")
                f.write(f"> **Input Format**: `{p['args_description']}`\n")
                f.write(f"> **Version**: `{p['version']}` | **Last Updated**: `{p['last_updated']}`\n")
                f.write(f"> **Tags**: {', '.join([f'`{t}`' for t in p['tags']])}\n\n")
                f.write("#### Template Content:\n")
                f.write("```markdown\n")
                f.write(p["prompt"])
                f.write("\n```\n\n")
                f.write("---\n\n")
    print(f"Update: {CATALOG_FILE} completed.")

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

    new_list = "## Available Templates\n\nTemplates are located in `commands/prompts/`. See the [Prompt Catalog](CATALOG.md) for full template details.\n\n"
    
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

    pattern = r"## Available Templates.*?(?=## Customization)"
    # Note: README now uses "Available Templates" and "Customization" as headers.
    new_content = re.sub(pattern, new_list, content, flags=re.DOTALL)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Update: {README_FILE} completed.")

if __name__ == "__main__":
    prompts = get_prompts()
    generate_catalog(prompts)
    update_gemini_md(prompts)
    update_readme_md(prompts)
    print("\nDocumentation synchronization completed.")
