# khair-2048

A lightweight Python implementation of a **2048-style sliding tile game** with a modern web interface.

The game is played on a square grid where numbers slides.
Matching numbers merge together, growing larger with each successful move.
The objective is to reach the goal tile (default: `2048`) before the board fills up and no more moves are possible.

![2048 Game UI](docs/images/ui_screenshot.png)

---

## Setup

- Python **3.11+** (required for `match` statements and modern typing)

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate  # you should see a (.venv) before your input $
pip install -r requirements.txt
```

If you want to deactivate, run the following:

```bash
deactivate  # if you want to deactivate the virtual environment
```

### Windows

```powershell
python3 -m venv .venv
.venv\Scripts\Activate.ps1  # you should see a (.venv) before your input $
pip install -r requirements.txt
```

If you want to deactivate, run the following:

```bash
deactivate  # if you want to deactivate the virtual environment
```

---

## Web Interface & API

This project now includes a **FastAPI backend** and a **responsive web-based UI**.

### Running the Web Game

1. **Activate the environment and install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   python src.main
   ```
   *The server will start at `http://127.0.0.1:8000` by default.*

3. **Play the game**:
   Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).
   - Use **Arrow Keys** or **WASD** to move tiles.
   - On mobile, **Swipe** in any direction.
   - Use the **UI Buttons** for manual control.

---

## Technical Details

- **Backend**: Python with FastAPI (Stateless).
- **Frontend**: React (Vite, Hooks).
- **Testing**: Pytest (Backend), Vitest (Frontend CLI).
- **State Management**: The backend is stateless; it takes a grid and a direction, then returns the resulting grid and status.

## Alternative Usage (CLI & Testing)

You can still run a simple CLI demo:

```bash
python -m src.main --help  # See available uvicorn options
```

Run backend unit tests:

```bash
pytest
```

Run web unit tests (CLI):

```bash
cd src/web && npm run test
```

Generate a backend test report:

```bash
pytest --junitxml=test_report.xml
```
