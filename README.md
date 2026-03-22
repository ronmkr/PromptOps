# PromptOps - AI CLI Prompt Template Library

```text
  _____                            _    ____
 |  __ \                          | |  / __ \
 | |__) | __ ___  _ __ ___  _ __  | |_| |  | |_ __  ___
 |  ___/ '__/ _ \| '_ ` _ \| '_ \ | __| |  | | '_ \/ __|
 | |   | | | (_) | | | | | | |_) || |_| |__| | |_) \__ \
 |_|   |_|  \___/|_| |_| |_| .__/  \__|\____/| .__/|___/
                           | |               | |
                           |_|               |_|
```

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub Star](https://img.shields.io/github/stars/ronmkr/PromptOps?style=social)](https://github.com/ronmkr/PromptOps)

> **Overview**: A library of over 55 prompt templates for AI CLI tools. Includes a terminal helper for fuzzy searching, file injection, piped input, and automated clipboard copying. Compatible with Claude Code, Gemini CLI, Aider, and web-based LLMs.

---

## Table of Contents

- [Core Features](#core-features)
- [Usage Instructions](#usage-instructions)
  - [Terminal Helper](#1-terminal-helper)
  - [Gemini CLI Integration](#2-gemini-cli-integration)
  - [Claude Code and Aider](#3-claude-code-and-aider)
- [Available Templates](#available-templates)
- [Extending the Library](#extending-the-library)
- [Contributing and Quality Control](#contributing-and-quality-control)
- [License](#license)

---

## Core Features

- **Standardized Templates**: Over 50 templates for development, architecture, DevOps, and security.
- **Tool-Agnostic**: Compatible with AI CLI tools and standard LLM interfaces.
- **Categorized Library**: Organized by domain (Frontend, Backend, Security, Operations).
- **Version Control**: Templates include version and date metadata for maintenance.
- **Tagging System**: Metadata-based discovery and filtering.
- **Clipboard Integration**: Output is automatically copied to the system clipboard.
- **Sensitive Data Protection**: Prompts marked as `sensitive` require explicit confirmation before copying.
- **Extensible**: TOML-based structure for adding or modifying templates.

---

## Prerequisites

Before using the PromptOps library, ensure your environment meets the following requirements:

- **Python 3.11+**: Required for the core CLI helper (`promptops`).
- **Rust (Cargo)**: Required only if you want to use the high-performance **TUI Browser**.
- **Linux Users**: To use the clipboard functionality, you must have `xclip` or `xsel` installed:
  ```bash
  sudo apt install xclip  # Debian/Ubuntu
  sudo pacman -S xclip    # Arch
  ```

---

## Usage Instructions

### 1. TUI Browser (Recommended)

The PromptOps TUI is a high-performance Rust-based terminal interface for browsing and using prompts with real-time fuzzy search and syntax-highlighted previews.

**Launch the TUI:**

```bash
make tui
```

**Key Features:**
- **Global Search**: Press `/` to search across all 55+ prompts instantly.
- **Interactive Hydration**: Sequential input for template variables (e.g., `{{args}}`, `{{code}}`).
- **Security Confirmation**: Automatic `[y/n]` confirmation modal for sensitive prompts.
- **Live Preview**: Press `v` to toggle syntax highlighting for prompt templates.
- **Auto-Copy**: Final hydrated prompts are automatically copied to your system clipboard.

---

### 2. Terminal Helper

The `promptops` (aliased as `pop`) utility provides access to the template library.

**Installation:**

```bash
git clone https://github.com/ronmkr/PromptOps.git
cd PromptOps
chmod +x promptops
# Optional: link to /usr/local/bin
sudo ln -s $(pwd)/promptops /usr/local/bin/pop
```

**Shell Auto-Completion:**

- **Zsh**: `source <(pop completion zsh)`
- **Bash**: `source <(pop completion bash)`
- **Fish**: `pop completion fish | source`

**Basic Commands:**

- `pop list`: List all templates.
- `pop list --tag <tag>`: Filter by category.
- `pop search <term>`: Search by name or description.
- `pop use <tool>`: Run a template interactively.
- `pop use <tool> --no-copy`: Disable automatic clipboard copying.
- `pop use <tool> -y`: Auto-confirm sensitive prompt warnings.
- `pop use <tool> --args @file.py`: Inject file content directly.
- `cat file.py | pop use <tool>`: Use piped input.

---

### 2. Gemini CLI Integration

PromptOps functions as a native extension for the Gemini CLI.

```bash
gemini extensions install https://github.com/ronmkr/PromptOps.git
```

Once installed, use the `/prompts:` namespace:

```bash
/prompts:suggest-fixes "code snippet"
```

---

### 3. Claude Code and Aider

For tools without native extension support, templates can be provided as context.

```bash
# Claude Code
claude "Read commands/prompts/design-api.toml and design a REST API"

# Aider
/read commands/prompts/security-policy.toml
```

---

## Available Templates

Templates are categorized by domain. Click a category to view its full reference notebook.

### [Code Review & Analysis](docs/catalog/code-review-and-analysis.ipynb)
- `/prompts:code-review-best-practices` - General best practices review
- `/prompts:code-review-performance` - Performance optimization suggestions
- `/prompts:code-review-security` - Deep security analysis of code
- `/prompts:debug-error` - Help diagnose and fix errors
- `/prompts:explain-code` - Detailed code explanation
- `/prompts:performance-profile` - Analyze performance profiles
- `/prompts:refactor-suggestions` - Code refactoring recommendations
- `/prompts:suggest-fixes` - Suggest potential bug fixes and improvements for code
- `/prompts:trace-issue` - Trace the root cause of issues

### [DevOps & Infrastructure](docs/catalog/devops-and-infrastructure.ipynb)
- `/prompts:bash-script-generator` - Write robust, POSIX-compliant bash scripts
- `/prompts:ci-cd-pipeline` - Generate CI/CD pipelines (GitHub Actions, GitLab CI, etc.)
- `/prompts:dockerfile-generator` - Generate optimized, production-ready Dockerfiles
- `/prompts:iam-policy` - Generate AWS IAM or GCP resource policies with least privilege
- `/prompts:kubernetes-manifest` - Create Kubernetes Deployment and Service YAML manifests
- `/prompts:terraform-module` - Write Infrastructure-as-Code Terraform modules

### [Security & Compliance](docs/catalog/security-and-compliance.ipynb)
- `/prompts:accessibility-audit` - Review HTML/React code for WCAG compliance
- `/prompts:code-review-security` - Deep security analysis of code
- `/prompts:dependency-audit` - Analyze a package.json or requirements.txt for known vulnerable patterns
- `/prompts:iam-policy` - Generate AWS IAM or GCP resource policies with least privilege
- `/prompts:security-policy` - Draft a SECURITY.md or vulnerability disclosure policy
- `/prompts:threat-modeling` - Generate a STRIDE threat model for a proposed architecture

### [Database & Data Engineering](docs/catalog/database-and-data-engineering.ipynb)
- `/prompts:design-database` - Design database schemas
- `/prompts:migration-script` - Generate safe up/down database migration scripts
- `/prompts:mock-data-gen` - Create realistic JSON/CSV mock data schemas for testing
- `/prompts:regex-builder` - Generate and explain complex Regular Expressions
- `/prompts:sql-optimizer` - Analyze slow queries and suggest indexes or rewrites

### [Testing & Debugging](docs/catalog/testing-and-debugging.ipynb)
- `/prompts:debug-error` - Help diagnose and fix errors
- `/prompts:generate-e2e-tests` - Create end-to-end tests
- `/prompts:generate-unit-tests` - Create unit tests for code
- `/prompts:performance-profile` - Analyze performance profiles
- `/prompts:review-test-coverage` - Analyze test coverage gaps
- `/prompts:suggest-fixes` - Suggest potential bug fixes and improvements for code
- `/prompts:test-edge-cases` - Identify and test edge cases
- `/prompts:trace-issue` - Trace the root cause of issues

### [UI / UX & Frontend](docs/catalog/ui-ux-and-frontend.ipynb)
- `/prompts:accessibility-audit` - Review HTML/React code for WCAG compliance
- `/prompts:component-story` - Generate Storybook stories for UI components
- `/prompts:css-tailwind-converter` - Convert standard CSS to Tailwind utility classes

### [Architecture & Design](docs/catalog/architecture-and-design.ipynb)
- `/prompts:design-api` - Design RESTful APIs
- `/prompts:design-database` - Design database schemas
- `/prompts:design-patterns` - Suggest appropriate design patterns
- `/prompts:system-architecture` - Design system architecture
- `/prompts:threat-modeling` - Generate a STRIDE threat model for a proposed architecture

### [Shell & Scripting](docs/catalog/shell-and-scripting.ipynb)
- `/prompts:bash-script-generator` - Write robust, POSIX-compliant bash scripts
- `/prompts:cli-command-explainer` - Deeply explain obscure terminal commands/flags
- `/prompts:git-workflow` - Suggest Git commands to recover from complex merge/rebase states
- `/prompts:regex-builder` - Generate and explain complex Regular Expressions

### [Project Management & Agile](docs/catalog/project-management-and-agile.ipynb)
- `/prompts:pr-template` - Generate a Pull Request template for a repository
- `/prompts:sprint-retrospective` - Analyze sprint data and generate a summary
- `/prompts:ticket-generator` - Convert a loose idea into a structured Jira/Linear ticket

### [Documentation & Learning](docs/catalog/documentation-and-learning.ipynb)
- `/prompts:compare-technologies` - Compare different technologies
- `/prompts:eli5` - Explain like I'm 5 (simple explanations)
- `/prompts:explain-concept` - Explain technical concepts clearly
- `/prompts:learning-path` - Create learning roadmaps
- `/prompts:pr-template` - Generate a Pull Request template for a repository
- `/prompts:prompt-best-practices` - Learn prompt engineering tips
- `/prompts:prompt-versioning` - Guide for managing and versioning prompt templates
- `/prompts:security-policy` - Draft a SECURITY.md or vulnerability disclosure policy
- `/prompts:simplify-jargon` - Simplify technical jargon
- `/prompts:write-api-docs` - Create API documentation
- `/prompts:write-changelog` - Generate changelog from changes
- `/prompts:write-contributing` - Create CONTRIBUTING.md guidelines
- `/prompts:write-email` - Draft professional emails
- `/prompts:write-inline-comments` - Add helpful code comments
- `/prompts:write-presentation` - Create presentation outlines
- `/prompts:write-readme` - Generate comprehensive README files
- `/prompts:write-technical-blog` - Write technical blog posts

## Extending the Library

PromptOps templates are defined in TOML and support dynamic data injection.

### Supported Variables

Templates utilize the following placeholders for context injection:

- `{{args}}`: Primary input placeholder.
- `{{code}}`: Snippet-specific placeholder.
- `{{file}}`: Complete file content placeholder.
- `{{language}}`: Contextual language placeholder.

### Creating a New Template

1. Create a `.toml` file in `commands/prompts/` (e.g., `my-tool.toml`).
2. Use the following structure:

````toml
description      = "A concise description ending with a period."
args_description = "A label for the input (e.g., 'Source Code')."
version          = "1.0.0"
last_updated     = "2026-03-21"
tags             = ["category"]
sensitive        = true  # Optional: Mark as sensitive to enable confirmation warnings

prompt           = """
# Template Title
Your detailed instructions for the AI model...

```
{{args}}
```
"""
````

3. Validate the template by running `make validate`.

---

## Contributing and Quality Control

Consult [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

**Automated Checks:**

- **Metadata Validation**: Ensures TOML syntax and required fields are present.
- **Logic Tests**: Verifies CLI helper functionality.
- **Catalog Sync**: Ensures domain notebooks remain updated.

**Run Tests Locally:**

```bash
make validate
make test
```

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) file for details.

---

Inspired by the [gemini-cli-prompt-library](https://github.com/harish-garg/gemini-cli-prompt-library) by Harish Garg.
