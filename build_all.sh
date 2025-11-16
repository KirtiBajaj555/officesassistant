#!/bin/bash

echo "🚀 Building Office Assistant for All Platforms..."
echo "=================================================="
echo ""

cd /Users/keshavbajaj/officesassistant/flutter_app

# Check if Flutter is available
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter not found. Please install Flutter first."
    exit 1
fi

echo "📋 Current platform: $(uname)"
echo ""

# Android
echo "📱 Building Android APK..."
if flutter build apk --release 2>&1 | tee /tmp/flutter_build.log; then
    echo "✅ Android APK built successfully!"
else
    echo "⚠️  Android build skipped or failed"
fi
echo ""

# Android App Bundle
echo "📦 Building Android App Bundle (for Play Store)..."
if flutter build appbundle --release 2>&1 | tee /tmp/flutter_build.log; then
    echo "✅ Android App Bundle built successfully!"
else
    echo "⚠️  Android App Bundle build skipped or failed"
fi
echo ""

# Web
echo "🌐 Building Web App..."
if flutter build web --release; then
    echo "✅ Web app built successfully!"
else
    echo "⚠️  Web build failed"
fi
echo ""

# macOS (only on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Building macOS App..."
    flutter config --enable-macos-desktop
    if flutter build macos --release; then
        echo "✅ macOS app built successfully!"
    else
        echo "⚠️  macOS build failed"
    fi
else
    echo "⏭️  Skipping macOS (not on macOS)"
fi
echo ""

# Windows (only on Windows)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "🪟 Building Windows EXE..."
    flutter config --enable-windows-desktop
    if flutter build windows --release; then
        echo "✅ Windows app built successfully!"
    else
        echo "⚠️  Windows build failed"
    fi
else
    echo "⏭️  Skipping Windows (not on Windows)"
fi
echo ""

# Linux (only on Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Building Linux App..."
    flutter config --enable-linux-desktop
    if flutter build linux --release; then
        echo "✅ Linux app built successfully!"
    else
        echo "⚠️  Linux build failed"
    fi
else
    echo "⏭️  Skipping Linux (not on Linux)"
fi
echo ""

echo "=================================================="
echo "🎉 Build Process Complete!"
echo "=================================================="
echo ""
echo "📁 Output Locations:"
echo ""
echo "Android APK:"
echo "  build/app/outputs/flutter-apk/app-release.apk"
echo ""
echo "Android App Bundle (Play Store):"
echo "  build/app/outputs/bundle/release/app-release.aab"
echo ""
echo "Web App:"
echo "  build/web/"
echo ""
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS App:"
    echo "  build/macos/Build/Products/Release/flutter_app.app"
    echo ""
fi
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Windows EXE:"
    echo "  build/windows/x64/release/runner/Release/flutter_app.exe"
    echo ""
fi
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux Binary:"
    echo "  build/linux/x64/release/bundle/"
    echo ""
fi

echo "📚 For publishing instructions, see: BUILD_AND_PUBLISH.md"
echo ""

