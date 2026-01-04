# --- Stage 1: Build the Frontend ---
FROM node:18-slim AS frontend-builder
WORKDIR /app/frontend

# Copy only package files first for better caching
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend directory and build
COPY frontend/ .
RUN npm run build

# --- Stage 2: Final Image ---
FROM python:3.11-slim AS runner
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the backend code
COPY backend/ ./backend/

# Install backend package
RUN cd backend && pip install -e .

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Metadata
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setup application environment variables
ENV APP__HOST=0.0.0.0
ENV APP__PORT=8000
EXPOSE 8000

# Run the application
WORKDIR /app/backend
CMD ["python", "-m", "src.main"]
