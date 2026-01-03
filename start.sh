#!/bin/bash

set -e  # Exit on error

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
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
    fi

    echo "Activating virtual environment and updating dependencies..."
    source .venv/bin/activate
    pip install -q -r "backend/requirements.txt"
    echo "Python environment ready."
}

build_frontend() {
    echo "Building frontend assets..."
    cd frontend
    npm install
    npm run build
    cd ..
    echo "Frontend build complete."
}

run_server() {
    local args=("$@")
    echo "Launching server..."
    cd backend
    python -m src.main "${args[@]}"
}

main() {
    # Navigate to the project root (where this script is located)
    cd "$(dirname "$0")"

    echo "Starting 2048 Game..."
    
    check_dependencies
    setup_python_env
    build_frontend
    run_server "$@"
}

# Execute main with all passed arguments
main "$@"
