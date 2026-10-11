# ⚙️ MessMate — Backend (FastAPI & MongoDB)

The high-performance asynchronous REST API and real-time backend engine for **MessMate**, built using **FastAPI**, **Motor (Async MongoDB)**, **Pydantic v2**, and **WebSockets**.

---

## 🛠️ Architecture & Core Modules

* **`server.py`**: The primary FastAPI application containing all REST endpoints, WebSocket handlers, and middleware.
* **`db_router.py`**: Multi-tenant database connection router ensuring complete data isolation per hostel/institution.
* **`security.py`**: Rate limiting, bcrypt password hashing, and token encryption algorithms.
* **`ws_manager.py`**: Asynchronous WebSocket connection pool manager for real-time headcount feeds.
* **`logger.py`**: Structured JSON and file logging system.

---

## 🔒 Single-Device Session Enforcement

To prevent unauthorized account sharing in college mess facilities:
1. Every user document stores an `active_session_id` UUID in MongoDB.
2. During login, email verification, or password reset, `rotate_session(user_id)` generates a new session UUID and encodes it into the JWT's `sid` claim.
3. Every protected API request validates that the JWT's `sid` matches the database's `active_session_id`.
4. If a session conflict occurs (e.g., student logs in on a friend's phone), any subsequent request from the previous device immediately receives:
   ```json
   {
     "code": "session_invalidated",
     "message": "You've been signed out because this account was signed in on another device."
   }
   ```

---

## 🔑 Environment Configuration

Create a `.env` file in the `backend/` directory using the provided `.env.example`:

```env
# Application Environment
ENVIRONMENT=development

# Database Settings
MONGO_URL=mongodb://localhost:27017
DB_NAME=messmate

# Multi-Tenant Sharding (Optional)
DATABASE_1_URI=mongodb://127.0.0.1:27017
DATABASE_1_NAME=messmate

# Authentication & Security
JWT_SECRET=your_super_secret_jwt_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080

# Email (SMTP for OTPs)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_google_app_password
FROM_EMAIL=your_email@gmail.com
FROM_NAME="MessMate Support"

# Razorpay Payments (Optional)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# Firebase Cloud Messaging (Optional)
# Place your 'firebase-adminsdk.json' service account file in this directory
```

---

## 🚀 Running the Backend

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start uvicorn server with hot reload
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation:
* Swagger UI: [**http://localhost:8000/docs**](http://localhost:8000/docs)
* ReDoc: [**http://localhost:8000/redoc**](http://localhost:8000/redoc)

### Running with Docker
```bash
# Build image
docker build -t messmate-backend .

# Run container
docker run -p 8000:8000 --env-file .env messmate-backend
```

---

## 🧪 Testing & Verification

Run the automated test suites:
```bash
# Run pytest tests
pytest tests/ -v

# Run E2E user journey test
python test_user_journey.py

# Run comprehensive QA suite
python comprehensive_qa.py
```
