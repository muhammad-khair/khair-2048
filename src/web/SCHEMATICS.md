# Web Frontend Schematic

A modern, responsive frontend inspired by the original 2048 game.

## UI Components

### 1. Game Header
- **Logo**: "2048" style branding.
- **Scoreboard**: 
    - **Current Best**: The highest tile reached in the *active* grid.
    - **Session Best**: The highest tile reached across *all* game resets in the current session.
- **New Game Button**: Resets the board via the `/new` endpoint.

### 2. Game Grid
- **Container**: A fixed-size square container ($450\text{px}$).
- **Cells**: A $4 \times 4$ background grid of empty slots.
- **Tiles**: Dynamically rendered `div` elements positioned absolutely over the grid.

### 3. Controls
- **Keyboard Listener**: Captures Arrow Keys and WASD.
- **On-screen Buttons**: Touch-friendly directional arrows for mobile/manual play.

## Visual Design
- **Typography**: Uses the 'Inter' font family for a clean, modern look.
- **Animations**: CSS transitions handle tile sliding (top/left properties) and merges.
- **Color Palette**:
    - `2`: `#eee4da`
    - `4`: `#ede0c8`
    - `2048`: `#edc22e` (Gold)

## State Management
The frontend `GameUI` class in `script.js` manages:
1. **Grid State**: Stores the current 2D array locally.
2. **Move Execution**: Sends the current grid to the backend and updates the local state with the response.
3. **Rendering**: Clears and re-populates the `tile-container` on every state change.
4. **Game Over/Win**: Displays an overlay message when the backend reports a terminal state.
