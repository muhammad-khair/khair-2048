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

## Setup

- Python **3.11+**
- Node.js **18+**

### Backend Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd web
npm install
npm run build  # Builds the React app into web/dist for the server to serve
```

---

## Running the Game

1. **Activate the environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Start the server**:
   ```bash
   python -m server.src.main
   ```
   *The server will start at `http://127.0.0.1:8000`.*

3. **Play the game**:
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

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
