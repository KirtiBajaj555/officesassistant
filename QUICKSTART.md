# 🚀 Quick Start Guide - Office Assistant

Get up and running in 5 minutes!

## ⚡ Quick Setup

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements-api.txt

# Install Flutter dependencies
cd flutter_app
flutter pub get
cd ..
```

### Step 2: Configure Environment

Create `thecallagent/.env` file with your API keys:

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_secret
SIP_OUTBOUND_TRUNK_ID=ST_your_trunk_id
GOOGLE_API_KEY=your_google_api_key
DEEPGRAM_API_KEY=your_deepgram_key
```

### Step 3: Start Backend

**Option A: Using script**
```bash
./start_backend.sh
```

**Option B: Manual**
```bash
python3 api_server.py
```

### Step 4: Launch Flutter App

**Option A: Using script**
```bash
./start_flutter.sh
```

**Option B: Manual**
```bash
cd flutter_app
flutter run
```

## 🎯 First Steps

1. **Open the app** - You'll see a beautiful chat interface
2. **Send a message** - Try "Hello!" or "What can you do?"
3. **Make a call** - Click the `+` button and select "Make a Call"
4. **Explore features** - Ask about emails, calendar, documents, etc.

## 🖥️ Supported Platforms

Run on different platforms:

```bash
cd flutter_app

# Desktop
flutter run -d macos           # macOS
flutter run -d windows         # Windows
flutter run -d linux           # Linux

# Mobile (connect device first)
flutter run -d ios             # iPhone/iPad
flutter run -d android         # Android

# Web
flutter run -d chrome          # Browser
```

## 📦 Building for Distribution

### Windows Executable
```bash
cd flutter_app
flutter build windows --release
# Find .exe in: build/windows/runner/Release/
```

### macOS Application
```bash
cd flutter_app
flutter build macos --release
# Find .app in: build/macos/Build/Products/Release/
```

### Android APK
```bash
cd flutter_app
flutter build apk --release
# Find .apk in: build/app/outputs/flutter-apk/
```

### iOS App
```bash
cd flutter_app
flutter build ios --release
# Use Xcode to archive and distribute
```

## 🎨 UI Preview

The app features:
- 🎨 Modern gradient design (Blue/Purple theme)
- 💬 Smooth chat interface with animations
- 🌊 Glassmorphic cards with soft shadows
- ⚡ Real-time typing indicators
- 📱 Responsive across all screen sizes
- ✨ Beautiful micro-interactions

## 📞 Testing Phone Calls

1. Ensure backend is running
2. Click the `+` button in chat
3. Select "Make a Call"
4. Enter phone number with country code: `+1234567890`
5. Click "Call"

## 🔍 Troubleshooting

### Backend won't start
```bash
# Check Python version (needs 3.9+)
python3 --version

# Reinstall dependencies
pip install -r requirements-api.txt --force-reinstall
```

### Flutter app won't run
```bash
# Clean and rebuild
cd flutter_app
flutter clean
flutter pub get
flutter run
```

### Can't connect to backend
- Make sure backend is running on port 8000
- Check `lib/services/chat_service.dart` - baseUrl should be `http://localhost:8000`
- For mobile devices, use your computer's IP instead of localhost

### Phone calls not working
- Verify LiveKit credentials in `.env`
- Check SIP trunk ID is correct
- Ensure outbound calling is enabled in LiveKit dashboard

## 💡 Usage Tips

1. **Natural Language**: Chat naturally - "Schedule a meeting tomorrow at 2pm"
2. **Quick Actions**: Use the `+` button for common tasks
3. **Long Press**: Long press messages to copy text
4. **Menu Options**: Tap the `⋮` button for more options

## 🎯 Example Commands

Try these in the chat:
- "Hello, what can you help me with?"
- "Make a call to +1234567890"
- "Show me my calendar"
- "Read my latest emails"
- "Create a new document"
- "Analyze this data"

## 🚀 Next Steps

1. Customize the AI responses in `api_server.py`
2. Add more features to the Flutter UI
3. Connect to your email and calendar APIs
4. Deploy to production servers
5. Distribute apps to your team

## 📚 Documentation

- Full README: [README.md](README.md)
- API Documentation: http://localhost:8000/docs (when running)
- Flutter Docs: https://flutter.dev/docs

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed information
- Review the code comments in each file
- Test the API at http://localhost:8000/docs

---

**Happy Assisting! 🎉**

