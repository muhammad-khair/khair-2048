#!/bin/bash
# start.sh - Professional script to build and start the 2048 game

# Exit on error
set -e

# --- Functions ---

check_dependencies() {
    echo "Checking dependencies..."
    if ! command -v npm &> /dev/null; then
        echo "Error: npm is not installed. Please install Node.js (v18+) to continue."
        exit 1
    fi

    if ! command -v python3 &> /dev/null; then
        echo "Error: python3 is not installed. Please install Python (v3.11+) to continue."
        exit 1
    fi
    echo "Dependencies verified."
}

setup_python_env() {
    # 1. Setup Python virtual environment if missing
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
    fi

    echo "Activating virtual environment and updating dependencies..."
    source .venv/bin/activate
    pip install -q -r requirements.txt
    echo "Python environment ready."
}

build_frontend() {
    local force_rebuild=$1
    
    # Check if build output is missing or rebuild is forced
    if [ ! -d "web/dist" ] || [ "$force_rebuild" = true ]; then
        echo "Building frontend assets..."
        cd web
        if [ ! -d "node_modules" ]; then
            echo "Installing frontend dependencies (npm install)..."
            npm install
        fi
        npm run build
        cd ..
        echo "Frontend build complete."
    else
        echo "Frontend build already exists. Use --build to force a fresh build."
    fi
}

run_server() {
    local args=("$@")
    echo "Launching server..."
    python -m server.src.main "${args[@]}"
}

# --- Main Entry Point ---

main() {
    # Navigate to the project root (where this script is located)
    cd "$(dirname "$0")"

    # Process arguments
    local force_rebuild=false
    local server_args=()

    for arg in "$@"; do
        if [ "$arg" == "--build" ]; then
            force_rebuild=true
        else
            server_args+=("$arg")
        fi
    done

    echo "Starting 2048 Game..."
    
    check_dependencies
    setup_python_env
    build_frontend "$force_rebuild"
    run_server "${server_args[@]}"
}

# Execute main with all passed arguments
main "$@"
