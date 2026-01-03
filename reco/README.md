# Recommender Module

Modular systems for generating move recommendations using Heuristics or AI.

## Overview

The `reco` module provides an analytical layer that suggests the best next move for a Given 2048 board state. It supports high-performance local heuristics and flexible AI model integration (Gemini/Local LLMs).

## Recommender Types

- **HeuristicRecommender**: Uses move simulation to maximize empty spaces and maintain tile organization (e.g., keeping high values in corners).
- **AiRecommender**: Queries Large Language Models (LLMs) to provide strategic advice and rationale. Supports:
    - **Online**: Google Gemini (requires `GEMINI_API_KEY`).
    - **Local**: Ollama or LocalAI (requires `LOCAL_AI_URL`).

## Configuration

Set the following environment variables to enable AI features:
- `GEMINI_API_KEY`: Your Google Gemini API key.
- `LOCAL_AI_URL`: The endpoint for a local OpenAI-compatible API.

If no AI keys are provided, the system defaults to the `HeuristicRecommender`.

## Testing

Run the module-specific test suite:

```bash
# From project root
source .venv/bin/activate
python -m pytest reco/test/
```

## Internal Structure

- `src/base.py`: Abstract base class and shared types.
- `src/heuristic.py`: Implementation of the tactical simulation engine.
- `src/ai.py`: Bridge for online and local LLM providers.
- `src/__init__.py`: Factory pattern for instantiating recommenders.
- `test/`: Focused unit tests for each component.
