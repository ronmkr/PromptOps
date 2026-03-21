# 📚 PromptOps - Universal AI CLI Prompt Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Star](https://img.shields.io/github/stars/ronmkr/PromptOps?style=social)](https://github.com/ronmkr/PromptOps)

A curated, tool-agnostic library of high-quality, professionally crafted prompts for modern development workflows. Works seamlessly with **Gemini CLI**, **Claude Code**, **Aider**, and other AI coding assistants.

---

## ✨ Key Features

- 🎯 **50+ Expert Prompts**: Battle-tested templates for coding, architecture, DevOps, and security.
- 🚀 **Tool-Agnostic**: Use with any AI CLI or LLM interface (Claude, Gemini, Aider, etc.).
- 🎨 **Domain Specific**: Categorized libraries for Frontend, Backend, Security, and Project Management.
- 📦 **Prompt Versioning**: Every prompt is versioned and tracked for better maintenance.
- 🏷️ **Tagging System**: Robust metadata and tagging for easy discovery and filtering.
- 🔧 **Customizable**: Simple TOML-based structure for easy modification and expansion.

---

## 📦 How to Use PromptOps

PromptOps is designed to work wherever you do. You can use it as a standalone terminal utility or integrate it directly into your favorite AI tool.

### 1. The PromptOps CLI Helper (Recommended)
We provide a zero-dependency Python script (`promptops`) that makes finding and using prompts incredibly fast.

**Setup the CLI:**
```bash
# Clone the repository
git clone https://github.com/ronmkr/PromptOps.git
cd PromptOps

# Make it executable
chmod +x promptops

# (Optional) Add it to your PATH for global access
sudo ln -s $(pwd)/promptops /usr/local/bin/pop
```

**Using the CLI:**
- **Search & Discover:**
  - `pop list` - List all available prompts.
  - `pop search "docker"` - Fuzzy search for prompts related to Docker.
  - `pop tags` - View all available categories (e.g., `security`, `frontend`).
- **Interactive Injection:**
  - `pop use suggest-fixes` - The CLI will detect variables like `{{args}}` and ask you to paste your code interactively.
- **Piping to AI (The Magic Workflow):**
  - `pop use dockerfile-generator --args "Python FastAPI app" | claude`
  - `pop use code-review-security --args "$(cat main.py)" | aider`

### 2. Using with Gemini CLI
PromptOps acts as a native extension for Gemini CLI.
```bash
gemini extensions install ronmkr/PromptOps
```
Once installed, all prompts are available via the `/prompts:` namespace. 
*Example: `/prompts:suggest-fixes "print('hello')"`*

### 3. Using with Claude Code & Aider
If you don't use the CLI helper, you can pass the `.toml` templates directly to your AI as context.
```bash
# Claude Code
claude "Read commands/prompts/design-api.toml and design an API for a blog"

# Aider
/read commands/prompts/security-policy.toml
```

---

## 📋 Available Prompts

Prompts are stored as `.toml` files in `commands/prompts/`. 

**For a full reference of all prompt templates and their content, see our [Prompt Catalog](CATALOG.md).**

### 🔍 Highlights:
- **Code Review**: `code-review-security`, `suggest-fixes`, `explain-code`.
- **DevOps**: `dockerfile-generator`, `kubernetes-manifest`, `ci-cd-pipeline`.
- **Security**: `threat-modeling`, `security-policy`, `iam-policy`.
- **Database**: `sql-optimizer`, `migration-script`, `design-database`.
- **Frontend**: `css-tailwind-converter`, `accessibility-audit`, `component-story`.
- **Prompt Engineering**: `improve-prompt`, `prompt-versioning`, `create-prompt-template`.

---

## 🛠️ How to Add New Prompts (Customization)

PromptOps is designed to be easily extensible. All prompts are stored as simple `.toml` files in the `commands/prompts/` directory.

### 📋 Supported Variables
You can inject dynamic user input into your templates using these standard variables:
- `{{args}}` (Primary): The user's direct input or argument.
- `{{code}}`: Specifically for code snippets.
- `{{file}}`: The full content of a file.
- `{{language}}`: The target programming language.
- `{{context}}`: Any additional metadata.

### Step-by-Step: Creating a Prompt
1. **Create the file**: Create a new file like `commands/prompts/my-new-tool.toml`.
2. **Use the Template**: Copy the structure from our [starter template](templates/template.toml).
3. **Fill in the Metadata & Prompt**:
```toml
description  = "A short, one-sentence description ending in a period."
version      = "1.0.0"
last_updated = "2026-03-21"
tags         = ["custom", "development"]

prompt       = """
  # Your Expert Prompt Title
  
  Act as a senior engineer. Please analyze the following input and provide feedback:
  
  ```
  {{args}}
  ```
  
  Please format your output with Markdown headers.
"""
```
4. **Validate**: Run `make validate` to ensure your new prompt meets the PromptOps syntax and metadata standards.
5. **Use it**: It is immediately available via `pop use my-new-tool` or `/prompts:my-new-tool`.

---

## 🤝 Contributing

Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) guide for detailed instructions on adding new prompt templates and categories.

---

## 🤖 CI/CD & Quality Control

PromptOps includes automated quality checks to ensure consistency:
- **Metadata Validation**: Every PR is checked for valid TOML, versioning, and required fields.
- **CLI Logic Tests**: Automated tests for fuzzy search, filtering, and variable injection.
- **Catalog Auto-Sync**: The `CATALOG.md` is automatically verified to be in sync with templates.

Run tests locally:
```bash
make validate
make test
make catalog
# Or run everything
make all
```

---

## 🙏 Acknowledgments

- Inspired by the [gemini-cli-prompt-library](https://github.com/harish-garg/gemini-cli-prompt-library) by Harish Garg.
- Built on modern prompt engineering best practices.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Made with ❤️ for the AI CLI community**
[![GitHub Star](https://img.shields.io/github/stars/ronmkr/PromptOps?style=social)](https://github.com/ronmkr/PromptOps)
