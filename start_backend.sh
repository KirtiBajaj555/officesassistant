#!/bin/bash

# Office Assistant Backend Startup Script
# This script starts the FastAPI server

echo "🚀 Starting Office Assistant Backend..."
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if .env file exists
if [ ! -f "thecallagent/.env" ]; then
    echo "⚠️  Warning: .env file not found in thecallagent/"
    echo "   Please create one with your API keys"
    echo ""
fi

# Start the API server
echo "✨ Starting FastAPI server on http://localhost:8000"
echo ""
python3 api_server.py

