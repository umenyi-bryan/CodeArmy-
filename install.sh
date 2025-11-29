#!/bin/bash

echo "🎯 CodeArmy Chat - Universal Installer"
echo "======================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "🐍 Installing Python3..."
    pkg install python -y
fi

# Install websocket client
echo "📦 Installing dependencies..."
pip install websocket-client --quiet

# Download and run
echo "🚀 Launching CodeArmy Chat..."
curl -s https://raw.githubusercontent.com/umenyi-bryan/CodeArmy-/main/codearmy.py | python3
