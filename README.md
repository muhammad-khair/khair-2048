# khair-2048

A modular Python implementation of a **2048-style sliding tile game** with a **React-TypeScript** web interface - with a recommend feature.

<p align="center">
  <img src="docs/images/ui_grid.png" width="30%" alt="2048 Game Grid UI" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="docs/images/ui_recommendation.png" width="30%" alt="2048 Game Recommendation UI" />
</p>

---

## Project Structure

This project is organized into four main components:

- **`game/`**: Core game logic (grid management, tile movement, merging).
- **`reco/`**: Recommendation Engine (using AI models like Gemini, Ollama, etc. or local heuristics).
- **`server/`**: FastAPI backend that serves the game logic and static assets.
- **`web/`**: Modern React-TypeScript frontend.

---

## Technical Details

- **Backend**: Python FastAPI (Stateless logic).
- **Frontend**: React 18, TypeScript, Vite.
- **Communication**: REST API (`/new`, `/move`, `/recommend`).
- **State**: Client-managed grid state, server-validated transitions.

### Core Assumptions

Based on standard 2048 mechanics:
- **Move Invariance**: A move is only finalized (turns incremented, new tile spawned) if it changes the board state. If no tiles can move or merge in the selected direction, the move is ignored.
- **Merging**: Only immediate merges are done, there are no chained merges.

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

## Environment Variables

There are some optional environment variables required for maximum usage of the recommender.
If none of the variables here are specified, then the application will default to a simple heuristic recommender.

- `GEMINI_API_KEY`: Required for Google Gemini recommendations.
- `OLLAMA_HOST`: Optional URL for Ollama (default's to Ollama's local endpoint: `http://localhost:11434`).

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
