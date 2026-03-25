# Using promptbook with Gemini CLI

promptbook is natively integrated with Gemini CLI as an extension.

## Installation
If you have the promptbook repository, you can link it:
```bash
gemini extension install /path/to/promptbook
```

## Basic Usage
Use the `/prompts:` prefix to trigger any prompt:
```bash
/prompts:code-review-security {{file}}
```

## Explorer
Launch the TUI to browse all 437+ prompts:
```bash
pop
# or
make tui
```

## Search
Search for specific prompts via CLI:
```bash
pop search "react testing"
```

---

## Using Promptbook as Skills

PromptBook templates work as reusable skills for Gemini CLI. Here's how to use them:

### Quick Skill Injection
```bash
# Hydrate a template and copy to clipboard
pop use code-reviewer-agent --args @file.py | pbcopy

# Use with language context for surgical extraction
pop use security-scan --language python --args @main.py | pbcopy

# Preview without copying
pop use refactor-agent --no-copy
```

### Creating Custom Skills
```bash
# Launch the interactive wizard
pop create

# This creates a .toml template you can customize
# Then use it: pop use my-custom-skill
```

### Export as Standalone Skill
```bash
# Export a template for reuse
pop use project-guidelines --no-copy > ~/.gemini/skills/my-project/SKILL.md
```

### Available Skill Categories

| Category | Use Case |
|----------|----------|
| `engineering/` | Code review, refactoring, debugging |
| `security/` | Security audits, threat modeling |
| `testing/` | TDD, E2E, test generation |
| `architecture/` | System design, ADRs |
| `<language>-specialist/` | Language-specific patterns |

### Example Workflow
```bash
# 1. Find a skill
pop search "code review"

# 2. Use it with your code
pop use code-reviewer-agent --language python --args @src/main.py

# 3. Paste the hydrated prompt into Gemini CLI
```
