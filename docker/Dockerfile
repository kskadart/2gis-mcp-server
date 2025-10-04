FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS dev

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

FROM python:3.13-slim-trixie AS runtime

WORKDIR /app

COPY --from=dev /app/.venv /app/.venv

COPY src/ /app/src/

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--transport", "stdio"]
