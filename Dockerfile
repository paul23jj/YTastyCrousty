FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/code/.venv \
    PATH="/code/.venv/bin:$PATH"

WORKDIR /code

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --locked --no-dev

EXPOSE 8000

CMD ["uvicorn", "ytastycrousty.main:app", "--host", "0.0.0.0", "--port", "8000"]