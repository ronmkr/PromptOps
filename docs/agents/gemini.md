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
