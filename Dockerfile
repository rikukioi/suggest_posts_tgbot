FROM python:3.13-slim

RUN apt-get update && apt-get install -y

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv sync

COPY . .

CMD ["uv", "run", "python -m src.main"]
