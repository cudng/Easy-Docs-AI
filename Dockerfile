FROM python:3.11-slim

WORKDIR /app

# install uv
RUN pip install --no-cache-dir uv

# copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# install deps
RUN uv sync --no-dev

# copy source code
COPY src ./src

EXPOSE 8000

CMD ["uv", "run", "flet", "run", "--web", "--port", "8000", "src/main.py"]