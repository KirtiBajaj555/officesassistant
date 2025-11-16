# 🎯 Office Assistant - AI-Powered Productivity Suite

A beautiful, modern office assistant with AI-powered chat interface built with Flutter (frontend) and Python FastAPI (backend). Supports phone calls, email management, scheduling, and more!

## 🌟 Features

### ✨ Flutter UI
- **Beautiful Modern Design**: Glassmorphic UI with smooth gradients and animations
- **Responsive Chat Interface**: Real-time messaging with typing indicators
- **Cross-Platform**: Works on iOS, Android, Windows, macOS, Linux, and Web
- **Interactive Elements**: Smooth animations, transitions, and micro-interactions
- **Professional Theme**: Blue/Purple gradient theme optimized for office use

### 🚀 Backend Capabilities
- **Phone Calling**: Integrated LiveKit for high-quality VoIP calls
- **AI Chat Assistant**: Intelligent responses for various office tasks
- **Email Management**: Gmail integration via MCP
- **Calendar & Scheduling**: Meeting management and reminders
- **Document Handling**: File operations and organization
- **Data Analysis**: Process and analyze office data

## 📁 Project Structure

```
officesassistant/
├── flutter_app/              # Flutter Frontend
│   ├── lib/
│   │   ├── main.dart         # App entry point
│   │   ├── theme/            # Design system & themes
│   │   ├── models/           # Data models
│   │   ├── services/         # API & business logic
│   │   ├── widgets/          # Reusable UI components
│   │   └── screens/          # App screens
│   ├── assets/               # Images, fonts, etc.
│   └── pubspec.yaml          # Flutter dependencies
│
├── thecallagent/             # Python Backend - Calling Agent
│   ├── calling_agent.py      # LiveKit voice agent
│   ├── make_calls.py         # Call initiation logic
│   └── outbound-trunk.json   # SIP trunk configuration
│
├── api_server.py             # FastAPI REST API
├── main.py                   # LangChain AI agent
├── requirements-api.txt      # API dependencies
├── pyproject.toml            # Python project config
└── README.md                 # This file
```

## 🎨 Design System

### Colors
- **Primary Blue**: `#2563EB` - Trust & Professionalism
- **Deep Purple**: `#8B5CF6` - Innovation & Creativity
- **Hot Pink**: `#EC4899` - Energy & Accent
- **Light Background**: `#F8FAFC` - Clean & Modern

### Typography
- **Font**: Inter (Google Fonts)
- **Style**: Clean, modern, highly readable

### UI Components
- Glassmorphic cards with soft shadows
- Smooth gradient animations
- Rounded corners (16-24px)
- Ample spacing for breathability

## 🛠️ Setup Instructions

### Prerequisites
- **Flutter SDK**: 3.0+ ([Install Flutter](https://flutter.dev/docs/get-started/install))
- **Python**: 3.9+ 
- **UV**: Python package manager ([Install UV](https://github.com/astral-sh/uv))

### 1. Backend Setup

```bash
# Install Python dependencies
cd officesassistant
uv pip install -r requirements-api.txt

# Set up environment variables
cp thecallagent/.env.example thecallagent/.env
# Edit .env with your API keys:
# - GOOGLE_API_KEY
# - LIVEKIT_URL
# - LIVEKIT_API_KEY
# - LIVEKIT_API_SECRET
# - SIP_OUTBOUND_TRUNK_ID

# Start the FastAPI server
python api_server.py
# Server will run on http://localhost:8000
```

### 2. Flutter App Setup

```bash
# Navigate to Flutter app
cd flutter_app

# Get dependencies
flutter pub get

# Run on your preferred platform
flutter run -d chrome          # Web
flutter run -d macos           # macOS
flutter run -d windows         # Windows
flutter run                    # Mobile (connected device)

# Build for production
flutter build apk              # Android
flutter build ios              # iOS
flutter build windows          # Windows .exe
flutter build macos            # macOS .app
flutter build linux            # Linux
flutter build web              # Web app
```

### 3. Start Calling Agent (Optional)

```bash
# In a separate terminal
cd thecallagent
python calling_agent.py
```

## 🚀 Usage

### Running the Complete System

**Terminal 1** - API Server:
```bash
python api_server.py
```

**Terminal 2** - Calling Agent:
```bash
cd thecallagent
python calling_agent.py
```

**Terminal 3** - Flutter App:
```bash
cd flutter_app
flutter run
```

### Flutter App Features

1. **Chat Interface**: Type any question or command
2. **Make Calls**: Click the `+` button → "Make a Call"
3. **Attach Files**: Use the attachment button for documents
4. **Clear Chat**: Use the menu (⋮) → "Clear Chat"

### API Endpoints

```bash
# Health check
GET http://localhost:8000/

# Send chat message
POST http://localhost:8000/chat
{
  "message": "Hello, can you help me?"
}

# Make a phone call
POST http://localhost:8000/make-call
{
  "phone_number": "+1234567890"
}

# Get conversation history
GET http://localhost:8000/conversation-history

# Clear conversation
DELETE http://localhost:8000/conversation-history
```

## 📱 Building Distribution Packages

### Windows .exe
```bash
cd flutter_app
flutter build windows --release
# Output: build/windows/runner/Release/
```

### macOS .app
```bash
cd flutter_app
flutter build macos --release
# Output: build/macos/Build/Products/Release/
```

### iOS App Store
```bash
cd flutter_app
flutter build ios --release
# Then use Xcode to archive and upload
```

### Android APK/AAB
```bash
cd flutter_app
flutter build apk --release          # APK
flutter build appbundle --release    # AAB for Play Store
# Output: build/app/outputs/
```

## 🔧 Configuration

### Backend Configuration

Edit `api_server.py` to customize:
- Port number (default: 8000)
- CORS origins
- Response processing logic
- AI model integration

### Flutter Configuration

Edit `lib/services/chat_service.dart`:
```dart
static const String baseUrl = 'http://localhost:8000';
// Change to your production URL
```

## 🎯 Features to Implement

- [ ] Voice input/output in Flutter
- [ ] File upload functionality
- [ ] Push notifications
- [ ] Offline mode support
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] User authentication
- [ ] Conversation export
- [ ] Advanced analytics dashboard

## 🤝 Contributing

This is a private office assistant. For internal improvements:
1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit for review

## 📄 License

Proprietary - Internal Use Only

## 🆘 Troubleshooting

### Flutter App Not Connecting to Backend
- Ensure API server is running on `http://localhost:8000`
- Check CORS settings in `api_server.py`
- For mobile devices, use your computer's IP address instead of localhost

### Calling Agent Not Working
- Verify LiveKit credentials in `.env`
- Check SIP trunk configuration
- Ensure outbound trunk ID is correct

### Build Errors
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

## 📞 Support

For issues or questions, contact the development team.

---

**Made with ❤️ for productivity and efficiency**

