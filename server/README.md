# Server Module

FastAPI-powered backend for 2048.

## Overview

The server module bridges the Python game logic with the React frontend. It provides a RESTful API (at `/api`) and serves the frontend's static build files.

## API Endpoints

- `POST /api/new`: Start a new game.
- `POST /api/move`: Make a move.
- `POST /api/recommend`: Get an AI recommendation.

## Running the Server

```bash
# From project root
source .venv/bin/activate
python -m server.src.main
```

## Testing

Run API integration tests:

```bash
# From project root
python -m pytest server/test/
```

## Internal Structure

- `src/main.py`: Application entry point and configuration.
- `src/routes.py`: API endpoints (prefixed with `/api`).
- `src/models.py`: Pydantic data schemas for requests and responses.
