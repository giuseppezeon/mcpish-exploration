.DEFAULT_GOAL := help

PYTHON ?= $(shell command -v python3 >/dev/null 2>&1 && echo python3 || echo python)
VENV_DIR ?= .venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip
UVICORN := $(VENV_BIN)/uvicorn

.PHONY: help venv install run clean

help:
	@echo "Targets:"
	@echo "  venv    - Create a local virtual environment in $(VENV_DIR)"
	@echo "  install - Create venv (if needed) and install requirements"
	@echo "  run     - Start the app with uvicorn (after install)"
	@echo "  clean   - Remove venv and Python caches"

venv:
	@test -d $(VENV_BIN) || $(PYTHON) -m venv $(VENV_DIR)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	rm -rf $(VENV_DIR) .pytest_cache __pycache__ **/__pycache__ .mypy_cache .ruff_cache .coverage htmlcov
