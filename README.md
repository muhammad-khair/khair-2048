# khair-2048

A modular Python implementation of a **2048-style sliding tile game** with a **React-TypeScript** web interface.

![2048 Game UI](docs/images/ui_screenshot.png)

---

## Project Structure

This project is organized into three main components:

- **`game/`**: Core game logic (grid management, tile movement, merging).
  - `src/`: Python source code.
  - `test/`: Pytest unit tests.
- **`server/`**: FastAPI backend that serves the game logic and static assets.
  - `src/`: Python source code (FastAPI app).
  - `test/`: Pytest unit tests for API endpoints.
- **`web/`**: Modern React-TypeScript frontend.
  - `src/`: React components and hooks.
  - `test/`: Vitest unit tests for the UI.

---

## Quick Start (Recommended)

Run the entire application with a single command from the project root:

### Using Bash
```bash
./start.sh
```
*This script will automatically build the frontend if needed and start the backend server.*

**To force a rebuild and run:**
```bash
./start.sh --build
```

### Using Docker
```bash
# Build the image
docker build -t khair-2048 .

# Run the container
docker run -p 8000:8000 khair-2048
```
*The game will be available at `http://localhost:8000`.*

---

## Individual Setup

### 1. Backend Setup (Python)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Frontend Setup (React/TS)
```bash
cd web
npm install
npm run build
```

---

## Manual Execution

If you prefer to run the components separately:

1. **Build the frontend**:
   ```bash
   cd web && npm run build
   ```

2. **Run the server**:
   ```bash
   python -m server.src.main
   ```

---

## Testing

### Backend (Pytest)
Run all backend tests from the project root:
```bash
pytest
```

### Frontend (Vitest)
Run web tests from the `web` directory:
```bash
cd web
npm run test
```

---

## Technical Details

- **Backend**: Python FastAPI (Stateless logic).
- **Frontend**: React 18, TypeScript, Vite.
- **Communication**: REST API (`/new`, `/move`).
- **State**: Client-managed grid state, server-validated transitions.

### Core Assumptions

Based on standard 2048 mechanics:
- **Move Invariance**: A move is only finalized (turns incremented, new tile spawned) if it changes the board state. If no tiles can move or merge in the selected direction, the move is ignored.
