# promptbook Makefile

.PHONY: help test validate docs evaluate all clean sync-version tui lint fmt setup

help:
	@echo "promptbook Developer Tools"
	@echo "-------------------------"
	@echo "make setup     - Install dependencies and pre-commit hooks"
	@echo "make validate  - Run metadata and structure validation on all prompts"
	@echo "make test      - Run logic and validation unit tests"
	@echo "make lint      - Run linting checks (Python & Rust)"
	@echo "make fmt       - Format code (Python & Rust)"
	@echo "make docs      - Synchronize all documentation and catalogs"
	@echo "make evaluate  - Run Golden Tests using LLM-as-a-judge (Supports OpenAI/Gemini)"
	@echo "make all       - Run validation, tests, linting, and sync documentation"
	@echo "make tui       - Build and run the Rust-based TUI browser"
	@echo "make clean     - Remove temporary files and __pycache__"

setup:
	@echo "Installing Python dependencies..."
	@python3 -m pip install -r requirements.txt
	@echo "Installing pre-commit hooks..."
	@pre-commit install

validate:
	@echo "Validating prompt metadata..."
	@python3 scripts/validate_prompts.py

lint:
	@echo "Running Python linting (ruff)..."
	@ruff check .
	@echo "Running Rust linting (clippy)..."
	@cd promptbook-tui && cargo clippy -- -D warnings
	@echo "Checking Rust formatting..."
	@cd promptbook-tui && cargo fmt -- --check

fmt:
	@echo "Formatting Python code (ruff)..."
	@ruff format .
	@echo "Formatting Rust code (cargo fmt)..."
	@cd promptbook-tui && cargo fmt

test:
	@echo "Running CLI helper tests..."
	@python3 scripts/test_promptbook.py
	@echo "Running validation unit tests..."
	@python3 scripts/test_validation.py

docs:
	@echo "Syncing all documentation..."
	@python3 scripts/sync_all_docs.py

evaluate:
	@echo "Running Golden Test evaluation..."
	@python3 scripts/evaluate_prompts.py

check-sync: docs
	@if [ -n "$$(git status --porcelain docs/catalog/ README.md GEMINI.md CLAUDE.md prompts.json)" ]; then \
		echo "Error: Documentation catalogs, README, or registry are out of sync!"; \
		echo "Please run 'make docs' locally and commit the changes."; \
		git diff docs/catalog/ README.md GEMINI.md CLAUDE.md prompts.json; \
		exit 1; \
	fi
	@echo "✅ All documentation is in sync."

sync-version:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is not set. Usage: make sync-version VERSION=0.0.x"; \
		exit 1; \
	fi
	@echo "Syncing all versions to $(VERSION)..."
	@python3 scripts/sync_all_versions.py $(VERSION)

all: validate test lint docs check-sync
	@echo "✅ All checks passed and documentation synchronized."

tui:
	@echo "Building and running Rust TUI..."
	@cd promptbook-tui && cargo run --release

clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf scripts/__pycache__
	@rm -rf scripts/promptbook/__pycache__
	@rm -f scripts/tmp_*
