# Web Schematics

## Tech Stack

- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Testing**: Vitest + React Testing Library

## Component Architecture

- **`App.tsx`**: The main controller.
  - Manages game state: `grid`, `score`, `bestScore`, `gameStatus`.
  - Handles keyboard listeners.
  - Controls API interactions via `fetch`.
- **`Tile`**: Discrete component for rendering a single 2048 tile with dynamic class mapping for styling values.

## State Management

The frontend uses the **`useState`** and **`useEffect`** hooks for local state and initialization.

### Event Flow

1.  **Mount**: `useEffect` trigger `fetch('/new')` to start the game.
2.  **Interaction**: User presses 'ArrowUp'.
3.  **Action**: `handleKeyPress` checks if game is active, then triggers `fetch('/move')`.
4.  **Reaction**: State updates with new grid/status, triggering a re-render.

## TypeScript Integration

The module uses strict typing for:
- **API Responses**: Interface definitions for `MoveResponse` and `Board`.
- **Properties**: Prop types for the `Tile` component.
- **Global Objects**: `globalThis.fetch` mocking in tests.

## Styling System

Vanilla CSS is used with custom property tokens for tile colors and animations:
- `styles.css` handles the layout, grid-spacing, and transition effects.
- Dynamic class names (e.g., `tile-2`, `tile-4`) provide a signature look for different values.
