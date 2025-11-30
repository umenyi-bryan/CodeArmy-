#!/bin/bash
echo "🚀 Starting Perfect Chat..."
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/umenyi-bryan/CodeArmy-/main/chat.py 2>/dev/null)" || python3 -c "$(wget -qO- https://raw.githubusercontent.com/umenyi-bryan/CodeArmy-/main/chat.py 2>/dev/null)" || echo "❌ Please check your internet connection"
