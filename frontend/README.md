# 📱 MessMate — Frontend (React Native & Expo)

The cross-platform frontend for **MessMate**, built using **React Native 0.81**, **Expo 54**, and **Expo Router 6**. It provides a responsive, eco-minimalist user experience tailored for students, hostel wardens, and mess administrators across Android, iOS, and Web.

---

## 🏗️ Architecture & Navigation

MessMate frontend utilizes Expo Router's file-based routing architecture:

```text
app/
├── index.tsx                 # Landing / Role selector screen (Student vs Admin)
├── _layout.tsx               # Root provider stack (Theme, Auth, Toast, QueryClient)
├── (auth)/                   # Authentication flows
│   ├── student-login.tsx     # Student email/password sign-in
│   ├── admin-login.tsx       # Admin/Warden credentials sign-in
│   ├── register.tsx          # New account registration with hostel selection
│   ├── verify-email.tsx      # Email OTP verification
│   ├── forgot-password.tsx   # Password reset request
│   ├── forgot-password-otp.tsx# OTP input for password reset
│   └── reset-password.tsx    # New password entry
├── (student)/                # Student Portal
│   ├── _layout.tsx           # Student bottom tab navigation
│   ├── home.tsx              # Today's meals RSVP scheduler & countdowns
│   ├── menu.tsx              # 7-day cyclical mess menu calendar
│   ├── wastage.tsx           # Eco impact & food waste awareness dashboard
│   └── settings.tsx          # Profile, theme switch, preferences & active session
└── (admin)/                  # Mess Manager / Admin Portal
    ├── _layout.tsx           # Admin bottom tab navigation
    ├── dashboard.tsx         # Live headcount attendance overview
    ├── necessary-info.tsx    # Recipe & cooking quantity calculator
    ├── students-status.tsx   # Student roster, approvals & block/unblock controls
    ├── wastage-calc.tsx      # Leftover food waste logger & cost estimation
    ├── billing.tsx           # Mess dues, invoices & Razorpay collection
    ├── notifications.tsx     # Campus-wide push notification dispatch
    └── settings.tsx          # Hostel settings & meal cutoff configurations
```

---

## 🎨 Design System & Theme

* **Design Philosophy**: Apple-style eco-minimalism designed to encourage sustainability.
* **Tokens**: Defined in [`src/theme.tsx`](./src/theme.tsx) with support for light and dark modes.
* **Palette**: Organic Forest Greens (`#248243`), Clean Slate Backgrounds (`#F9F9F9`), and High-Contrast Accents.

---

## 🔐 Session Management & Interceptors

In [`src/api/client.ts`](./src/api/client.ts) and [`src/auth/AuthContext.tsx`](./src/auth/AuthContext.tsx):
* Every outgoing request carries the JWT access token from `SecureStore` (or `AsyncStorage` on Web).
* If another device logs into the same account, the server responds with HTTP 401 code `session_invalidated`.
* The client interceptor automatically catches this response, purges local credentials, displays a notification, and redirects the user back to the sign-in screen.

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Variables
Create a `.env` file in the `frontend` root:
```env
EXPO_PUBLIC_BACKEND_URL=http://localhost:8000
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_ENV=development
```
> **Note for Physical Device Testing**: Replace `localhost` with your computer's local IP address (e.g., `192.168.1.50`).

### 3. Launch Development Server

* **Web Browser**:
  ```bash
  npm run web
  ```
  Launches on [http://localhost:8081](http://localhost:8081).

* **Expo Go / Physical Device**:
  ```bash
  npx expo start
  ```
  Scan the QR code in your terminal with the Expo Go app.

* **Android Emulator**:
  ```bash
  npm run android
  ```

---

## 📦 Building Production APKs

To build a standalone release APK:
```bash
# Using EAS Build (Expo Cloud)
npx eas build -p android --profile production

# Or local Android build
npx expo run:android --variant release
```
Pre-built release APKs are available in the repository root (`MessMate-Release.apk`).
