set dotenv-load := true

# Lists all available commands.
help:
    just --list

# ---------------------------------------------- #
# Script to rule them all recipes.               #
# ---------------------------------------------- #

# Install pre-commit hooks
_install-pre-commit: _check-pre-commit
    #!/usr/bin/env bash
    if [[ ! -f .git/hooks/pre-commit ]]; then
      echo "Pre-commit hooks are not installed yet! Doing so now."
      pre-commit install
    fi
    exit 0

# Downloads and installs uv on your system. If on Windows, follow the directions at https://docs.astral.sh/uv/getting-started/installation/ instead.
uv-install:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! command -v uv &> /dev/null;
    then
      echo "uv is not found on path! Starting install..."
      curl -LsSf https://astral.sh/uv/install.sh | sh
    else
      uv self update
    fi

# Update uv
uv-update:
    uv self update

# Uninstall uv
uv-uninstall:
    uv self uninstall

_check-pre-commit:
    #!/usr/bin/env bash
    if ! command -v pre-commit &> /dev/null; then
      echo "Pre-commit is not installed!"
      exit 1
    fi

# Setup the project and update dependencies.
bootstrap: uv-install _install-pre-commit
    #!/usr/bin/env bash
    uv sync
    DJANGO_SETTINGS_MODULE="play_different_games.settings" PYTHONPATH="$PYTHONPATH:$(pwd)" uv run django-admin migrate

# Checks that project is ready for development.
check: _check-pre-commit
    #!/usr/bin/env bash
    if ! command -v uv &> /dev/null; then
      echo "UV is not installed!"
      exit 1
    fi
    if [[ ! -f ".venv/bin/python" ]]; then
      echo "Virtualenv is not created! Run 'just bootstrap' to complete setup."
      exit 1
    fi

# Run Django management commands
manage *ARGS: check
    #!/usr/bin/env bash
    DJANGO_SETTINGS_MODULE="play_different_games.settings" PYTHONPATH="$PYTHONPATH:$(pwd)" uv run django-admin {{ ARGS }}

# Run the development server
server: check
    #!/usr/bin/env bash
    DJANGO_SETTINGS_MODULE="play_different_games.settings" PYTHONPATH="$PYTHONPATH:$(pwd)" uv run honcho -f Procfile.dev

# Check types
check-types: check
    uv run pyright

# Run linting, types, and safety checks
check-all: lint check-types safety

# Run just formatter and rye formatter.
fmt: check
    just --fmt --unstable
    uv run ruff format

# Run ruff linting
lint *ARGS: check
    uv run ruff check {{ ARGS }}

# Run the test suite
test *ARGS: check
    uv run -m pytest {{ ARGS }}

# Run tox for code style, type checking, and multi-python tests. Uses run-parallel.
tox *ARGS: check
    uvx --python 3.12 --with tox-uv tox run-parallel {{ ARGS }}

# Runs bandit safety checks.
safety: check
    uv run -m bandit -c pyproject.toml -r src

# Runs bump-my-version to increment version numbers and tag the resulting changes.
bump *ARGS: check
    uv run bump-my-version {{ ARGS }}

# Access mkdocs commands
docs *ARGS: check
    uv run mike {{ ARGS }}

# Build Python package
build *ARGS: check
    uv build {{ ARGS }}

# Removes pycache directories and files.
_pycache-remove:
    find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

# Remove generated builds.
_build-remove:
    rm -rf dist/*

# Remove generated docs
_docs-clean:
    rm -rf site/*

# Removes pycache directories and files, and generated builds.
clean: _pycache-remove _build-remove _docs-clean
