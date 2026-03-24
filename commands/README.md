# Commands & Prompt Definitions

This directory contains the prompt templates and command definitions used by the promptbook extension.

## Directory Structure

- `prompts/`: Hierarchical directory containing all 437+ prompt templates in TOML format.
  - `ai/`: Agent orchestration and LLM patterns.
  - `architecture/`: System design and scalable patterns.
  - `database/`: Schema design and query optimization.
  - `engineering/`: Senior developer and implementation guides.
  - `security/`: Threat modeling and security audits.
  - `...and more (Testing, Frontend, Backend, etc.)`

## File Format

Every prompt is defined as a `.toml` file following this schema:

```toml
description = "Concise description"
args_description = "Context-aware input label"
version = "1.0.0"
last_updated = "YYYY-MM-DD"
tags = ["category", "tag2"]
prompt = """
Instructions go here.
{{args}}
"""
```

## Adding a New Prompt

1. Choose the correct category subdirectory in `prompts/`.
2. Use `templates/template.toml` as a base.
3. Name your file according to the prompt slug (e.g., `react-unit-test.toml`).
4. Run `make validate` from the root to ensure your file follows the schema.
