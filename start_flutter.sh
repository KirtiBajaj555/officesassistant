#!/bin/bash

# Office Assistant Flutter App Startup Script

echo "📱 Starting Flutter Office Assistant App..."
echo "=================================="
echo ""

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed. Please install Flutter from https://flutter.dev"
    exit 1
fi

# Navigate to Flutter app directory
cd flutter_app

# Check for dependencies
if [ ! -d ".dart_tool" ]; then
    echo "📦 Installing Flutter dependencies..."
    flutter pub get
    echo ""
fi

# Run the app
echo "✨ Launching Flutter app..."
echo "   The app will connect to http://localhost:8000"
echo ""
flutter run

