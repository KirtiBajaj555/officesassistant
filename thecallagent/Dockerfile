FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml ./pyproject.toml
COPY uv.lock* ./

# Install dependencies
RUN uv sync

# Copy call agent code
COPY thecallagent/ .

# Run the voice agent worker
CMD ["uv", "run", "calling_agent.py", "start"]
