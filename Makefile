PYTHON = venv/bin/python3
PIP = venv/bin/pip
CONFIG = config.json

install:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install mazegenerator-00001-py3-none-any.whl
	$(PIP) install flake8 mypy pytest

run:
	$(PYTHON) main.py $(CONFIG)

debug:
	$(PYTHON) -m pdb main.py $(CONFIG)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint:
	venv/bin/flake8 .
	venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

test:
	venv/bin/pytest tests/

.PHONY: install run debug clean lint test
