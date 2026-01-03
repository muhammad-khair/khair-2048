# --- Stage 1: Build the Frontend ---
FROM node:18-slim AS frontend-builder
WORKDIR /app/web

# Copy only package files first for better caching
COPY web/package*.json ./
RUN npm install

# Copy the rest of the web directory and build
COPY web/ .
RUN npm run build

# --- Stage 2: Final Image ---
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY game/ ./game/
COPY server/ ./server/

# Copy the built frontend from Stage 1
COPY --from=frontend-builder /app/web/dist ./web/dist

# Expose the port FastAPI runs on
EXPOSE 8000

# Metadata
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "-m", "server.src.main", "--host", "0.0.0.0", "--port", "8000"]
