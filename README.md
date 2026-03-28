# promptbook — AI CLI Prompt Template Library

[![Web Explorer](https://img.shields.io/badge/Browse-Web%20Explorer-blue?style=for-the-badge&logo=github)](https://ronmkr.github.io/PromptBook/)
[![CI](https://github.com/ronmkr/Promptbook/actions/workflows/ci.yml/badge.svg)](https://github.com/ronmkr/Promptbook/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Promptbook is a structured library of expert prompt templates for AI CLI tools — organized, versioned, and ready to use.**

Browse, search, and hydrate prompts directly in your browser without any installation:
**[https://ronmkr.github.io/PromptBook/](https://ronmkr.github.io/PromptBook/)**

- **Searchable Interface:** Instantly find prompts by name, tag, or category.
- **Web-Only Workflow:** Paste your code/context directly in the browser.
- **Instant Hydration:** Copy fully hydrated, LLM-ready prompts with one click.
- **Zero Config:** Works in any browser, no CLI setup required.

---

## 🔍 What is this?

**promptbook** is a curated collection of standardized, high-quality prompt templates designed specifically for **developers, architects, and data engineers**. It provides a unified interface to discover and use prompts across any AI agent or CLI tool (Gemini, Claude Code, Aider, etc.).

Unlike loose collections of snippets, Promptbook treats prompts as **first-class code assets** with metadata, versioning, and client-side hydration logic.

## 🚀 Key Features

- **Massive Catalog:** Unique prompts across Engineering, Security, AI, DevOps, and specialized developer domains.
- **Client-Side Hydration:** Input your arguments directly in the web UI to generate ready-to-use prompts.
- **Universal Compatibility:** Prompts work with any LLM (Claude, GPT-4, Gemini, Llama).
- **PII Masking:** Built-in protection for emails, phone numbers, and sensitive data (GDPR ready).
- **Context Profiles:** Save and manage named sets of variables to reuse across different prompts.
- **TUI & CLI Explorer:** High-performance Rust-based tools for terminal power users.

## 🛠 Usage

### 1. Web (Fastest)
Visit the [Promptbook Explorer](https://ronmkr.github.io/PromptBook/), select a prompt, paste your context into the arguments field, and click **Copy**.

### 2. Terminal (Power Users)
If you prefer working in the terminal, you can use the Rust-based TUI or CLI helper.

#### Quick Install
```bash
git clone https://github.com/ronmkr/PromptBook.git
cd PromptBook
make build
# Binary will be at target/release/pop
```

#### Interactive TUI
```bash
make tui
```

#### CLI Helper (`pop`)
```bash
# Search for a prompt
pop search "code review"

# Use it with your code
pop use code-reviewer-agent --language python --args @src/main.py
```

## 🖥 What does it look like?

### Web Explorer
Modern, dark-mode interface for rapid prompt discovery and hydration.
[https://ronmkr.github.io/PromptBook/](https://ronmkr.github.io/PromptBook/)

### Terminal TUI
Lightning-fast fuzzy search and interactive variable hydration directly in your terminal.
*(Run `make tui` to launch)*

---

## 🛠 Developer Commands

The project uses a `Makefile` to simplify common development tasks:

| Command | Description |
|---|---|
| `make build` | Build all crates (CLI and TUI) |
| `make test` | Run all unit tests across the workspace |
| `make lint` | Run clippy on all crates |
| `make validate` | Validate all prompt templates |
| `make docs` | Synchronize template catalog (CATALOG.md) |
| `make tui` | Launch the TUI Explorer |

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new templates to our hierarchical structure.

---
*promptbook is open source under the MIT License.*
