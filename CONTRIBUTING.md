# Contributing to promptbook
Thank you for your interest in contributing to promptbook. We welcome contributions, from new prompt templates to improvements in existing ones.
---
## Table of Contents
- [Contributing to promptbook](#contributing-to-promptbook)
  - [Table of Contents](#table-of-contents)
  - [How to Contribute](#how-to-contribute)
    - [1. Adding a New Prompt Template](#1-adding-a-new-prompt-template)
    - [2. Improving Existing Prompts](#2-improving-existing-prompts)
    - [3. Documentation Synchronization](#3-documentation-synchronization)
  - [Validation Rules](#validation-rules)
  - [Prompt Variables](#prompt-variables)
  - [Development Workflow](#development-workflow)
    - [Golden Tests (Optional)](#golden-tests-optional)
  - [License](#license)
---
## How to Contribute
### 1. Adding a New Prompt Template
All prompts are stored as `.toml` files in the `commands/prompts/` directory.
To add a new prompt:
1.  Create a new file with a descriptive, dash-separated name (e.g., `my-new-tool.toml`).
2.  Use the [starter template](templates/template.toml).
3.  Follow the required structure below:
````toml
description      = "A short, one-sentence description ending with a period."
args_description = "A friendly label for the main input (e.g. 'Source Code')."
version          = "1.0.0"
last_updated     = "2026-03-21"
tags             = ["category"]
prompt           = """
# Template Title
Instructions...
```
{{args}}
```
"""
````
### 2. Improving Existing Prompts
- Ensure changes maintain the standardized tone of the library.
- When making logic changes, increment the version following Semantic Versioning (SemVer) and update the `last_updated` date.
- Use the `/prompts:prompt-versioning` tool for guidance on managing prompt lifecycles.
### 3. Documentation Synchronization
If you add a new prompt or category, ensure it is correctly listed in:
- `GEMINI.md` (for Gemini CLI extension users).
- `README.md` (under the "Available Templates" section).
---
## Validation Rules
To maintain consistency, all prompts must follow these rules:
- **Naming**: File names must be `kebab-case.toml`.
- **Description**: Maximum 150 characters, must end with a period.
- **Versioning**: Follow [Semantic Versioning](https://semver.org/).
- **Date**: Use `YYYY-MM-DD` format.
- **Tags**: Must be lowercase, no spaces, and non-empty.
- **Content**: Must start with a Markdown header `#` and include at least one variable like `{{args}}`.
---
## Prompt Variables
promptbook supports a set of variables that are substituted when the prompt is executed:
- `{{args}}` (Primary): The user's input/argument provided when calling the prompt.
- `{{code}}`: Specifically for passing code snippets to be analyzed.
- `{{file}}`: The full content of a file.
- `{{language}}`: The programming language of the context.
- `{{context}}`: Additional project or system context.
> **Note**: In most CLI tools, `{{args}}` is the default variable for input provided after the command name.
---
## Development Workflow
1.  **Fork the Repository**: Create your own copy of promptbook.
2.  **Create a Feature Branch**: `git checkout -b feature/your-feature-name`.
3.  **Setup Your Environment**: Install dependencies and pre-commit hooks to automate validation:
    ```bash
    make setup
    ```
    This will ensure that Python linting (ruff), prompt metadata validation, and Rust formatting are automatically checked whenever you commit.
4.  **Validate Locally**: You can also run individual checks manually:
    ```bash
    make validate # Check prompt metadata
    make lint     # Run all linters (Python & Rust)
    make test     # Run unit tests
    make docs     # Synchronize documentation
    ```
### Golden Tests (Optional)
If you are making significant changes to a prompt's logic, evaluate its quality using the evaluation framework.
1.  Install testing dependencies: `pip install -r requirements.txt`
2.  Set your Google Gemini API key: `export GEMINI_API_KEY="your-api-key"`
3.  Run the evaluations: `make evaluate`
This tests the prompts against predefined cases in `tests/golden_datasets/`.
4.  **Commit Your Changes**: Use clear, descriptive commit messages (e.g., `feat: add docker-compose-generator prompt`).
5.  **Submit a Pull Request**: Provide a clear description of the new prompt and its intended use case.
---
## License
By contributing, you agree that your contributions will be licensed under the project's MIT License.
