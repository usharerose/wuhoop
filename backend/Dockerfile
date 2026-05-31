FROM python:3.14-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv --no-cache-dir \
    && uv sync --frozen --no-dev \
    && rm -rf /root/.cache

COPY backend/ ./backend/

EXPOSE 5000

CMD ["uv", "run", "uvicorn", "--factory", "backend.api.app:create_app", "--host", "0.0.0.0", "--port", "5000"]
