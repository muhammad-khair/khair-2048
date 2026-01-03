import argparse
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from server.src.routes import router

app = FastAPI(title="2048 Game API")

# Include the API router with the prefix
app.include_router(router, prefix="/api")

# Setup static file serving for the React frontend
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.abspath(os.path.join(current_dir, "../../web/dist"))
assets_dir = os.path.join(static_dir, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/")
async def read_index():
    """
    Serve the main index.html file for the game frontend.
    """
    return FileResponse(os.path.join(static_dir, "index.html"))


def main() -> None:
    """Driver logic to launch the FastAPI server."""
    parser = argparse.ArgumentParser(description="Run the 2048 Game Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    args = parser.parse_args()

    print(f"Starting 2048 game server at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server.")
    
    # Run uvicorn with the app instance
    # Note: reload works best when passing string import, but passing app instance directly is also fine for simple use
    # If reload is True, we must use import string.
    
    if args.reload:
        uvicorn.run(
            "server.src.main:app", 
            host=args.host, 
            port=args.port, 
            reload=True
        )
    else:
        uvicorn.run(
            app, 
            host=args.host, 
            port=args.port
        )


if __name__ == "__main__":
    main()
