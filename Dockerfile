FROM python:3.11-slim

WORKDIR /app

# Copy only backend requirements first
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder
COPY backend/ .

# Expose the port Railway will use
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
