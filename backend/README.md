# Backend - 2048

This directory contains the backend implementation for the 2048 application. It serves as the API server, game engine, and recommendation system.

## Project Structure

- **`src/app/`**: Application factory and composition root.
- **`src/api/`**: FastAPI routers (including `index.py` for static files) and Pydantic models.
- **`src/game/`**: Core 2048 game logic and state management.
- **`src/recommendation/`**: Application-agnostic recommendation system (Heuristic & AI).
- **`src/config/`**: Centralized configuration and settings.
- **`test/`**: Comprehensive test suite (Pytest).

## Setup & Running

1. **Create Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run Server**:
   ```bash
   python -m src.main
   ```
   The server will start at `http://localhost:8000`.

## Testing

Run the full test suite using `pytest`:

```bash
# Run all tests
python -m pytest

# Run specific module tests
python -m pytest test/api
python -m pytest test/game
python -m pytest test/recommendation
```

### Linting

Run the full linting suite using `pylint`:

```bash
# Run all linters
pylint $(git ls-files '*.py')
```

## Configuration

All configuration is managed via Environment Variables. You can set these in a `.env` file or export them directly.

See `src/config/settings.py` for the complete list of settings.

### Key Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |
| `RECOMMENDATION__GEMINI__API_KEY` | API Key for Google Gemini | `""` |
| `RECOMMENDATION__GEMINI__ALLOWED_MODELS` | JSON list of allowed Gemini models | `["gemini-2.0-flash", ...]` |
| `RECOMMENDATION__OLLAMA__HOST` | URL for Ollama server | `http://localhost:11434` |
| `RECOMMENDATION__OLLAMA__ALLOWED_MODELS` | JSON list of allowed Ollama models | `[]` (None) |
