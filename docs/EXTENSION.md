# Difficulty Extension: Boulders

This document outlines the requirements for adding difficulty levels to the 2048 game by introducing "boulders" - special cells that act as obstacles.

## Overview

Boulders are locked grid cells that cannot be moved or merged with numbers. They add strategic complexity to the game by blocking tile movement and reducing available merging space.

## Requirements

### 1. Boulder Behavior

- **Static Position**: Boulders do not move in any direction
- **Non-Mergable**: Boulders cannot merge with numbers or other boulders
- **Blocking**: Tiles slide until they hit a boulder or the grid edge

### 2. Difficulty Levels

| Difficulty | Boulder Count | Description |
|------------|---------------|-------------|
| Easy       | 0             | Standard 2048 gameplay |
| Medium     | 1             | One boulder randomly placed |
| Hard       | 2             | Two boulders randomly placed |

### 3. Backend Implementation

#### GameBoard Class

- **Constructor Extension**: Add optional `boulder_count` parameter to allow configurable boulder placement
- **Boulder Representation**: Use `0` (or a dedicated constant like `BOULDER`) to represent boulders in the grid
- **Movement Logic**: Update movement functions (`move_left`, `move_right`, `move_up`, `move_down`) to treat boulders as immovable obstacles

Example board with some boulders:

```python
[
    [2, 2, BOULDER, None],
    [None, BOULDER, None, 2],
    [2, None, BOULDER, 2],
    [None, None, None, None],
]
```

This is what happens if you move left:

```python
[
    [4, None, BOULDER, None],
    [None, BOULDER, 2, None],
    [2, None, BOULDER, 2],
    [None, None, None, None],
]
```

#### API Endpoint

- Extend `/api/new` to accept a `difficulty` parameter that maps to boulder counts

### 4. Frontend Implementation

#### Difficulty Selector

- Add a dropdown menu on the main screen allowing users to select difficulty (Easy/Medium/Hard)
- Default to Easy (no boulders)
- Selector should be placed near the "New Game" button

#### Tile Rendering

- Display boulders as grey boxes (darker background with hidden text)
- Use consistent styling that matches the existing tile aesthetic

### 5. Testing Requirements

- Unit tests for all four movement directions with boulders present
- Test edge cases: boulders at corners, edges, and middle positions
- Test multiple boulders blocking each other

## Implementation Notes

- The boulder implementation was designed to be backward-compatible with existing games
- Consider adding boulder count configuration to game settings for future extensibility
- The frontend difficulty selector should disable game recommendations while a game is in progress
