# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x superuser.sh

# Create directories
RUN mkdir -p /app/staticfiles /app/data

# Expose port 8000
EXPOSE 8000

# Entrypoint handles setup
ENTRYPOINT ["/bin/bash", "./superuser.sh"]

# CMD starts the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]