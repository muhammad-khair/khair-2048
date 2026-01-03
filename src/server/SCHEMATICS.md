# Server API Schematic

This module defines the stateless FastAPI interface for the 2048 game.

## API Endpoints

### `POST /new`
- **Description**: Initializes a new game grid.
- **Request**: None.
- **Response**: `Board` (2D List of integers or null).

### `POST /move`
- **Description**: Processes a move and returns the resulting state based on the provided grid.
- **Request Body**:
  ```json
  {
    "grid": [[null, 2, ...], ...],
    "direction": "up" | "down" | "left" | "right"
  }
  ```
- **Response Body**:
  ```json
  {
    "grid": [[2, 4, ...], ...],
    "status": "ONGOING" | "WIN" | "LOSE",
    "largest_number": 2048
  }
  ```

## Integration Flow
1. **Frontend** sends current grid + direction to `/move`.
2. **Server** instantiates a `GameBoard` with the provided data.
3. **GameBoard** performs logic (merge/spawn) and returns the result.
4. **Server** serializes the new state and sends it back to the client.
