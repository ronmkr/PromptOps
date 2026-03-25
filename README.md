# promptbook
**Promptbook is a structured library of expert prompt templates for AI CLI tools — organized, versioned, and ready to use.**
[![Validated Prompts](https://github.com/ronmkr/promptbook/actions/workflows/validate-prompts.yml/badge.svg)](https://github.com/ronmkr/promptbook/actions/workflows/validate-prompts.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## 🚀 Quick Install
Get up and running in seconds with our universal installer:
```bash
curl -fsSL https://raw.githubusercontent.com/ronmkr/Promptbook/main/scripts/install.sh | bash
# Then run the setup wizard
pop init
```
*This clones the library to `~/.promptbook` and sets up the `pop` alias in `~/.local/bin`.*
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
## 🚀 Key Features
- **Massive Catalog:** 167+ unique prompts across Engineering, Security, AI, DevOps, and specialized developer domains.
- **Secure Vault:** Encrypted storage for API keys using OS-level keyring and AES encryption.
- **Audit Logging:** Compliance-ready tracking of all sensitive prompt executions.
- **PII Masking:** Automatic anonymization of emails, phones, and sensitive data (GDPR ready).
- **Dynamic Context:** Support for dynamic shell execution `{{$(cmd)}}` and environment variables `{{env.VAR}}`.
- **Evaluation Framework:** LLM-as-a-judge golden testing for any OpenAI-compatible provider.
- **Conditional Extraction:** Surgical prompt pruning using `<if language="...">` blocks to minimize context bloat.
- **TUI Browser:** A high-performance Rust-based TUI for browsing and previewing templates.
- **Native Integrations:** First-class support for Gemini CLI, Claude Code, and Aider.
## 🛠 Advanced Features
### 🔒 Secure API Key Vault
Promptbook includes a built-in secure vault to manage your API keys without exposing them in environment variables or history.
```bash
# Store a key securely
pop keys set openai sk-...
# List stored providers
pop keys list
```
### 🎭 PII Masking (GDPR)
Protect sensitive data by masking PII before it's sent to the LLM using the `--mask` flag.
```bash
pop use security-reviewer --args @server_logs.txt --mask
```
### 📜 Audit Logging
All executions of prompts marked as `sensitive` are automatically logged to `~/.promptbook/audit.log` for security auditing and compliance.
### 📊 Golden Test Evaluations
Run automated evaluations using LLM-as-a-judge to ensure prompt quality. Supports OpenAI, Gemini, and local providers (Ollama/Llama.cpp).
```bash
# Run the evaluation suite
make evaluate
```
## 🛠 Installation
### Automated Install (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/ronmkr/Promptbook/main/scripts/install.sh | bash
```
### Manual Installation
```bash
git clone https://github.com/ronmkr/Promptbook.git
cd Promptbook
# Set up dependencies (venv recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Make executable and symlink
chmod +x promptbook
mkdir -p ~/.local/bin
ln -s $(pwd)/promptbook ~/.local/bin/pop
```
## 📂 Documentation
- [Full Prompt Catalog](docs/CATALOG.md)
- [Gemini CLI Extension Guide](docs/agents/gemini.md)
- [Claude Code Integration](docs/agents/claude-code.md)
- [Aider & Web-LLM Usage](docs/agents/aider.md)

## 📖 Discovery & Usage
Templates are organized hierarchically in `commands/prompts/`. You can explore and use them via:

1. **Terminal Overview**: Run `make docs` to see a categorized list of all prompts in your terminal.
2. **Web Catalog**: Browse the [Full Template Catalog](docs/CATALOG.md) on GitHub.
3. **Interactive TUI**: Run `make tui` for a high-performance terminal browser with fuzzy search and syntax previews.
4. **CLI Helper**: Use `pop list` or `pop search <term>` to find templates directly from your shell.

## 🤝 Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new templates to our hierarchical structure.
---
*promptbook is open source under the MIT License.*
