# Using promptbook with Windsurf

Windsurf (by Codeium) supports highly contextual agentic flows.

## Context Injection
Use promptbook templates to set the initial "mental model" for Windsurf.
Browse the `architecture/` and `workflow/` categories for high-level guidance.

## TUI Explorer
Keep the `pop` TUI open in a separate terminal to quickly find and inject prompts.

---

## Using Promptbook as Skills

PromptBook templates work as reusable skills for Windsurf. Here's how to use them:

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
# Export a template as a Windsurf-compatible skill
pop use project-guidelines --no-copy > .windsurf/skills/project-guidelines.md
```

### Setting Up in Windsurf

1. **Create a skills directory**:
   ```bash
   mkdir -p .windsurf/skills
   ```

2. **Export skills**:
   ```bash
   pop use tdd-workflow --no-copy > .windsurf/skills/tdd-workflow.md
   pop use security-scan --no-copy > .windsurf/skills/security-scan.md
   ```

3. **Reference in Windsurf config**:
   Add the skill path to your Windsurf settings or reference via `@skill` syntax.

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

# 3. Paste the hydrated prompt into Windsurf
```
