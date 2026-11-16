.PHONY: install run test coverage lint format typecheck check docker

install:
	uv sync

run:
	uv run uvicorn src.smart_brochure_generator.api.main:app --reload

test:
	uv run pytest

coverage:
	uv run pytest --cov=src/smart_brochure_generator --cov-report=term-missing

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy .

check: lint typecheck test

docker:
	docker compose up --build