# PromptOps Makefile

.PHONY: help test validate catalog evaluate all clean

help:
	@echo "PromptOps Developer Tools"
	@echo "-------------------------"
	@echo "make validate  - Run metadata and structure validation on all prompts"
	@echo "make test      - Run CLI helper logic tests"
	@echo "make catalog   - Regenerate the CATALOG.md file"
	@echo "make evaluate  - Run Golden Tests using LLM-as-a-judge (Requires GEMINI_API_KEY)"
	@echo "make all       - Run validation, tests, and regenerate catalog"
	@echo "make clean     - Remove temporary files and __pycache__"

validate:
	@echo "Validating prompt metadata..."
	@python3 scripts/validate_prompts.py

test:
	@echo "Running CLI helper tests..."
	@python3 scripts/test_promptops.py

docs:
	@echo "Syncing all documentation..."
	@python3 scripts/sync_all_docs.py

all: validate test docs
	@echo "✅ All checks passed and catalog updated."

clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf scripts/__pycache__
	@rm -f scripts/tmp_*
	@rm -f add_tags.py add_versions.py create_prompts.py restructure.py
