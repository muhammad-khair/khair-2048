#!/bin/bash

set -e

WORKSPACE=/workspaces/khair-2048
echo "Setting up development environment..."

cd $WORKSPACE/backend
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -e ".[dev]"

cd $WORKSPACE/frontend
npm install

sudo chown -R vscode:vscode /home/vscode/.ssh

echo "Dev environment ready!"
