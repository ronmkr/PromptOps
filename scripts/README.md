# promptbook Scripts & Core Logic

This directory contains the Python core and CLI logic for the promptbook extension, along with maintenance scripts for the prompt library.

## Directory Structure

- `promptbook/`: Python package containing core library logic.
  - `cli.py`: Command-line interface logic.
  - `core.py`: Library functions (discovery, parsing, injection).
  - `ui.py`: CLI formatting and terminal colors.
  - `utils.py`: Constants and shared utilities.
- `evaluate_prompts.py`: Script to run automated evals for prompt quality.
- `sync_all_docs.py`: Syncs catalog notebooks with current prompt files.
- `validate_prompts.py`: Schema validation for TOML prompt files.
- `test_promptbook.py`: Functional tests for the CLI helper.
- `install.sh`: Universal one-line installer for the library and CLI.

## Requirements

The scripts require Python 3.11+ for `tomllib` support.

Install dependencies:
```bash
pip install -r ../requirements.txt
```

## Running Evals

To evaluate prompt quality using a model:
```bash
python scripts/evaluate_prompts.py
```

## Validating Prompts

Ensure all prompts in `commands/prompts/` follow the schema:
```bash
python scripts/validate_prompts.py
```
