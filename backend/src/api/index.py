import os
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

router = APIRouter()


def mount_static_files(app: FastAPI):
    """
    Setup static file serving for the React frontend.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.abspath(os.path.join(current_dir, "../../../frontend/dist"))
    assets_dir = os.path.join(static_dir, "assets")

    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    app.state.static_dir = static_dir


@router.get("/")
async def read_index(request: Request):
    """
    Serve the main index.html for the game frontend.
    """
    static_dir = getattr(request.app.state, "static_dir", None)

    if not static_dir:
        # Fallback if not set (though it should be)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.abspath(os.path.join(current_dir, "../../../frontend/dist"))

    return FileResponse(os.path.join(static_dir, "index.html"))
