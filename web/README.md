# Web Module

React-TypeScript frontend for 2048.

## Overview

A modern, responsive frontend built with Vite, React 18, and TypeScript. It handles user input (keyboard/touch), renders the game state, and integrates closely with the AI recommendation system.

## Architecture

The application is structured into modular components:
- **`src/components/`**: Reusable UI blocks.
  - `Grid`: Renders the game board (also used for AI previews).
  - `Tile`: Individual interactive tiles.
  - `Recommendation`: Displays AI advice and rationale.
  - `Controls`, `Header`, `GameOverlay`: Layout and interaction.
- **`src/types.ts`**: Shared TypeScript definitions.

## Development

```bash
# From the web directory
npm install
npm run dev
```

## Testing

Run unit tests using Vitest and React Testing Library:

```bash
npm run test
```

## Building

Generate the production static assets for the server:

```bash
npm run build
```

The output will be in `web/dist/`.
