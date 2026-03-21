# PromptOps Makefile

.PHONY: help test validate catalog all clean

help:
	@echo "PromptOps Developer Tools"
	@echo "-------------------------"
	@echo "make validate  - Run metadata and structure validation on all prompts"
	@echo "make test      - Run CLI helper logic tests"
	@echo "make catalog   - Regenerate the CATALOG.md file"
	@echo "make all       - Run validation, tests, and regenerate catalog"
	@echo "make clean     - Remove temporary files and __pycache__"

validate:
	@echo "Validating prompt metadata..."
	@python3 scripts/validate_prompts.py

test:
	@echo "Running CLI helper tests..."
	@python3 scripts/test_promptops.py

catalog:
	@echo "Generating CATALOG.md..."
	@python3 scripts/generate_catalog.py

all: validate test catalog
	@echo "✅ All checks passed and catalog updated."

clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf scripts/__pycache__
	@rm -f scripts/tmp_*
	@rm -f add_tags.py add_versions.py create_prompts.py restructure.py
