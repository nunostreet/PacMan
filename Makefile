PYTHON = venv/bin/python3
PIP = venv/bin/pip
CONFIG = config/config.json

install:
	python3.12 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install mazegenerator-00001-py3-none-any.whl
	$(PIP) install pygame flake8 mypy pytest

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
	venv/bin/flake8 . --exclude=venv,venv 2,.git,__pycache__,.mypy_cache --max-line-length=79
	venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

test:
	venv/bin/pytest tests/

package:
	bash packager.sh

.PHONY: install run debug clean lint test package
