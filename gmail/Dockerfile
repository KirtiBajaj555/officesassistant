FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml ./pyproject.toml
COPY uv.lock* ./

# Install dependencies
RUN uv sync

# Copy gmail server code
COPY gmail/ .

# MCP servers run via stdio when spawned by backend
# This is mainly for standalone testing
CMD ["uv", "run", "server.py"]
