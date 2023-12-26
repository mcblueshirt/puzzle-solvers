PYTHON_DIRS = src tests


install:
	poetry install --no-root

run:
	poetry run python -m src.main

format:
	poetry run black $(PYTHON_DIRS)
	poetry run ruff --fix $(PYTHON_DIRS)


check:
	poetry run black --check $(PYTHON_DIRS)
	poetry run ruff check $(PYTHON_DIRS)
	poetry run mypy $(PYTHON_DIRS)

test:
	poetry run pytest tests

check-all: check test
