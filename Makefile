.DEFAULT_GOAL := help

PYTHON ?= $(shell command -v python3 >/dev/null 2>&1 && echo python3 || echo python)
VENV_DIR ?= .venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip
UVICORN := $(VENV_BIN)/uvicorn

.PHONY: help venv install run clean baml-init baml-generate baml

help:
	@echo "Targets:"
	@echo "  venv    - Create a local virtual environment in $(VENV_DIR)"
	@echo "  install - Create venv (if needed) and install requirements"
	@echo "  run     - Start the app with uvicorn (after install)"
	@echo "  clean   - Remove venv and Python caches"
	@echo "  baml    - Initialize and generate BAML client (optional)"

venv:
	@test -d $(VENV_BIN) || $(PYTHON) -m venv $(VENV_DIR)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

baml-init:
	# Try Node-based CLI first, fall back to system CLI if available
	@which npx >/dev/null 2>&1 && npx baml-cli@latest init || (which baml-cli >/dev/null 2>&1 && baml-cli init || true)

baml-generate:
	# Generate baml_client from baml_src/
	@which npx >/dev/null 2>&1 && npx baml-cli@latest generate || (which baml-cli >/dev/null 2>&1 && baml-cli generate || true)

baml: baml-init baml-generate
	@echo "BAML client generated (if CLI available)."

clean:
	rm -rf $(VENV_DIR) .pytest_cache __pycache__ **/__pycache__ .mypy_cache .ruff_cache .coverage htmlcov
