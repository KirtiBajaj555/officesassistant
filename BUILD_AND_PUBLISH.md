# 🚀 Build & Publish Guide - Office Assistant

Complete guide to build and publish your Office Assistant on all platforms!

---

## 📱 Android - Play Store / APK Distribution

### Prerequisites
- Android Studio installed (optional but recommended)
- Java JDK 11+ installed

### Build APK (For Testing/Direct Distribution)

```bash
cd /Users/keshavbajaj/officesassistant/flutter_app

# Build release APK
flutter build apk --release

# Output location:
# build/app/outputs/flutter-apk/app-release.apk
```

### Build AAB (For Google Play Store)

```bash
# Build App Bundle for Play Store
flutter build appbundle --release

# Output location:
# build/app/outputs/bundle/release/app-release.aab
```

### Setup for Play Store Publishing

1. **Create Keystore** (one-time setup):
```bash
keytool -genkey -v -keystore ~/office-assistant-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias office-assistant
```

2. **Create `android/key.properties`**:
```properties
storePassword=YOUR_STORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=office-assistant
storeFile=/Users/keshavbajaj/office-assistant-key.jks
```

3. **Update `android/app/build.gradle`**:
```gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    ...
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

4. **Upload to Play Store**:
   - Go to: https://play.google.com/console
   - Create app
   - Upload AAB file
   - Fill app details
   - Submit for review

---

## 🍎 iOS - App Store

### Prerequisites
- **macOS required**
- Xcode installed
- Apple Developer account ($99/year)

### Setup

```bash
# Install CocoaPods
sudo gem install cocoapods

# Setup iOS dependencies
cd /Users/keshavbajaj/officesassistant/flutter_app/ios
pod install
cd ..
```

### Build for Testing (Simulator)

```bash
# Run on iOS simulator
flutter run -d ios

# Or specific simulator
flutter run -d "iPhone 15 Pro"
```

### Build for Device Testing

```bash
# Build for connected iPhone/iPad
flutter build ios --release
```

### Build for App Store

1. **Open in Xcode**:
```bash
open ios/Runner.xcworkspace
```

2. **In Xcode**:
   - Select your Apple Developer account
   - Set Bundle Identifier: `com.yourcompany.officeassistant`
   - Set version and build number
   - Select "Any iOS Device" as target

3. **Archive & Upload**:
   - Product → Archive
   - Wait for build to complete
   - Click "Distribute App"
   - Select "App Store Connect"
   - Follow prompts to upload

4. **In App Store Connect**:
   - Go to: https://appstoreconnect.apple.com/
   - Create app listing
   - Add screenshots, description
   - Submit for review

### Quick Command (Alternative)

```bash
# Build IPA
flutter build ipa --release

# Output: build/ios/ipa/office_assistant.ipa
```

---

## 🌐 Web - Hosted Web App

### Build Web App

```bash
cd /Users/keshavbajaj/officesassistant/flutter_app

# Build for web
flutter build web --release

# Output location:
# build/web/
```

### Deploy to Hosting Services

#### Option 1: Firebase Hosting (Free)

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init hosting
# Select build/web as public directory

# Deploy
firebase deploy
```

#### Option 2: Vercel (Free)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd build/web
vercel
```

#### Option 3: Netlify (Free)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd build/web
netlify deploy --prod
```

#### Option 4: GitHub Pages (Free)

1. Push `build/web` contents to GitHub repository
2. Enable GitHub Pages in repository settings
3. Done!

#### Option 5: Any Web Server

Just upload the `build/web` folder contents to any web server:
- Apache
- Nginx
- Any hosting provider

---

## 🪟 Windows - EXE Application

### Prerequisites
- Windows 10/11 (or run in VM on Mac)
- Visual Studio 2019+ with C++ tools

### Build Windows EXE

```bash
cd /Users/keshavbajaj/officesassistant/flutter_app

# Enable Windows desktop
flutter config --enable-windows-desktop

# Build release
flutter build windows --release

# Output location:
# build/windows/x64/release/runner/Release/
```

### Executable Location
Your app will be at:
```
build/windows/x64/release/runner/Release/flutter_app.exe
```

### Create Installer (Optional)

#### Using Inno Setup (Free)

1. **Download Inno Setup**: https://jrsoftware.org/isinfo.php

2. **Create installer script** (`windows_installer.iss`):
```inno
[Setup]
AppName=Office Assistant
AppVersion=1.0
DefaultDirName={pf}\OfficeAssistant
DefaultGroupName=Office Assistant
OutputDir=installer
OutputBaseFilename=OfficeAssistantSetup

[Files]
Source: "build\windows\x64\release\runner\Release\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Office Assistant"; Filename: "{app}\flutter_app.exe"
Name: "{commondesktop}\Office Assistant"; Filename: "{app}\flutter_app.exe"
```

3. **Build installer**:
   - Open Inno Setup
   - Load the script
   - Compile

### Distribution
- Share the EXE directly
- Or create installer and distribute
- Or publish to Microsoft Store

---

## 🍎 macOS - .app Application

### Prerequisites
- macOS required
- Xcode installed

### Build macOS App

```bash
cd /Users/keshavbajaj/officesassistant/flutter_app

# Enable macOS desktop
flutter config --enable-macos-desktop

# Build release
flutter build macos --release

# Output location:
# build/macos/Build/Products/Release/flutter_app.app
```

### Create DMG Installer (Optional)

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "Office Assistant" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "flutter_app.app" 175 120 \
  --hide-extension "flutter_app.app" \
  --app-drop-link 425 120 \
  "OfficeAssistant.dmg" \
  "build/macos/Build/Products/Release/"
```

### Distribution Options

1. **Direct Distribution**:
   - Share the .app file (compress as ZIP)
   - Users drag to Applications folder

2. **DMG Distribution**:
   - Share the .dmg file
   - Professional installer experience

3. **Mac App Store**:
   - Similar to iOS App Store process
   - Requires Apple Developer account
   - Use Xcode to archive and upload

---

## 🐧 Linux - Binary Application

### Prerequisites
- Linux system (or VM/Docker)
- Build tools installed

### Setup (On Linux)

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev

# Or on other distros, install equivalent packages
```

### Build Linux App

```bash
cd /Users/keshavbajaj/officesassistant/flutter_app

# Enable Linux desktop
flutter config --enable-linux-desktop

# Build release
flutter build linux --release

# Output location:
# build/linux/x64/release/bundle/
```

### Create Package (Optional)

#### Option 1: AppImage (Universal)

```bash
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppImage structure
mkdir -p AppDir/usr/bin
cp -r build/linux/x64/release/bundle/* AppDir/usr/bin/
./appimagetool-x86_64.AppImage AppDir OfficeAssistant.AppImage
```

#### Option 2: .deb Package (Debian/Ubuntu)

```bash
# Install packaging tool
sudo apt-get install dpkg-deb

# Create package structure
mkdir -p office-assistant_1.0_amd64/DEBIAN
mkdir -p office-assistant_1.0_amd64/usr/local/bin

# Copy files
cp -r build/linux/x64/release/bundle/* office-assistant_1.0_amd64/usr/local/bin/

# Create control file
cat > office-assistant_1.0_amd64/DEBIAN/control << EOF
Package: office-assistant
Version: 1.0
Architecture: amd64
Maintainer: Your Name
Description: Office Assistant AI Application
EOF

# Build .deb
dpkg-deb --build office-assistant_1.0_amd64
```

### Distribution
- Share AppImage (works on most Linux distros)
- Share .deb for Debian/Ubuntu
- Share .rpm for RedHat/Fedora
- Publish to Snap Store or Flathub

---

## 📦 Quick Build All Platforms Script

Create `build_all.sh`:

```bash
#!/bin/bash

echo "🚀 Building Office Assistant for All Platforms..."
cd /Users/keshavbajaj/officesassistant/flutter_app

echo "📱 Building Android APK..."
flutter build apk --release

echo "🌐 Building Web..."
flutter build web --release

echo "🪟 Building Windows..."
flutter build windows --release 2>/dev/null || echo "Skipped (not on Windows)"

echo "🍎 Building macOS..."
flutter build macos --release

echo "🐧 Building Linux..."
flutter build linux --release 2>/dev/null || echo "Skipped (not on Linux)"

echo ""
echo "✅ Build Complete! Find your apps in:"
echo "   Android: build/app/outputs/flutter-apk/app-release.apk"
echo "   Web:     build/web/"
echo "   Windows: build/windows/x64/release/runner/Release/"
echo "   macOS:   build/macos/Build/Products/Release/flutter_app.app"
echo "   Linux:   build/linux/x64/release/bundle/"
```

Run it:
```bash
chmod +x build_all.sh
./build_all.sh
```

---

## 🎯 Platform-Specific Checklist

### Before Publishing Anywhere:

- [ ] Update version in `pubspec.yaml`
- [ ] Update app name and description
- [ ] Add app icon (all sizes)
- [ ] Add splash screen
- [ ] Test on real devices
- [ ] Create screenshots
- [ ] Write app description
- [ ] Prepare privacy policy
- [ ] Configure backend URL for production

### App Icons

Generate for all platforms:
```bash
# Install flutter_launcher_icons
flutter pub add flutter_launcher_icons

# Add to pubspec.yaml:
flutter_icons:
  android: true
  ios: true
  image_path: "assets/icon/icon.png"

# Generate
flutter pub run flutter_launcher_icons
```

---

## 💰 Cost Breakdown

| Platform | Cost | Notes |
|----------|------|-------|
| Android Play Store | $25 one-time | Developer account |
| iOS App Store | $99/year | Apple Developer account |
| Web Hosting | Free - $20/month | Many free options |
| Windows EXE | Free | Direct distribution |
| macOS .app | Free | Direct distribution |
| Linux Binary | Free | Direct distribution |
| Microsoft Store | $19 one-time | Optional for Windows |
| Mac App Store | $99/year | Same as iOS |

---

## 🚀 Recommended Publishing Order

1. **Web** (easiest, instant)
   - Deploy to Vercel/Netlify
   - Share link immediately
   - Get user feedback

2. **Windows EXE** (easy)
   - Build and share directly
   - Or create installer

3. **macOS .app** (medium)
   - Build and share as ZIP
   - Or create DMG

4. **Android APK** (medium)
   - Build and share for testing
   - Then submit to Play Store

5. **iOS App Store** (complex)
   - Requires most setup
   - Submit for review

6. **Linux** (optional)
   - Build if you have Linux users
   - Create AppImage for easy distribution

---

## 📱 Quick Test Commands

```bash
# Test on different platforms
flutter run -d chrome              # Web
flutter run -d windows             # Windows
flutter run -d macos               # macOS  
flutter run -d android             # Android (device connected)
flutter run -d ios                 # iOS (simulator)
flutter run -d linux               # Linux
```

---

## 🔗 Useful Links

- Flutter Build Docs: https://docs.flutter.dev/deployment
- Play Store Console: https://play.google.com/console
- App Store Connect: https://appstoreconnect.apple.com
- Firebase Hosting: https://firebase.google.com/products/hosting
- Microsoft Store: https://partner.microsoft.com/dashboard

---

## 🆘 Troubleshooting

### Build Fails?
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter build [platform] --release
```

### iOS Signing Issues?
- Check Apple Developer account
- Verify Bundle Identifier
- Update provisioning profiles

### Android Signing Issues?
- Verify keystore path
- Check passwords in key.properties
- Ensure keystore file exists

---

## 🎉 You're Ready!

Your Office Assistant can now be published on:
✅ Android (Play Store or APK)
✅ iOS (App Store)
✅ Web (hosted anywhere)
✅ Windows (EXE file)
✅ macOS (APP file)
✅ Linux (binary)

**One codebase, six platforms!** 🚀

---

**Need help with a specific platform? Check the detailed sections above!**

