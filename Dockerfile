FROM python:3.12.4-slim-bookworm AS base

FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /bin/uv
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml uv.lock* README.md /app/

# Create the complete virtual environment
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache \
    uv venv .venv && \
    uv sync --frozen --no-group research
ENV PATH="/app/.venv/bin:$PATH"

# Final image
FROM base

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY ./src /app/src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH" \
    PORT=8000

# Expose the port
EXPOSE 8000

# Run the application
CMD ["python", "src/main.py"] 