# Using promptbook with GitHub Copilot / Codex

Copilot uses inline and chat-based interactions.

## Inline Instructions
Find a relevant prompt in the [Catalog](../catalog/FULL_CATALOG.md) and paste it as a comment for Copilot to follow.

## Chat
Copy-paste promptbook templates from the TUI (`pop`) directly into the Copilot Chat window.

---

## Using Promptbook as Skills

PromptBook templates work as reusable skills for Copilot/Codex. Here's how to use them:

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
pop use project-guidelines --no-copy > .github/copilot-instructions.md
```

### Setting Up in Copilot

1. **Create a copilot instructions file**:
   ```bash
   mkdir -p .github
   ```

2. **Export skills**:
   ```bash
   pop use code-reviewer-agent --no-copy > .github/copilot-instructions.md
   ```

3. **Or use inline**:
   Copy the hydrated prompt and paste as a comment at the top of your file.

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

# 3. Paste the hydrated prompt into Copilot Chat
```
