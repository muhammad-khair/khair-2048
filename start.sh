#!/bin/bash
# start.sh - Simple script to build and start the 2048 game

# Exit on error
set -e

# Navigate to the project root (where this script is located)
cd "$(dirname "$0")"

echo "🚀 Starting 2048 Game..."

# 1. Build frontend if dist is missing or if --build flag is provided
REBUILD=false
for arg in "$@"; do
    if [ "$arg" == "--build" ]; then
        REBUILD=true
        break
    fi
done

if [ ! -d "web/dist" ] || [ "$REBUILD" = true ]; then
    echo "📦 Building frontend assets..."
    cd web
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    npm run build
    cd ..
fi

# 2. Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
fi

# 3. Launch the server
echo "🌐 Launching server..."
# Filter out --build from the arguments passed to the server
SERVER_ARGS=()
for arg in "$@"; do
    if [ "$arg" != "--build" ]; then
        SERVER_ARGS+=("$arg")
    fi
done

python -m server.src.main "${SERVER_ARGS[@]}"
