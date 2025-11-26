# Use official Python image
FROM python:3.11-slim

# Create and go to working directory
WORKDIR /app

# Install dependencies first to improve caching
COPY requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Railway sets PORT env variable automatically)
EXPOSE 8000

# Start FastAPI through uvicorn
CMD ["uvicorn", "app. main: app", "--host", "0.0.0.0", "--port", "8000"]
