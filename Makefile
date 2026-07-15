PYTHON = venv/bin/python3
PIP = venv/bin/pip
CONFIG = config/config.json

PYTHON_BIN := $(shell for v in python3.12 python3.11 python3.10; do command -v $$v >/dev/null 2>&1 && echo $$v && break; done)

install:
ifeq ($(PYTHON_BIN),)
	$(error No Python 3.10+ interpreter found (checked python3.12, python3.11, python3.10))
endif
	$(PYTHON_BIN) -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install mazegenerator-00001-py3-none-any.whl
	$(PIP) install pygame flake8 mypy pytest pyinstaller

run:
	$(PYTHON) pac-man.py $(CONFIG)

debug:
	$(PYTHON) -m pdb pac-man.py $(CONFIG)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint:
	venv/bin/flake8 . --exclude=venv,.git,__pycache__,.mypy_cache --max-line-length=79
	venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

test:
	venv/bin/pytest tests/

package:
	bash packager.sh

.PHONY: install run debug clean lint test package
