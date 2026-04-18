FROM python:3.11-slim

WORKDIR /app

# Install only OS deps needed (no build tools for heavy ML)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Force install exactly pinned versions, ignoring dependency conflicts
RUN pip install --no-cache-dir --no-deps -r requirements.txt

COPY . .

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]