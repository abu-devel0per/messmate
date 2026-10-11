# 🚀 MessMate — Production Deployment Guide

This guide covers deployment strategies for MessMate across Cloud (Render), Docker, and Mobile (Android APK).

---

## 1. Cloud Backend Deployment (Render)

The repository includes a ready-to-use [`render.yaml`](../render.yaml) blueprint:

```yaml
services:
  - type: web
    name: messmate-backend
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: uvicorn backend.server:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: MONGO_URL
        sync: false
      - key: JWT_SECRET
        generateValue: true
```

### Steps:
1. Connect your GitHub repository (`abu-devel0per/messmate`) in the [Render Dashboard](https://dashboard.render.com).
2. Choose **New > Blueprint** and link the repo.
3. Configure the environment variables (`MONGO_URL` pointing to MongoDB Atlas, `SMTP_*`, and `RAZORPAY_*`).
4. Trigger manual deploy or enable auto-deploy on `main` branch.

---

## 2. Containerized Deployment (Docker & Compose)

Deploy both backend and database using Docker Compose:

```bash
# Build and launch containers in background
docker compose up -d --build
```

The [`docker-compose.yml`](../docker-compose.yml) handles:
* MongoDB service on port `27017` with persistent volumes.
* FastAPI backend service on port `8000` with auto-restart policies.

---

## 3. Mobile Deployment & Android Release Builds

### Building Standalone APK with EAS (Expo Application Services):
```bash
# Log in to Expo
npx eas login

# Configure project ID
npx eas project:init

# Build Android Release APK
npx eas build -p android --profile production
```

### Direct Distribution:
Release APK files (`MessMate-Release.apk`) can be directly hosted or shared using the included Cloudflare tunnel script:
```powershell
python start_apk_share.py
```
This generates a public Cloudflare download URL and a scannable QR code in your terminal.
