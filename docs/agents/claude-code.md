# Using promptbook with Claude Code

The AI agent can be extended via custom MCP servers or simply by piping templates.

## Simple Usage (Piping)
Pipe your code into a promptbook template and send it to the AI agent:
```bash
pop use code-review-security --args "$(cat main.py)" | pbcopy
# Paste into the AI agent
```

## Agentic Workflows
Use specific prompts from `commands/prompts/ai/` to guide the AI agent's agentic behavior.

---

## Using Promptbook as Skills

PromptBook templates work as reusable skills for Claude Code. Here's how to use them:

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
# Export a template as a Claude Code-compatible skill
pop use project-guidelines --no-copy > ~/.claude/skills/project-guidelines.md
```

### Setting Up in Claude Code

1. **Create a skills directory**:
   ```bash
   mkdir -p ~/.claude/skills
   ```

2. **Export skills**:
   ```bash
   pop use tdd-workflow --no-copy > ~/.claude/skills/tdd-workflow.md
   pop use security-scan --no-copy > ~/.claude/skills/security-scan.md
   pop use code-reviewer-agent --no-copy > ~/.claude/skills/code-review.md
   ```

3. **Reference in conversations**:
   Use `@skill-name` or paste the hydrated prompt directly.

### Available Skill Categories

| Category | Use Case |
|----------|----------|
| `engineering/` | Code review, refactoring, debugging |
| `security/` | Security audits, threat modeling |
| `testing/` | TDD, E2E, test generation |
| `architecture/` | System design, ADRs |
| `ai-agents/` | Agentic workflows, MCP, eval |
| `<language>-specialist/` | Language-specific patterns |

### Example Workflow
```bash
# 1. Find a skill
pop search "code review"

# 2. Use it with your code
pop use code-reviewer-agent --language python --args @src/main.py

# 3. Paste the hydrated prompt into Claude Code
```

### Recommended Skills for Claude Code

- `code-reviewer-agent` — Comprehensive code review
- `security-scan` — Security vulnerability detection
- `refactor-agent` — Safe refactoring suggestions
- `tdd-workflow` — Test-driven development
- `error-resolution-agent` — Debugging and error fixes
- `mcp-master` — MCP server design
