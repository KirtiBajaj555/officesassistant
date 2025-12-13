# 🐳 Docker Deployment Guide

This guide explains how to build and deploy the Office Assistant backend using Docker.

## ✅ Prerequisites

- Docker installed
- Google Cloud CLI (`gcloud`) installed (for Cloud Run)
- Your `GOOGLE_API_KEY` and other secrets ready

---
00
## 🛠️ 1. Build the Image

Run this command from the project root (`/home/keshavbajaj/officeagent`):

```bash
docker build -t office-assistant-backend -f backend/Dockerfile .
```

**Verify it works:**
```bash
docker run -p 8000:8000 --env-file .env office-assistant-backend
```
Then visit: http://localhost:8000/health

---

## ☁️ 2. Deploy to Google Cloud Run (Recommended)

Since you use Firebase and Gemini, Cloud Run is the best fit.

### Step A: Configure Google Cloud

```bash
# Login to Google Cloud
gcloud auth login

# Set your project (same as Firebase)
gcloud config set project theofficeassistant-de2f0

# Enable required services
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Step B: Push Image to Google Artifact Registry

```bash
# 1. Create a repository (if not exists)
gcloud artifacts repositories create backend-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Office Assistant Backend"

# 2. Configure Docker to authenticate
gcloud auth configure-docker us-central1-docker.pkg.dev

# 3. Tag the image
docker tag office-assistant-backend us-central1-docker.pkg.dev/theofficeassistant-de2f0/backend-repo/api:latest

# 4. Push the image
docker push us-central1-docker.pkg.dev/theofficeassistant-de2f0/backend-repo/api:latest
```

### Step C: Deploy Service

```bash
gcloud run deploy office-assistant-api \
  --image us-central1-docker.pkg.dev/theofficeassistant-de2f0/backend-repo/api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars GOOGLE_API_KEY=your_gemini_key_here \
  --set-env-vars LIVEKIT_URL=your_livekit_url \
  --set-env-vars LIVEKIT_API_KEY=your_key \
  --set-env-vars LIVEKIT_API_SECRET=your_secret \
  --set-env-vars ENVIRONMENT=production
```

**🎉 Success!** You will get a URL like: `https://office-assistant-api-xxxxx-uc.a.run.app`

---

## 🔄 3. Update Frontend

Once deployed, update your Flutter app to use the new URL.

**File:** `flutter_app/lib/services/chat_service.dart`

```dart
// Update the production URL
return 'https://office-assistant-api-xxxxx-uc.a.run.app';
```

**Redeploy Frontend:**
```bash
cd flutter_app
flutter build web --release
firebase deploy --only hosting --project theofficeassistant-de2f0
```

---

## ☁️ 3. Render.com Deployment (Easiest Docker Option)

Yes! You can deploy your Docker container directly to Render. This is often easier than Cloud Run or AWS.

### Step 1: Push Code to GitHub
Ensure your latest code (including `backend/Dockerfile` and `render.yaml`) is pushed to GitHub.

### Step 2: Create Web Service on Render
1. Go to **[dashboard.render.com](https://dashboard.render.com)**
2. Click **New +** → **Web Service**
3. Connect your repository (`KirtiBajaj555/officesassistant`)
4. Render will detect the `render.yaml` file automatically!
5. Click **Apply** or **Create Web Service**

### Step 3: Configure Environment Variables
Render might ask you to confirm environment variables. Ensure you add your real values for:
- `GOOGLE_API_KEY`
- `LIVEKIT_URL` (if using voice)
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`

### Step 4: Deploy
- Render will build your Docker image from `backend/Dockerfile`.
- It will start the service.
- You will get a URL like: `https://office-assistant-backend.onrender.com`

---

## ☁️ 4. AWS Deployment (Free Tier Option)

AWS is **not automatically free** for Docker (ECS/App Runner are paid), but you can use **EC2 Free Tier** (12 months).

### Option: Deploy to EC2 (Free Tier Eligible)

**Pros:** Free for 12 months (750 hours/mo).
**Cons:** Manual setup, manual updates.

1. **Launch Instance:**
   - Go to AWS Console → EC2 → Launch Instance
   - Name: `office-assistant`
   - OS: **Amazon Linux 2023** (Free tier eligible)
   - Instance Type: **t2.micro** or **t3.micro** (Free tier eligible)
   - Key Pair: Create new (download `.pem` file)
   - Network settings: Allow HTTP (80), HTTPS (443), and Custom TCP (8000)

2. **Connect & Install Docker:**
   ```bash
   # SSH into your instance
   ssh -i "your-key.pem" ec2-user@your-instance-public-ip

   # Install Docker
   sudo yum update -y
   sudo yum install -y docker
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   # Log out and log back in
   exit
   ```

3. **Run Your Container:**
   ```bash
   # Create .env file with your secrets
   nano .env
   
   # Run the container
   docker run -d -p 8000:8000 --env-file .env --restart always office-assistant-backend
   ```

4. **Public URL:**
   - Your API will be at: `http://your-instance-public-ip:8000`
   - **Note:** EC2 IP changes on restart unless you use an Elastic IP (free if attached).

---

## 🌍 Other Platforms

---

## 🐛 Troubleshooting

**Build Fails?**
- Ensure you are in the project root.
- Check `backend/Dockerfile` exists.

**Deploy Fails?**
- Check logs in Google Cloud Console.
- Ensure `GOOGLE_API_KEY` is valid.
- Ensure port 8000 is exposed.
