import os
import glob
import tomllib
import datetime

PROMPTS_DIR = "commands/prompts"
OUTPUT_FILE = "CATALOG.md"

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
                    "version": data.get("version", "N/A"),
                    "last_updated": data.get("last_updated", "N/A"),
                    "tags": data.get("tags", ["general"]),
                    "prompt": data.get("prompt", "").strip()
                })
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue
    return sorted(prompts, key=lambda x: x["name"])

def generate_catalog():
    prompts = get_prompts()
    
    # Collect all unique tags
    all_tags = set()
    for p in prompts:
        all_tags.update(p["tags"])
    sorted_tags = sorted(list(all_tags))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# 📖 PromptOps - Prompt Catalog\n\n")
        f.write(f"This catalog is auto-generated on {datetime.date.today().isoformat()}. It contains the full reference for all {len(prompts)} prompts available in the PromptOps library.\n\n")
        
        # Table of Contents
        f.write("## 🗂️ Table of Contents\n\n")
        for tag in sorted_tags:
            f.write(f"- [{tag.replace('-', ' ').title()}](#{tag})\n")
        f.write("\n---\n\n")

        # Category Sections
        for tag in sorted_tags:
            f.write(f"## <a name='{tag}'></a> {tag.replace('-', ' ').title()}\n\n")
            
            tag_prompts = [p for p in prompts if tag in p["tags"]]
            for p in tag_prompts:
                f.write(f"### {p['name']}\n\n")
                f.write(f"> **Description**: {p['description']}\n")
                f.write(f"> **Version**: `{p['version']}` | **Last Updated**: `{p['last_updated']}`\n")
                f.write(f"> **Tags**: {', '.join([f'`{t}`' for t in p['tags']])}\n\n")
                
                f.write("#### Prompt Template:\n")
                f.write("```markdown\n")
                f.write(p["prompt"])
                f.write("\n```\n\n")
                f.write("---\n\n")

    print(f"✅ {OUTPUT_FILE} generated successfully with {len(prompts)} prompts.")

if __name__ == "__main__":
    generate_catalog()
