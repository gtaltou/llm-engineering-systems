# ==================================================
# Builder
# ==================================================

FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock* ./

RUN uv sync --no-dev

# ==================================================
# Runtime
# ==================================================

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /root/.cache /root/.cache

COPY . .

RUN pip install uv && \
    uv sync --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.smart_brochure_generator.api.main:app", "--host", "0.0.0.0", "--port", "8000"]