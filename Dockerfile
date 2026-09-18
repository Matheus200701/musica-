FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY . .
RUN useradd -r -u 10001 botuser && mkdir -p /app/data && chown -R botuser:botuser /app
USER botuser
CMD ["python","bot.py"]
