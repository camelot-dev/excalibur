# Excalibur web UI. Runs as a non-root user on port 7860. The public demo on
# Render builds this file directly from the repository.
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /usr/local/bin/uv

RUN useradd --create-home --uid 1000 user
USER user
ENV HOME=/home/user \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH=/home/user/app/.venv/bin:$PATH \
    EXCALIBUR_WEB_HOST=0.0.0.0 \
    EXCALIBUR_WEB_PORT=7860
WORKDIR /home/user/app

# Dependencies first so they're cached between code changes.
COPY --chown=user pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY --chown=user . .
# Editable on purpose: tasks run as `python -m excalibur` from this directory,
# so the web server and the tasks must use the same package (and upload folder).
RUN uv sync --frozen --no-dev

EXPOSE 7860
CMD ["sh", "-c", "excalibur initdb && excalibur webserver"]
