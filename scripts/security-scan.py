#!/usr/bin/env python3
import os
import re
import sys

# Patterns to look for
SECRETS_PATTERNS = [
    re.compile(r"(?i)api_key\s*=\s*['\"][a-z0-9]{20,}['\"]"),
    re.compile(r"(?i)password\s*=\s*['\"][a-z0-9]{8,}['\"]"),
    re.compile(r"(?i)secret\s*=\s*['\"][a-z0-9]{20,}['\"]"),
    re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----"),
]

DANGEROUS_PATTERNS = [
    re.compile(r"dangerouslySetInnerHTML"),
    re.compile(r"eval\("),
]

def scan_file(filepath):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for pattern in SECRETS_PATTERNS:
                if pattern.search(content):
                    errors.append(f"Potential secret found in {filepath} matching {pattern.pattern}")
            
            # For dangerous patterns, we allow them in templates (commands/prompts/) 
            # because they are often part of instructions or review checklists.
            if "commands/prompts/" not in filepath and "scripts/security-scan.py" not in filepath:
                for pattern in DANGEROUS_PATTERNS:
                    if pattern.search(content):
                        errors.append(f"Dangerous pattern '{pattern.pattern}' found in {filepath}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return errors

def main():
    root_dir = "."
    all_errors = []
    
    # Files/dirs to skip
    skip_dirs = {".git", "target", "node_modules", ".ruff_cache", "dist", "web/node_modules"}
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for file in files:
            if file.endswith((".ts", ".tsx", ".rs", ".toml", ".yml", ".yaml", ".sh", ".py")):
                filepath = os.path.join(root, file)
                all_errors.extend(scan_file(filepath))
    
    if all_errors:
        print("\n".join(all_errors))
        print(f"\nTotal security issues found: {len(all_errors)}")
        sys.exit(1)
    else:
        print("✅ No immediate security issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
