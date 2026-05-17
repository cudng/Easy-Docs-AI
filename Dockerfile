FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

RUN pip install --no-cache-dir uv==0.5.*

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src ./src

EXPOSE 8000

CMD ["sh", "-c", "uv run flet run --web --host 0.0.0.0 --port ${PORT} src/main.py"]
