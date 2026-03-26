# promptbook Testing Framework

This directory contains the organized test suites for the promptbook library and TUI.

## Directory Structure

- `python/`: Modular Python test suites.
  - `unit/`: Unit tests for core engine components (Discovery, Hydration, Session).
  - `integration/`: End-to-end integration tests for CLI commands and high-level features.
  - `metadata/`: Validation tests for prompt template TOML schema and metadata.
- `golden_datasets/`: Curated input/output datasets used for LLM-as-a-judge quality evaluations.

## Running Tests

### Python Tests
The easiest way to run all Python tests is via the root Makefile:
```bash
make test
```

Alternatively, you can run specific categories using `unittest` discovery:
```bash
# Run all unit tests
python3 -m unittest discover -s tests/python/unit

# Run all integration tests
python3 -m unittest discover -s tests/python/integration
```

### Rust TUI Tests
Unit tests for the Rust TUI are located within the `promptbook-tui/src` directory.
```bash
make rust-test
# or
cd promptbook-tui && cargo test
```

## Writing New Tests
- **Unit Tests**: Add to `tests/python/unit/` for logic that doesn't require complex state or filesystem interaction.
- **Integration Tests**: Add to `tests/python/integration/` for features involving CLI flags, interactive input, or multiple package components.
- **Metadata Tests**: Add to `tests/python/metadata/` for schema-related validation.
