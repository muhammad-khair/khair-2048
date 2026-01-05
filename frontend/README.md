# Frontend Module

React-TypeScript frontend for 2048.

## Overview

A modern, responsive frontend built with Vite, React 18, and TypeScript. It handles user input (keyboard/touch), renders the game state, and integrates closely with the AI recommendation system.

## Architecture

The application is structured into modular components:
- **`src/components/`**: Reusable UI blocks.
  - `Grid`: Renders the game board (also used for AI previews).
  - `Tile`: Individual interactive tiles.
  - `Recommendation`: Displays AI advice and rationale.
  - `ModelSelector`: Dropdown to switch between Heuristic, Gemini, and Ollama models.
  - `Controls`, `Header`, `GameOverlay`: Layout and interaction.
- **`src/services/`**: Integration layer.
  - `transport.ts`: Handles all API communication with the backend.
- **`src/configs/`**: Configuration files.
  - `config.ts`: Environment and app-level constants.
- **`src/types.ts`**: Shared TypeScript definitions.

## Configuration

The application authenticates with the backend using the address specified in `SERVER_HOST`.

- `SERVER_HOST`: The endpoint for the game server (default: `http://localhost:8000`).

## Development

```bash
# From the frontend directory
npm install
npm run dev
```

## Testing

Run unit tests using Vitest and React Testing Library:

```bash
npm run test
```

### Linting

Run the linter to check for code quality issues:

```bash
npm run lint
```

## Building

Generate the production static assets for the server:

```bash
npm run build
```

The output will be in `web/dist/`.
