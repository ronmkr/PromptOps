# Using promptbook with Cursor

Cursor supports custom rules and prompt templates.

## Custom Rules (.cursorrules)
You can copy the content of any promptbook template into your project's `.cursorrules` file.
Find relevant rules in: `commands/prompts/rules/`

## Template Injection
Use the `pop` CLI to quickly copy a prompt to your clipboard:
```bash
pop use python-testing --no-copy
```
Then paste it into Cursor's composer or chat.

## Native Catalog
Browse all 437+ prompts in the [Full Catalog](../catalog/FULL_CATALOG.md).

---

## Using Promptbook as Skills

PromptBook templates work as reusable skills for Cursor. Here's how to use them:

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
# Export a template as a Cursor-compatible skill
pop use project-guidelines --no-copy > .cursorrules
```

### Setting Up in Cursor

1. **Create a skills directory**:
   ```bash
   mkdir -p .cursor/skills
   ```

2. **Export skills**:
   ```bash
   pop use tdd-workflow --no-copy > .cursor/skills/tdd-workflow.md
   pop use security-scan --no-copy > .cursor/skills/security-scan.md
   ```

3. **Reference in .cursorrules**:
   ```markdown
   # .cursorrules
   @tdd-workflow
   @security-scan
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

# 3. Paste the hydrated prompt into Cursor's composer
```
