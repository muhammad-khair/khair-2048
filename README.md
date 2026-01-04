# khair-2048

A modular Python implementation of a **2048-style sliding tile game** with a **React-TypeScript** web interface - with a recommend feature.

See the app in action here: [khair-2048](https://khair-2048.onrender.com).

<p align="center">
  <img src="docs/images/ui_grid.png" width="30%" alt="2048 Game Grid UI" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="docs/images/ui_recommendation.png" width="30%" alt="2048 Game Recommendation UI" />
</p>

---

## Project Structure

This project is organized into two main components:

- **`backend/`**: Python backend.
  - Core game logic (grid management, tile movement, merging).
  - Recommendation Engine (using AI models like Gemini, Ollama, etc. or local heuristics).
  - FastAPI backend that serves the game logic and static assets.
- **`frontend/`**: Modern React-TypeScript frontend.

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

*This script will automatically build the frontend and start the backend server.*

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

- `RECOMMENDATION__GEMINI__API_KEY`: Required for Google Gemini recommendations.
- `RECOMMENDATION__OLLAMA__HOST`: Optional URL for Ollama (default's to Ollama's local endpoint: `http://localhost:11434`).

### Model Access Control (Optional)

You can restrict which specific models are available to the user via these environment variables (JSON formatted list):

- `RECOMMENDATION__GEMINI__ALLOWED_MODELS`: List of allowed Gemini models (e.g., `["gemini-2.0-flash"]`). Empty list = No models allowed.
- `RECOMMENDATION__OLLAMA__ALLOWED_MODELS`: List of allowed Ollama models (e.g., `["deepseek-r1:1.5b"]`). Empty list = No models allowed.

---

## Individual Setup

### 1. Backend Setup (Python)
```bash
# run this in the project root directory
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Frontend Setup (React/TS)
```bash
# run this in the project root directory
cd frontend
npm install
npm run build
```

### 3. Run backend (which serves the frontend package)
```bash
# run this in the project root directory
cd backend
python -m src.main
```

---

## Testing

### Backend (Pytest)
Run all backend tests from the `backend` directory:
```bash
# run this in the project root directory
cd backend
pytest
```

### Frontend (Vitest)
Run web tests from the `frontend` directory:
```bash

# run this in the project root directory
cd frontend
npm run test
```

---

## Deployment (CI/CD)

The project uses **GitHub Actions** for Continuous Integration and Deployment.

### Workflows
- **`ci.yml`**: Runs backend & frontend tests on all Pull Requests and non-main branches.
- **`cd.yml`**: Runs tests and then triggers deployment on pushes to `main`.
- **`reusable-tests.yml`**: Centralized test definitions shared by CI and CD.

### Configuration
Go to your GitHub repository **Settings > Secrets and variables > Actions** to configure:

#### Repository Secrets
- `RENDER_DEPLOY_HOOK_URL`: (Required) The unique deploy hook URL from your Render dashboard.

#### Repository Variables
- `RENDER_APP_URL`: (Required) The public URL of your live app (e.g. `https://yourapp.onrender.com`).
- `DEPLOY_WAIT_SECONDS`: (Optional) Seconds to wait before health check (Default: `300`).
- `HEALTH_CHECK_RETRIES`: (Optional) Number of health check attempts (Default: `3`).
- `HEALTH_CHECK_DELAY_SECONDS`: (Optional) Seconds between retries (Default: `60`).
