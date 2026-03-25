import os
import sys

# Add current directory to path so we can import our package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from promptbook import core  # noqa: E402
from promptbook.utils import Colors

CATALOG_FILE = "docs/CATALOG.md"

def generate_catalog():
    """Generates a terminal summary and a docs/CATALOG.md file."""
    prompts = core.get_prompts()
    
    # Terminal Output
    print(f"\n{Colors.BOLD}{Colors.CYAN}📋 Promptbook Template Overview{Colors.RESET}")
    print("=" * 80)
    
    # Group by category (primary tag)
    categories = {}
    for p in prompts:
        cat = p["tags"][0].replace("-", " ").title() if p["tags"] else "General"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    # Prepare Markdown Content
    md_content = [
        "# 📚 Promptbook Catalog\n\n",
        "A complete reference of all available expert prompt templates, organized by domain.\n\n",
        "| Category | Prompt | Description |\n",
        "|---|---|---|\n"
    ]

    for cat in sorted(categories.keys()):
        cat_prompts = categories[cat]
        
        # Terminal print
        print(f"\n{Colors.BOLD}{Colors.YELLOW}📂 {cat}{Colors.RESET} ({len(cat_prompts)} prompts)")
        print("-" * 80)
        
        for p in sorted(cat_prompts, key=lambda x: x["display_name"]):
            name = p["display_name"]
            desc = p["description"]
            
            # Markdown entry
            md_content.append(f"| **{cat}** | `{name}` | {desc} |\n")
            
            # Terminal print (truncated)
            t_desc = desc[:62] + "..." if len(desc) > 65 else desc
            print(f"  {Colors.GREEN}{name:<30}{Colors.RESET} | {t_desc}")

    # Write Markdown File
    os.makedirs(os.path.dirname(CATALOG_FILE), exist_ok=True)
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write("".join(md_content).strip() + "\n")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Catalog updated: {CATALOG_FILE}{Colors.RESET}")

if __name__ == "__main__":
    generate_catalog()
