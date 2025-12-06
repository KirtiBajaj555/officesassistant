FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml ./pyproject.toml
COPY uv.lock* ./

# Install dependencies
RUN uv sync

# Copy backend code
COPY backend/ .

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uv", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
