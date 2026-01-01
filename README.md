# khair-2048

A lightweight Python implementation of a **2048-style sliding tile game**.

The game is played on a square grid where numbers slides.
Matching numbers merge together, growing larger with each successful move.
The objective is to reach the goal tile (default: `2048`) before the board fills up and no more moves are possible.

---

## Setup

- Python **3.10+** (required for `match` statements and modern typing)

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

## Usage

You can run a simple main function over here:

```bash
python -m src.main
```

You may run tests with this command:

```bash
python -m pytest
```
