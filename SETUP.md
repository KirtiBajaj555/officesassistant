# 🚀 Office Assistant - Complete Setup Guide

This guide covers everything you need to set up, run, and deploy the Office Assistant in both development and production environments.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Environment Configuration](#environment-configuration)
4. [Development Setup](#development-setup)
5. [Production Deployment with Docker](#production-deployment-with-docker)
6. [Running the Application](#running-the-application)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Flutter SDK** (3.0+) - [Install Flutter](https://flutter.dev/docs/get-started/install)
  ```bash
  flutter --version
  ```

- **Python** (3.9+)
  ```bash
  python3 --version
  ```

- **UV** (Python package manager) - [Install UV](https://github.com/astral-sh/uv)
  ```bash
  pip install uv
  ```

- **Docker** (for production deployment) - [Install Docker](https://docs.docker.com/get-docker/)
  ```bash
  docker --version
  docker-compose --version
  ```

### Required API Keys

You'll need the following API keys:

1. **Google AI (Gemini)** - [Get API Key](https://aistudio.google.com/app/apikey)
2. **LiveKit** (for voice calls) - [Sign up](https://cloud.livekit.io/)
3. **Google Cloud** (for Gmail/Calendar) - [Google Cloud Console](https://console.cloud.google.com/)

---

## Project Structure

```
officeagent/
├── backend/                    # Backend API (if using separate backend)
├── flutter_app/               # Flutter Frontend
│   ├── lib/
│   │   ├── main.dart
│   │   ├── services/
│   │   └── screens/
│   └── pubspec.yaml
├── thecallagent/              # Voice calling agent
│   ├── calling_agent.py
│   └── make_calls.py
├── gmail/                     # Gmail MCP server
│   └── server.py
├── calendar/                  # Calendar MCP server
│   └── server.py
├── api_server.py             # Main FastAPI server
├── main.py                   # LangChain AI agent
├── docker-compose.yml        # Docker configuration
├── .env.development          # Development environment variables
├── .env.production           # Production environment variables
├── requirements-api.txt      # Python dependencies
└── pyproject.toml           # Python project config
```

---

## Environment Configuration

### Development Environment (`.env.development`)

Create or update `.env.development`:

```bash
# LLM Configuration
GOOGLE_API_KEY=your_gemini_api_key_here

# LiveKit Configuration (for voice agent)
LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
SIP_OUTBOUND_TRUNK_ID=ST_xxxxx

# Environment
ENVIRONMENT=development

# Backend Configuration
BACKEND_PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Database (optional for development)
DATABASE_URL=sqlite:///./dev.db
```

### Production Environment (`.env.production`)

Create or update `.env.production`:

```bash
# LLM Configuration
GOOGLE_API_KEY=your_production_gemini_api_key

# LiveKit Configuration
LIVEKIT_URL=wss://your-production-livekit-url.livekit.cloud
LIVEKIT_API_KEY=your_production_livekit_api_key
LIVEKIT_API_SECRET=your_production_livekit_api_secret
SIP_OUTBOUND_TRUNK_ID=ST_xxxxx

# Environment
ENVIRONMENT=production

# Backend Configuration
BACKEND_URL=https://your-domain.com
BACKEND_PORT=8000
ALLOWED_ORIGINS=https://your-flutter-app.com,https://your-domain.com

# Database
DATABASE_URL=postgresql://user:password@db:5432/officeagent

# Security
SECRET_KEY=generate_a_secure_random_key_here

# Logging
LOG_LEVEL=INFO
```

### Create `.env` for Local Development

```bash
# Copy development config to .env
cp .env.development .env

# Edit with your actual API keys
nano .env  # or use your preferred editor
```

---

## Development Setup

### 1. Install Python Dependencies

```bash
# Navigate to project root
cd /home/keshavbajaj/officeagent

# Install dependencies using uv
uv pip install -r requirements-api.txt

# Verify installation
python3 -c "import fastapi; print('FastAPI installed successfully!')"
```

### 2. Install Flutter Dependencies

```bash
# Navigate to Flutter app
cd flutter_app

# Get dependencies
flutter pub get

# Verify Flutter setup
flutter doctor
```

### 3. Configure Google Cloud (for Gmail/Calendar)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable APIs:
   - Gmail API
   - Google Calendar API
4. Create OAuth 2.0 credentials
5. Download `credentials.json` and place in:
   - `gmail/credentials.json`
   - `calendar/credentials.json`

### 4. First-Time Authentication

```bash
# Authenticate Gmail
cd gmail
uv run server.py
# Follow the OAuth flow in your browser

# Authenticate Calendar
cd ../calendar
uv run server.py
# Follow the OAuth flow in your browser
```

This will create `token.json` files in each directory.

---

## Production Deployment with Docker

### 1. Prepare Environment

```bash
# Copy production config
cp .env.production .env

# Edit with your production values
nano .env
```

### 2. Build and Start Services

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 3. Docker Compose Services

The `docker-compose.yml` includes:

- **db**: PostgreSQL database
- **backend**: Main API server
- **voice-worker**: LiveKit voice agent

### 4. Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild specific service
docker-compose up -d --build backend

# View logs for specific service
docker-compose logs -f backend

# Scale backend (if needed)
docker-compose up -d --scale backend=3

# Restart a service
docker-compose restart backend
```

---

## Running the Application

### Development Mode (Local)

#### Option 1: Using Scripts

```bash
# Terminal 1: Start backend
./start_backend.sh

# Terminal 2: Start Flutter app
./start_flutter.sh
```

#### Option 2: Manual Start

**Terminal 1 - Backend API:**
```bash
cd /home/keshavbajaj/officeagent
python3 api_server.py
# Server runs on http://localhost:8000
```

**Terminal 2 - Voice Agent (Optional):**
```bash
cd /home/keshavbajaj/officeagent/thecallagent
python3 calling_agent.py
```

**Terminal 3 - Flutter App:**
```bash
cd /home/keshavbajaj/officeagent/flutter_app

# Run on web
flutter run -d chrome

# Run on desktop
flutter run -d macos    # macOS
flutter run -d windows  # Windows
flutter run -d linux    # Linux

# Run on mobile
flutter run             # Connected device/emulator
```

### Production Mode (Docker)

```bash
# Start all services
docker-compose up -d

# Access the application
# Backend API: http://your-domain.com:8000
# Flutter Web: Deploy separately or serve from nginx
```

### Building Flutter for Production

#### Web
```bash
cd flutter_app
flutter build web
# Output: build/web/
```

#### Desktop

**Windows:**
```bash
flutter build windows --release
# Output: build/windows/runner/Release/
```

**macOS:**
```bash
flutter build macos --release
# Output: build/macos/Build/Products/Release/
```

**Linux:**
```bash
flutter build linux --release
# Output: build/linux/x64/release/bundle/
```

#### Mobile

**Android:**
```bash
flutter build apk --release
# Output: build/app/outputs/flutter-apk/app-release.apk

# For Play Store:
flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab
```

**iOS:**
```bash
flutter build ios --release
# Then use Xcode to archive and upload to App Store
```

---

## API Endpoints

### Health Check
```bash
GET http://localhost:8000/
```

### Send Chat Message
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "message": "Hello, can you help me?"
}
```

### Make Phone Call
```bash
POST http://localhost:8000/make-call
Content-Type: application/json

{
  "phone_number": "+1234567890"
}
```

### Get Conversation History
```bash
GET http://localhost:8000/conversation-history
```

### Clear Conversation
```bash
DELETE http://localhost:8000/conversation-history
```

---

## Troubleshooting

### Backend Won't Start

**Issue:** Port 8000 already in use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)
```

**Issue:** Missing dependencies
```bash
# Reinstall dependencies
pip3 install -r requirements-api.txt --force-reinstall
```

### Flutter App Won't Build

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

### Can't Connect to Backend

**For Desktop/Web:**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `api_server.py`

**For Mobile Devices:**
Edit `flutter_app/lib/services/chat_service.dart`:
```dart
static const String baseUrl = 'http://YOUR_COMPUTER_IP:8000';
// Example: 'http://192.168.1.100:8000'
```

### Docker Issues

**Issue:** Container won't start
```bash
# Check logs
docker-compose logs backend

# Rebuild container
docker-compose up -d --build backend

# Remove all containers and rebuild
docker-compose down
docker-compose up -d --build
```

**Issue:** Database connection failed
```bash
# Check database is running
docker-compose ps db

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

### Google OAuth Issues

**Issue:** Token expired
```bash
# Delete old token
rm gmail/token.json
rm calendar/token.json

# Re-authenticate
cd gmail
uv run server.py
```

**Issue:** Invalid credentials
- Verify `credentials.json` is in the correct location
- Ensure OAuth consent screen is configured
- Check that required APIs are enabled in Google Cloud Console

### Voice Agent Issues

**Issue:** Calls not working
- Verify LiveKit credentials in `.env`
- Check SIP trunk ID starts with `ST_`
- Ensure outbound calling is enabled in LiveKit dashboard
- Phone number must be in international format: `+1234567890`

---

## Next Steps

After successful setup:

1. **Test the chat interface** - Send a message and verify response
2. **Test voice calls** - Make a test call to verify LiveKit integration
3. **Configure Gmail/Calendar** - Test email and calendar operations
4. **Customize AI responses** - Modify prompts in `main.py`
5. **Deploy to production** - Use Docker Compose for production deployment

---

## Production Checklist

### Security
- [ ] Enable HTTPS (SSL certificates)
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Use environment variables for secrets
- [ ] Enable secure token storage

### Scalability
- [ ] Add Redis for caching
- [ ] Implement connection pooling
- [ ] Set up load balancer
- [ ] Monitor resource usage

### Monitoring
- [ ] Set up logging (ELK/CloudWatch)
- [ ] Implement error tracking (Sentry)
- [ ] Add health check endpoints
- [ ] Set up uptime monitoring

### Deployment
- [ ] Configure CI/CD pipeline
- [ ] Set up database backups
- [ ] Create staging environment
- [ ] Document rollback procedures

---

## Support

For issues or questions:
- Check the logs: `docker-compose logs -f`
- Review API docs: `http://localhost:8000/docs`
- Test endpoints: Use the test scripts in the project

---

**Made with ❤️ for productivity and efficiency**

Last Updated: December 6, 2024
