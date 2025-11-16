# 🚀 Installation Guide - Office Assistant

Complete step-by-step installation instructions for your Office Assistant.

---

## ⚡ Prerequisites

Before starting, ensure you have:

### Required Software
- ✅ **Flutter SDK** (3.0 or higher)
  - Download: https://flutter.dev/docs/get-started/install
  - Verify: `flutter --version`

- ✅ **Python** (3.9 or higher)
  - Download: https://www.python.org/downloads/
  - Verify: `python3 --version`

- ✅ **Git** (for version control)
  - Download: https://git-scm.com/downloads
  - Verify: `git --version`

### Optional Tools
- **VS Code** or **Android Studio** (for Flutter development)
- **Xcode** (for iOS/macOS builds - Mac only)
- **Android SDK** (for Android builds)

---

## 📦 Step 1: Install Python Dependencies

```bash
# Navigate to project root
cd /Users/keshavbajaj/officesassistant

# Install Python packages
pip3 install -r requirements-api.txt

# Or using uv (faster)
uv pip install -r requirements-api.txt
```

**Verify installation:**
```bash
python3 -c "import fastapi; print('FastAPI installed successfully!')"
```

---

## 📱 Step 2: Install Flutter Dependencies

```bash
# Navigate to Flutter app
cd flutter_app

# Get dependencies
flutter pub get

# Verify Flutter setup
flutter doctor
```

**Expected output:**
```
✓ Flutter (Channel stable, 3.x.x)
✓ Connected device (1 available)
✓ No issues found!
```

---

## 🔐 Step 3: Configure Environment Variables

Create `.env` file in `thecallagent/` folder:

```bash
# Create .env file
touch thecallagent/.env
```

**Edit `thecallagent/.env` with your API keys:**

```env
# LiveKit Configuration (for phone calls)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
SIP_OUTBOUND_TRUNK_ID=ST_your_sip_trunk_id

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Deepgram Configuration (for voice)
DEEPGRAM_API_KEY=your_deepgram_api_key
```

### 🔑 Where to Get API Keys

**LiveKit** (for phone calls):
1. Sign up at https://cloud.livekit.io/
2. Create a new project
3. Get API credentials from project settings
4. Set up SIP trunk for phone calls

**Google AI**:
1. Visit https://aistudio.google.com/app/apikey
2. Create API key
3. Copy and paste into `.env`

**Deepgram** (for voice):
1. Sign up at https://deepgram.com/
2. Get API key from dashboard
3. Add to `.env`

---

## ✅ Step 4: Verify Installation

### Test Backend

```bash
# Start API server
python3 api_server.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test in browser:**
- Open: http://localhost:8000
- Should see: `{"status": "online", ...}`
- API docs: http://localhost:8000/docs

### Test Flutter App

```bash
# In new terminal
cd flutter_app

# Run app (will open in available device)
flutter run
```

**For specific platform:**
```bash
flutter run -d chrome          # Web browser
flutter run -d macos           # macOS desktop
flutter run -d windows         # Windows desktop
```

---

## 🏃 Step 5: Run the Complete System

### Using Scripts (Recommended)

**Terminal 1 - Backend:**
```bash
cd /Users/keshavbajaj/officesassistant
./start_backend.sh
```

**Terminal 2 - Flutter App:**
```bash
cd /Users/keshavbajaj/officesassistant
./start_flutter.sh
```

### Manual Start

**Terminal 1 - Backend:**
```bash
cd /Users/keshavbajaj/officesassistant
python3 api_server.py
```

**Terminal 2 - Flutter App:**
```bash
cd /Users/keshavbajaj/officesassistant/flutter_app
flutter run
```

**Terminal 3 - Calling Agent (Optional):**
```bash
cd /Users/keshavbajaj/officesassistant/thecallagent
python3 calling_agent.py
```

---

## 🎯 Step 6: First Use

1. **Open the app** - Beautiful chat interface appears
2. **Send test message** - Type "Hello" and press send
3. **Check response** - AI should respond with capabilities
4. **Test features** - Try making a call or asking questions

---

## 🔧 Platform-Specific Setup

### macOS

```bash
# Enable desktop support
flutter config --enable-macos-desktop

# Build and run
cd flutter_app
flutter build macos
open build/macos/Build/Products/Release/flutter_app.app
```

### Windows

```bash
# Enable desktop support
flutter config --enable-windows-desktop

# Build and run
cd flutter_app
flutter build windows
# Run: build\windows\runner\Release\flutter_app.exe
```

### Linux

```bash
# Enable desktop support
flutter config --enable-linux-desktop

# Install dependencies (Ubuntu/Debian)
sudo apt-get install clang cmake ninja-build pkg-config libgtk-3-dev

# Build and run
cd flutter_app
flutter build linux
./build/linux/x64/release/bundle/flutter_app
```

### iOS

```bash
# Requires macOS and Xcode
cd flutter_app
flutter build ios
# Open Xcode and run on simulator or device
open ios/Runner.xcworkspace
```

### Android

```bash
# Connect Android device or start emulator
cd flutter_app
flutter devices          # Check connected devices
flutter build apk        # Build APK
flutter install          # Install on device
```

### Web

```bash
cd flutter_app
flutter build web
# Serve locally
python3 -m http.server 8080 -d build/web
# Open: http://localhost:8080
```

---

## 📦 Building Production Releases

### Windows .exe

```bash
cd flutter_app
flutter build windows --release

# Output location:
# build/windows/runner/Release/flutter_app.exe

# Create installer (optional - using Inno Setup)
# Download Inno Setup: https://jrsoftware.org/isinfo.php
```

### macOS .app

```bash
cd flutter_app
flutter build macos --release

# Output location:
# build/macos/Build/Products/Release/flutter_app.app

# Create DMG (optional)
# Use "Disk Utility" to create DMG from .app
```

### Android APK

```bash
cd flutter_app
flutter build apk --release

# Output location:
# build/app/outputs/flutter-apk/app-release.apk

# For Play Store (AAB):
flutter build appbundle --release
# build/app/outputs/bundle/release/app-release.aab
```

### iOS App

```bash
cd flutter_app
flutter build ios --release

# Then in Xcode:
# 1. Open ios/Runner.xcworkspace
# 2. Product → Archive
# 3. Distribute App → App Store Connect
```

---

## 🐛 Troubleshooting

### Issue: Backend won't start

**Solution:**
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Reinstall dependencies
pip3 install -r requirements-api.txt --force-reinstall

# Check port 8000
lsof -ti:8000  # If occupied, kill process
```

### Issue: Flutter app won't build

**Solution:**
```bash
cd flutter_app

# Clean project
flutter clean

# Re-get dependencies
flutter pub get

# Check Flutter setup
flutter doctor -v

# Update Flutter
flutter upgrade
```

### Issue: Can't connect to backend

**For Desktop/Web:**
- Backend URL: `http://localhost:8000`
- Verify backend is running
- Check CORS settings in `api_server.py`

**For Mobile Devices:**
```dart
// Edit: flutter_app/lib/services/chat_service.dart
// Change:
static const String baseUrl = 'http://YOUR_COMPUTER_IP:8000';
// Example: 'http://192.168.1.100:8000'
```

### Issue: Phone calls not working

**Check:**
1. LiveKit credentials in `.env` are correct
2. SIP trunk ID starts with `ST_`
3. Outbound calling is enabled in LiveKit dashboard
4. Phone number is in international format: `+1234567890`

### Issue: Missing dependencies

```bash
# Flutter
cd flutter_app
flutter pub get
flutter pub upgrade

# Python
pip3 install -r requirements-api.txt --upgrade
```

---

## 🔍 Verification Checklist

Before using in production, verify:

- [ ] Backend starts without errors
- [ ] Flutter app builds successfully
- [ ] Can send and receive messages
- [ ] API endpoints respond correctly
- [ ] Phone call initiation works
- [ ] UI is responsive and smooth
- [ ] Error handling works properly
- [ ] All API keys are configured
- [ ] Environment variables are set
- [ ] Documentation is accessible

---

## 📞 Support & Help

### Quick Help

1. **Check logs:**
   - Backend: Terminal output from `api_server.py`
   - Flutter: Terminal output from `flutter run`

2. **Test API:**
   - Visit: http://localhost:8000/docs
   - Try endpoints directly

3. **Flutter DevTools:**
   ```bash
   flutter pub global activate devtools
   flutter pub global run devtools
   ```

### Documentation

- [README.md](README.md) - Complete documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Project details
- [DESIGN_SPEC.md](DESIGN_SPEC.md) - Design system

---

## 🎉 You're All Set!

Your Office Assistant is now installed and ready to use!

**Next steps:**
1. Explore the chat interface
2. Try making a phone call
3. Customize the AI responses
4. Build for your target platform
5. Deploy to your team

**Enjoy your new assistant!** 🚀

---

**Last Updated:** November 16, 2025

