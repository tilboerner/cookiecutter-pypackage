.PHONY: clean clean-build clean-pyc clean-test clean-venv deps docs format help lint resync shell test test-all test-coverage .MAKEVENV .MAKEPOETRY
.DEFAULT_GOAL := help

POETRY := $(shell command -v poetry)
ifndef POETRY
	POETRY := .MAKEPOETRY
	VIRTUALENV := .MAKEPOETRY
else
	VIRTUALENV := $(shell poetry env info --path)
endif
ifndef VIRTUALENV
	VIRTUALENV := .MAKEVENV
endif

# Need Poetry >= 1.1.0 for --remove-untracked;
# try to find the flag in poetry help output and use it if found:
HAS_REMOVE_UNTRACKED := $(shell poetry help install | grep -o  -- '--remove-untracked' | uniq)
ifeq ($(strip $(HAS_REMOVE_UNTRACKED)),--remove-untracked)
	REMOVE_UNTRACKED := --remove-untracked
endif

help:  ## Print this help text.
	@echo "Please provide a make target."

clean: clean-build clean-pyc clean-test  ## Remove all build, test, coverage and Python artifacts.

clean-build:  ## Remove build artifacts.
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:  ## Remove python artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:  ## Remove test and coverage artifacts.
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-venv:  ## Delete project virtualenv.
	poetry env remove python

deps: $(VIRTUALENV)/.updated .git/hooks/pre-commit  ## Create dev environment.

docs: export PYTHONPATH=src
docs: deps  ## Generate Sphinx HTML documentation, including API docs.
	rm -f docs/{{cookiecutter.project_slug}}.rst
	rm -f docs/modules.rst
	PYTHONPATH=src poetry run sphinx-apidoc -o docs/ src/{{cookiecutter.project_slug}}
	poetry run $(MAKE) -C docs clean
	poetry run $(MAKE) -C docs html
	@echo xdg-open docs/_build/html/index.html

format: deps  ## Auto-format all Python code to project standard.
	poetry run isort --recursive src tests
	poetry run black src tests

lint: deps  ## Run code linters.
	SKIP=black,isort poetry run pre-commit run --all-files

resync: $(VIRTUALENV) poetry.lock  ## `make resync deps` to force deps install
	-rm $(VIRTUALENV)/.updated

shell: export PYTHONPATH=src
shell: deps  ## Get a Python shell in the dev environment.
	poetry run ipython

test: export PYTHONPATH=src
test: deps  ## Run tests quickly with default Python.
	poetry run pytest

test-all: deps  ## Run tests on every Python version with tox.
	poetry run tox

test-coverage: export PYTHONPATH=src
test-coverage: deps  ## Check code coverage quickly with default Python.
	-poetry run pytest --cov=src --cov-report=html
	-poetry run coverage report --show-missing --skip-empty --skip-covered
	@echo xdg-open htmlcov/index.html

poetry.lock: pyproject.toml
	poetry lock && touch poetry.lock

$(VIRTUALENV)/.updated: $(VIRTUALENV) poetry.lock
	# Need Poetry >= 1.1.0 for --remove-untracked
	poetry install -v --no-root $(REMOVE_UNTRACKED) && touch $(VIRTUALENV)/.updated

.git/hooks/pre-commit: $(VIRTUALENV)/.updated
	[ -f .git/hooks/pre-commit ] || poetry run pre-commit install

.MAKEVENV:
	poetry env use python
	# We can't reassign VIRTUALENV variable here, because
	# 'eval' does not like the dash in 'poetry env info --path'.
	# So we abort to start from the beginning next time.
	@echo "Created virtualenv. Re-run make command to use it."
	exit 1

.MAKEPOETRY:
	@echo "Please install Poetry for Python."
	@echo "Your favourite package manager would have something like 'python-poetry'."
	@echo "Or see: https://python-poetry.org/docs/#installation"
	exit 1
