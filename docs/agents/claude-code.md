# Using promptbook with Claude Code

the AI agent can be extended via custom MCP servers or simply by piping templates.

## Simple Usage (Piping)
Pipe your code into a promptbook template and send it to the AI agent:
```bash
pop use code-review-security --args "$(cat main.py)" | pbcopy
# Paste into the AI agent
```

## Agentic Workflows
Use specific prompts from `commands/prompts/ai/` to guide the AI agent's agentic behavior.
