# promptbook

**Promptbook is a structured library of expert prompt templates for AI CLI tools — organized, versioned, and ready to use.**

[![CI](https://github.com/ronmkr/Promptbook/actions/workflows/ci.yml/badge.svg)](https://github.com/ronmkr/Promptbook/actions/workflows/ci.yml)
[![Release](https://github.com/ronmkr/Promptbook/actions/workflows/release.yml/badge.svg)](https://github.com/ronmkr/Promptbook/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Install

### From Source (Rust required)
```bash
git clone https://github.com/ronmkr/PromptBook.git
cd PromptBook
make build
# Binary will be at target/release/pop (CLI) and target/release/promptbook-tui (TUI)
```

## 🛠 Usage

**1. CLI Helper (pop)**
```bash
# List all templates
cargo run --bin pop -- list

# Use a prompt (hydrates variables interactively)
cargo run --bin pop -- use refactor-agent
```

**2. Interactive Explorer (TUI)**
```bash
make tui
```

## 🔍 What is this?

**promptbook** is a curated collection of standardized, high-quality prompt templates designed specifically for **developers, architects, and data engineers**. It provides a unified interface to discover and use prompts across any AI agent or CLI tool (Gemini, Claude Code, Aider, etc.).

Unlike loose collections of snippets, Promptbook treats prompts as **first-class code assets** with metadata, versioning, dynamic context resolution, and conditional extraction.

## 💡 Why do I need it?

- **Consistency**: Stop reinventing the prompt. Use battle-tested templates for security audits, architectural reviews, and debugging.
- **Context Awareness**: Templates use dynamic variables like `{{file}}`, `{{language}}`, and `{{context}}` to inject your project's state automatically.
- **Dynamic Execution**: Pull live system context into your prompts using `{{$(git diff)}}` or `{{env.AWS_REGION}}`.
- **Context Efficiency**: Surgical extraction using `<if language="...">` blocks ensures the AI only sees what it needs, reducing token bloat.
- **Portability**: Write a prompt once, use it everywhere—in your terminal, in your IDE extension, or in web-based LLMs.

## 🖥 What does it look like?

### The TUI Explorer
Lightning-fast fuzzy search and interactive variable hydration directly in your terminal.

![Promptbook TUI Demo](https://raw.githubusercontent.com/ronmkr/Promptbook/main/docs/assets/tui-demo.gif)

*(Run `make tui` to launch)*

### MCP Server (Model Context Protocol)
Expose the entire PromptBook library to AI agents like Claude Desktop or Gemini as **Tools** and **Resources**.

**1. Build the server:**
```bash
make mcp
```

**2. Configure Claude Desktop:**
Add this to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "promptbook": {
      "command": "/absolute/path/to/PromptBook/target/debug/promptbook-mcp",
      "args": []
    }
  }
}
```

**3. AI Tools provided:**
- `list_prompts`: Search and discover templates.
- `get_prompt`: Hydrate and retrieve a prompt (e.g., "Use 'architect' with arguments {'args': 'my app'}")
- **Resources**: Direct access to raw templates via `promptbook://prompts/name` URIs.

### Usage Examples

**1. Security Audit (with Language Context)**
```bash
# Review a Python file for vulnerabilities, ignoring irrelevant logic
pop use security-scan --language python --args @main.py
```

**2. Dynamic Architectural Context**
```bash
# Generate a summary based on the current git state
pop use pr-template --args "{{$(git diff HEAD)}}"
```

**3. Debugging Stack Traces**
```bash
# Analyze a log file to find root cause and suggest fixes
cat server.log | pop use debug-error
```

**4. Context Profiles**
```bash
# Save common variables to a profile and reuse them
pop profile set my-project project=PromptBook lang=python
pop use refactor-agent --profile my-project
```

**5. Prompt Chaining**
```bash
# Chain multiple prompts (output of step 1 becomes input for step 2)
pop chain prompt-specialist refactor-agent --args "initial code"
```

## 🚀 Key Features

- **Context Profiles:** Save and manage named sets of variables to reuse across different prompts.
- **Prompt Chaining:** Create complex multi-step workflows by piping the output of one prompt into the input of the next.
- **Massive Catalog:** 167+ unique prompts across Engineering, Security, AI, DevOps, and specialized developer domains.
- **Secure Vault:** Encrypted storage for API keys using OS-level keyring and AES encryption.
- **Audit Logging:** Compliance-ready tracking of all sensitive prompt executions.
- **PII Masking:** Automatic anonymization of emails, phones, and sensitive data (GDPR ready).
- **Dynamic Context:** Support for dynamic shell execution `{{$(cmd)}}` and environment variables `{{env.VAR}}`.
- **Evaluation Framework:** LLM-as-a-judge golden testing for any OpenAI-compatible provider.
- **Conditional Extraction:** Surgical prompt pruning using `<if language="...">` blocks to minimize context bloat.
- **TUI Browser:** A high-performance Rust-based TUI for browsing and previewing templates.
- **Native Integrations:** First-class support for Gemini CLI, Claude Code, and Aider.

## 🛠 Developer Commands

The project uses a `Makefile` to simplify common development tasks:

| Command | Description |
|---|---|
| `make build` | Build all crates (CLI and TUI) |
| `make test` | Run all unit tests across the workspace |
| `make lint` | Run clippy on all crates |
| `make fmt` | Format all Rust code |
| `make validate` | Validate all prompt templates |
| `make docs` | Synchronize template catalog (CATALOG.md) |
| `make tui` | Launch the TUI Explorer |
| `make mcp` | Build the MCP server |

## 📂 Documentation

- [Full Prompt Catalog](docs/CATALOG.md)
- [Template Changelog (TEMPLATES.md)](TEMPLATES.md)
- [Model Context Protocol (MCP) Guide](docs/agents/mcp.md)
- [Gemini CLI Extension Guide](docs/agents/gemini.md)
- [Claude Code Integration](docs/agents/claude-code.md)
- [Aider & Web-LLM Usage](docs/agents/aider.md)

## 📖 Discovery & Usage

Templates are organized hierarchically in `commands/prompts/`. You can explore them via:

1. **Terminal Overview**: Run `make docs` for a categorized list.
2. **Web Catalog**: Browse the [Full Template Catalog](docs/CATALOG.md) on GitHub.
3. **Interactive TUI**: Run `make tui` for the full browser with syntax previews.
4. **CLI Helper**: Use `pop list` or `pop search <term>`.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new templates to our hierarchical structure.

---
*promptbook is open source under the MIT License.*
