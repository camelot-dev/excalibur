.PHONY: install test lint docs

install:
	uv sync --extra dev

test:
	uv run pytest

lint:
	uvx pre-commit run --all-files

docs:
	cd docs && make html
