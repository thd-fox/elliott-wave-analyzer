# Multi-arch friendly Dockerfile for Elliott Wave Analyzer
# Build (local ARM Mac): docker build -t elliott-wave:dev .
# Run: docker run -d --name elliott-wave -p 8000:8000 \
#   -e OPENAI_API_KEY=sk-xxx -e AI_MODE=auto elliott-wave:dev
# For server (x86_64) just build there; for multi-arch push use buildx (see README notes).

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    AI_MODE=auto

# System deps for numpy/pandas/matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev libpng-dev libjpeg-dev zlib1g-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements first (better layer cache)
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt gunicorn

# Copy application
COPY . .

# Create non-root user (optional)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Start via lightweight script (allows env overrides)
ENTRYPOINT ["/app/start.sh"]
