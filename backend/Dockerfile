FROM python:3.11-slim

WORKDIR /app

# Copy requirements FIRST for better caching
COPY requirements/ ./requirements/

# Install dependencies
RUN pip install --no-cache-dir -r requirements/dev.txt

# Copy app code
COPY . .

# Create non-root user
RUN useradd -m oracle
USER oracle

EXPOSE 8000