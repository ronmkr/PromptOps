# Using promptbook with Aider

Aider uses a CONTEXT -> COMMAND -> EDIT loop.

## Usage
1. Find a prompt using `pop search`.
2. Use `pop use <name> --no-copy` to see the prompt.
3. Paste the instructions into Aider's chat.

## Best Practices
Aider works best with "surgical" prompts from the `engineering/` and `testing/` categories.

---

## Using Promptbook as Skills

PromptBook templates work as reusable skills for Aider. Here's how to use them:

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

### Using with Aider's --prompt Flag
```bash
# Export a template and use with aider
pop use code-reviewer-agent --no-copy > /tmp/code-review.md
aider --prompt /tmp/code-review.md main.py

# Or pipe directly
pop use refactor-agent --args @file.py | aider --just-if-new-file --
```

### Export as Standalone Skill
```bash
# Export a template for reuse
pop use project-guidelines --no-copy > ~/.aider.skills/project-guidelines.md
```

### Setting Up Aider with Skills

1. **Create a skills directory**:
   ```bash
   mkdir -p ~/.aider.skills
   ```

2. **Export skills**:
   ```bash
   pop use tdd-workflow --no-copy > ~/.aider.skills/tdd-workflow.md
   pop use refactor-agent --no-copy > ~/.aider.skills/refactor.md
   ```

3. **Use in Aider**:
   ```bash
   # Reference skill file
   aider --prompt ~/.aider.skills/tdd-workflow.md
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

# 3. Paste the hydrated prompt into Aider's chat
```
