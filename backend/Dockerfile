# ==================================================
# Andiny Atlas Backend Container
# ==================================================

FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python output is sent directly to logs
ENV PYTHONUNBUFFERED=1

# Set the application working directory
WORKDIR /app

# Install system dependencies required by Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definitions first to improve Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the backend application
COPY . .

# Application port
EXPOSE 8000

# Make the startup script executable
RUN chmod +x /app/start.sh

# Start Andiny Atlas
CMD ["/app/start.sh"]