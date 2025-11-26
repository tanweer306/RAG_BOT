FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for python-magic
RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder
COPY backend/ .

# Expose port
EXPOSE 8000

# Use shell form CMD (no brackets) for proper variable expansion
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
