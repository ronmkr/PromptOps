# Contributing to PromptOps

Thank you for your interest in contributing to PromptOps. We welcome contributions, from new prompt templates to improvements in existing ones.

## How to Contribute

### 1. Adding a New Prompt Template
All prompts are stored as `.toml` files in the `commands/prompts/` directory.

To add a new prompt:
1. Create a new file with a descriptive, dash-separated name (e.g., `my-new-tool.toml`).
2. Use the starter template: [templates/template.toml](templates/template.toml).
3. Follow the required structure below:

```toml
description      = "A short, one-sentence description ending with a period."
args_description = "A friendly label for the main input (e.g. 'Source Code')."
version          = "1.0.0"
last_updated     = "2026-03-21"
tags             = ["category1", "category2"]

prompt           = \"\"\"
  # Template Title
  Instructions...
  ```
  {{args}}
  ```
\"\"\"
```

### Validation Rules
To maintain consistency, all prompts must follow these rules:
- **Naming**: File names must be `kebab-case.toml`.
- **Description**: Maximum 150 characters, must end with a period.
- **Versioning**: Follow [Semantic Versioning](https://semver.org/).
- **Date**: Use `YYYY-MM-DD` format.
- **Tags**: Must be lowercase, no spaces, and non-empty.
- **Content**: Must start with a Markdown header `#` and include at least one variable like `{{args}}`.

### Prompt Variables
PromptOps supports a set of variables that are substituted when the prompt is executed:

- `{{args}}` (Primary): The user's input/argument provided when calling the prompt.
- `{{code}}`: Specifically for code snippets.
- `{{file}}`: The full content of a file.
- `{{language}}`: The programming language of the context.
- `{{context}}`: Additional project or system context.

Note: In most CLI tools, `{{args}}` is the default variable for input provided after the command name.

### 2. Improving Existing Prompts
- Ensure changes maintain the standardized tone of the library.
- When making logic changes, increment the version following Semantic Versioning (SemVer) and update the `last_updated` date.
- Use the `/prompts:prompt-versioning` tool for guidance on managing prompt lifecycles.

### 3. Documentation Sync
If you add a new prompt or category, ensure it is correctly listed in:
- `GEMINI.md` (for Gemini CLI extension users).
- `README.md` (under the "Available Prompts" section).

---

## Development Workflow

1. **Fork the Repository**: Create your own copy of PromptOps.
2. **Create a Feature Branch**: `git checkout -b feature/your-feature-name`.
3. **Validate Your Prompt**: Use the automated validation script to ensure prompts meet project standards. Run it locally using the `Makefile`:
```bash
make validate
```

You can also run tests and synchronize documentation:
```bash
make test
make docs
```

### 4. Golden Tests (Optional)
If you are making significant changes to a prompt's logic, evaluate its quality using the evaluation framework.
1. Install testing dependencies: `pip install -r requirements.txt`
2. Set your Google Gemini API key: `export GEMINI_API_KEY="your-api-key"`
3. Run the evaluations: `make evaluate`
This tests the prompts against predefined cases in `tests/golden_datasets/`.

5. **Commit Your Changes**: Use clear, descriptive commit messages (e.g., `feat: add docker-compose-generator prompt`).
6. **Submit a Pull Request**: Provide a clear description of the new prompt and its intended use case.

## License
By contributing, you agree that your contributions will be licensed under the project's MIT License.
