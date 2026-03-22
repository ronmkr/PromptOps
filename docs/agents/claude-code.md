# Using PromptOps with Claude Code

Claude Code can be extended via custom MCP servers or simply by piping templates.

## Simple Usage (Piping)
Pipe your code into a PromptOps template and send it to Claude Code:
```bash
pop use code-review-security --args "$(cat main.py)" | pbcopy
# Paste into Claude Code
```

## Agentic Workflows
Use specific prompts from `commands/prompts/ai/` to guide Claude Code's agentic behavior.
