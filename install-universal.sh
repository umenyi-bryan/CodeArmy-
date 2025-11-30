#!/bin/bash
echo "🚀 Universal Anonymous Chat Installer"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "🐍 Installing Python3..."
    if command -v pkg &> /dev/null; then
        pkg install python -y
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install python3 -y
    elif command -v yum &> /dev/null; then
        sudo yum install python3 -y
    elif command -v brew &> /dev/null; then
        brew install python
    else
        echo "❌ Please install Python3 manually"
        exit 1
    fi
fi

echo "✅ Python3 is ready"
echo "🌐 Universal Chat can now run anywhere!"
echo ""
echo "🎯 To start chatting, run:"
echo "   python3 universal-one-liner.py"
echo ""
echo "🌍 This works on:"
echo "   • Termux (Android)"
echo "   • Linux"
echo "   • macOS" 
echo "   • Windows (with Python)"
echo "   • Anywhere with Python!"
