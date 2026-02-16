.ONESHELL:
SHELL := bash
.DEFAULT_GOAL := help
OS := $(shell uname)

.PHONY: \
	build \
	check \
	clean \
	create_venv \
	deploy_prod \
	deploy_test \
	help \
	install \
	install_wheel \
	rebuild_venv \
	test \
	upgrade_deps \
	upgrade_hooks

PYTHON_VERSION=3.14

build: ## build the wheel for this package
	uv build --clear

clean: ## clean out dist/ directory
	rm -rf dist/*

deploy_test: ## run all checks, build dist files, upload to test pypi
	$(MAKE) check
	$(MAKE) build
# 	uv run twine upload --repository testpypi dist/*
	uv run uv-publish --repository testpypi

deploy_prod: ## run all checks, build dist files, upload to prod pypi
	$(MAKE) check
	$(MAKE) build
# 	uv run twine upload --repository account dist/*
	uv run uv-publish --repository account

install_wheel: ## pip install this package
	uv run python -m pip install dist/free_d6-*-py3-none-any.whl --force-reinstall

test: ## Run pytest tests
	uv run pytest tests/

check: ## Run all linting/formatting checks
	uv run ruff check .
	uv run ruff format --check .

install: ## install/reinstall all packages in the environment
	uv sync --python=${PYTHON_VERSION} --all-extras --frozen
	uv run pre-commit install

create_venv: ## create virtualenv for this project
	rm -rf .venv
	uv sync --python=${PYTHON_VERSION} --all-extras --frozen
	uv run pre-commit install

activate_venv: ## activate the virtualenv for this project
	source .venv/bin/activate

upgrade_deps: ## upgrade all dependencies to latest versions
	uv sync --python=${PYTHON_VERSION} --all-extras

upgrade_hooks: ## upgrade pre-commit hooks to latest versions
	uv run pre-commit autoupdate

rebuild_venv: create_venv activate_venv install ## rebuild project virtualenv

help: ## Generate and display help info on make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
