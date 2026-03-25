# promptbook Makefile

.PHONY: help test validate docs evaluate all clean sync-version tui lint fmt setup rust-build rust-test release check-sync

help:
	@echo "promptbook Developer Tools"
	@echo "-------------------------"
	@echo "make setup        - Install dependencies and pre-commit hooks"
	@echo "make validate     - Run metadata and structure validation on all prompts"
	@echo "make test         - Run logic and validation unit tests"
	@echo "make lint         - Run linting checks (Python & Rust)"
	@echo "make fmt          - Format code (Python & Rust)"
	@echo "make docs         - Generate terminal overview and docs/CATALOG.md"
	@echo "make evaluate     - Run Golden Tests (usage: make evaluate [prompt-name])"
	@echo "make sync-version - Sync all prompt versions (usage: make sync-version [version])"
	@echo "make all          - Run validation, tests, linting, and sync catalog"
	@echo "make tui          - Build and run the Rust-based TUI browser"
	@echo "make clean        - Remove temporary files and __pycache__"

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
	@echo "Running extended feature tests..."
	@python3 tests/test_features_extended.py
	@echo "Running validation unit tests..."
	@python3 scripts/test_validation.py

rust-build:
	@echo "Building Rust TUI (Debug)..."
	@cd promptbook-tui && cargo build

rust-test:
	@echo "Running Rust unit tests..."
	@cd promptbook-tui && cargo test

release:
	@echo "Building Rust TUI (Release)..."
	@cd promptbook-tui && cargo build --release

docs:
	@echo "Generating template overview..."
	@python3 scripts/sync_all_docs.py

check-sync: docs
	@if [ -n "$$(git status --porcelain -u no docs/CATALOG.md | grep '^ M')" ]; then \
		echo "Error: Template catalog is out of sync!"; \
		echo "Please run 'make docs' locally and commit the changes."; \
		git diff docs/CATALOG.md; \
		exit 1; \
	fi
	@echo "✅ Template catalog is in sync."

evaluate:
	@PROMPT=$$(echo "$(PROMPT)" | grep -v "^$$" || echo "$(filter-out $@,$(MAKECMDGOALS))"); \
	if [ -n "$$PROMPT" ]; then \
		echo "Running Golden Test evaluation for: $$PROMPT..."; \
		python3 scripts/evaluate_prompts.py $$PROMPT; \
	else \
		echo "Running all Golden Test evaluations..."; \
		python3 scripts/evaluate_prompts.py; \
	fi

sync-version:
	@VERSION=$$(echo "$(VERSION)" | grep -E '^[0-9]+\.[0-9]+\.[0-9]+' || echo "$(filter-out $@,$(MAKECMDGOALS))"); \
	if [ -z "$$VERSION" ]; then \
		echo "Error: VERSION is not set. Usage: make sync-version [version]"; \
		exit 1; \
	fi; \
	echo "Syncing all versions to $$VERSION..."; \
	python3 scripts/sync_all_versions.py $$VERSION

# Catch-all rule to prevent errors when passing arguments to targets
%:
	@:

all: validate test lint docs check-sync
	@echo "✅ All checks passed and overview generated."

tui:
	@echo "Building and running Rust TUI..."
	@cd promptbook-tui && cargo run --release

clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf scripts/__pycache__
	@rm -rf scripts/promptbook/__pycache__
	@rm -f scripts/tmp_*
