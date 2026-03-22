# PromptOps: The Universal Prompt Library for AI Agents

PromptOps is a curated collection of 437+ standardized, high-quality prompt templates designed for developers, architects, and AI engineers. It provides a unified interface to discover and use prompts across any AI agent.

## 🚀 Key Features

- **Massive Catalog:** 437 unique prompts across 16+ categories (Engineering, Security, AI, DevOps, etc.).
- **TUI Explorer:** High-performance terminal UI for lightning-fast search and discovery.
- **Agent Agnostic:** Specialized guides for Gemini, Cursor, Claude Code, Aider, and more.
- **Standardized Schema:** Every prompt includes metadata, versioning, and context-aware variable injection.

## 🛠 Installation

```bash
git clone https://github.com/your-repo/PromptOps.git
cd PromptOps
pip install -r requirements.txt
alias pop="$(pwd)/promptops"
```

## 📖 Usage

### Launch the Explorer
```bash
pop
```

### Search via CLI
```bash
pop search "security audit"
```

### Use in Gemini CLI
```bash
/prompts:code-review-security {{file}}
```

## 📂 Documentation

- [Full Prompt Catalog](docs/catalog/FULL_CATALOG.md)
- **Agent How-To Guides:**
  - [Gemini CLI](docs/agents/gemini.md)
  - [Cursor](docs/agents/cursor.md)
  - [Claude Code](docs/agents/claude-code.md)
  - [Aider](docs/agents/aider.md)
  - [GitHub Copilot / Codex](docs/agents/codex.md)
  - [Windsurf](docs/agents/windsurf.md)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new templates to our hierarchical structure.

## 📜 Acknowledgements

PromptOps is inspired by and incorporates patterns from these excellent community resources:
- [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
- [harish-garg/gemini-cli-prompt-library](https://github.com/harish-garg/gemini-cli-prompt-library)
