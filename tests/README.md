# Testing promptbook

This directory contains test suites and golden datasets for validating the promptbook library.

## Contents

- `test_features_extended.py`: Functional tests for prompt discovery, variable injection, and CLI features.
- `golden_datasets/`: Curated input/output examples for prompt quality evaluation.

## Running Tests

To run the functional tests:
```bash
pytest tests/
```

To run a single test file:
```bash
python tests/test_features_extended.py
```
