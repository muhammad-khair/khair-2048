# Server Module

FastAPI-powered backend for 2048.

## Overview

The server module bridges the Python game logic with the React frontend. It provides a RESTful API and serves the frontend's static build files.

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

- `src/app.py`: FastAPI application definition and endpoint logic.
- `src/main.py`: Entry point for starting the server (CLI).
