import uvicorn
import argparse


def main() -> None:
    """Driver logic to launch the FastAPI server."""
    parser = argparse.ArgumentParser(description="Run the 2048 Game Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    args = parser.parse_args()

    print(f"Starting 2048 game server at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server.")
    
    uvicorn.run(
        "src.server.app:app", 
        host=args.host, 
        port=args.port, 
        reload=args.reload
    )


if __name__ == "__main__":
    main()
