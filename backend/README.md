# Backend - 2048

This directory contains the backend implementation for the 2048 application. It is composed of three independent modules that work together:
- **API** - HTTP interface for the frontend
- **Game** - Core 2048 game engine
- **Recommendation** - Move recommendation logic (heuristics and AI)

### Run the backend 

```bash
# From project root
source .venv/bin/activate
cd backend
python -m api.src.main
```

### Backend tests

```bash
# From project root with venv activated
cd backend
python -m pytest
```

---

## API Module (`api/`)

Provides a FastAPI-based HTTP server that exposes the game and recommendation functionality to the frontend.

### What it does

- Serves REST endpoints under `/api`
- Creates and updates game state
- Returns move recommendations

### Run API tests

```bash
# From project root with venv activated
cd backend
python -m pytest test/api
```

---

## Game Module (`game/`)

This module provides the independent engine for the game, handling the 4x4 grid, tile generation, movement rules, and game state validation (Ongoing, Won, Lost).

This engine follows the standard 2048 convention: **A move is only valid if it results in a change to the board.**
- If a move (Up, Down, Left, or Right) does not shift any tiles or trigger any merges, the turn counter is not incremented.
- No new random tile is spawned for an invalid (invariant) move.

### What it does

- Manages the 4×4 board state
- Applies movement and merge rules 
- Determines win / loss conditions

### Run game tests

```bash
# From project root with venv activated
cd backend
python -m pytest test/game
```

---

## Recommendation Module (`recommendation/`)

Analyzes game states and suggests the best next move.

### What it does

- Provides deterministic heuristic-based recommendations
- Optionally integrates with AI models for advanced strategy
- Falls back to heuristics when no AI is configured

### Configuration (optional)

You might want to configure the following environment variables:

- `GEMINI_API_KEY` - Enable Google Gemini recommendations
- `OLLAMA_HOST` - Enable local Ollama recommendations (default: `http://localhost:11434`)

### Run recommender tests

```bash
# From project root with venv activated
cd backend
python -m pytest test/recommendation
```

---

## Notes

- Each module has its own isolated test suite
- Core game logic is framework-agnostic
- AI features are optional and disabled by default
