#!/bin/bash
# Office Agent - Flutter Web Runner
# This script runs Flutter web with a FIXED port (8080)
# to avoid Google OAuth issues with random ports

cd "$(dirname "$0")"
echo "🚀 Starting Office Agent Flutter Web on port 8080..."
echo "📱 App will open at: http://localhost:8080"
echo ""
flutter run -d chrome --web-port=8080
