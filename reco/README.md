# Recommender Module

Modular systems for generating move recommendations using Heuristics or AI.

## Overview

The `reco` module provides an analytical layer that suggests the best next move for a Given 2048 board state. It supports high-performance local heuristics and flexible AI model integration (Gemini/Local LLMs).

## Recommender Types

- **HeuristicRecommender**: Uses move simulation to maximize empty spaces and maintain tile organization.
- **GeminiRecommender**: Connects to Google's Gemini models for high-quality strategic advice.
- **OllamaRecommender**: Connects to local Ollama API for private, offline AI suggestions.

## Configuration

Set the following environment variables to enable AI features:
- `GEMINI_API_KEY`: Your Google Gemini API key (Required for Gemini).
- `OLLAMA_HOST`: Optional URL for Ollama (default's to Ollama's local endpoint: `http://localhost:11434`).

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
- `src/gemini.py`: Google Gemini integration.
- `src/ollama.py`: Local Ollama integration.
- `src/__init__.py`: Factory pattern for instantiating recommenders.
- `test/`: Focused unit tests for each component.
