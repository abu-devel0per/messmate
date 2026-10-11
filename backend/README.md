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

```bash
cp .env.example .env
# Edit .env with your configuration
```

Key variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `ENVIRONMENT` | `development` or `production` | Yes |
| `MONGO_URL` | MongoDB connection string | Yes |
| `DB_NAME` | Database name | Yes |
| `JWT_SECRET` | Secret key for JWT signing (min 32 chars) | Yes |
| `JWT_ALGORITHM` | `HS256` | Yes |
| `JWT_EXPIRE_MINUTES` | Token expiry (default: 10080 = 1 week) | Yes |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Path to Firebase service account JSON | For push notifications |
| `RAZORPAY_KEY_ID` | Razorpay key ID | For payments |
| `RAZORPAY_KEY_SECRET` | Razorpay key secret | For payments |
| `GMAIL_CLIENT_ID` | Gmail OAuth client ID | For email OTPs |
| `GMAIL_CLIENT_SECRET` | Gmail OAuth client secret | For email OTPs |
| `GMAIL_REFRESH_TOKEN` | Gmail OAuth refresh token | For email OTPs |

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

### Using Docker Compose (Recommended)

```bash
# From project root
docker-compose up -d
```

This starts:
- Backend API on port 8000
- MongoDB on port 27017
- Automatic database initialization

---

## 🧪 Testing & Verification

Run the automated test suites:

```bash
# Run pytest tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run E2E user journey test
python test_user_journey.py

# Run comprehensive QA suite
python comprehensive_qa.py
```

### Test Coverage

Target: **>80% code coverage**

View coverage report:
```bash
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

---

## 📁 Project Structure

```
backend/
├── server.py                 # Main FastAPI application
├── db_router.py             # Multi-tenant DB router
├── security.py              # Auth, rate limiting, encryption
├── ws_manager.py            # WebSocket manager
├── logger.py                # Structured logging
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container definition
├── .env.example            # Environment template
├── .flake8                 # Linter config
├── services/               # Business logic services
│   ├── email_service.py
│   ├── notification_service.py
│   └── storage_service.py
└── tests/                  # Test suite
    ├── __init__.py
    ├── test_coupons.py
    ├── test_free_trial_and_validation.py
    ├── test_iteration8_email_otp.py
    ├── test_iteration9_today_tomorrow.py
    ├── test_multi_database_routing.py
    └── test_student_notifications.py
```

---

## 🔧 Development Tools

### Code Quality

```bash
# Format with Black
black .

# Sort imports
isort .

# Lint with flake8
flake8 . --max-line-length=88 --extend-ignore=E203,W503

# Type check with mypy
mypy . --ignore-missing-imports
```

### Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

---

## 📚 API Documentation

Full API reference available at `/docs` when server is running.

Key endpoints:

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/api/auth/register` | Public | Register new account |
| `POST` | `/api/auth/verify-email` | Public | Verify email OTP |
| `POST` | `/api/auth/login` | Public | Login & get JWT |
| `GET` | `/api/auth/me` | Authenticated | Get current user |
| `GET` | `/api/student/today` | Student | Today's menu & RSVP |
| `PUT` | `/api/student/today` | Student | Update meal RSVP |
| `GET` | `/api/admin/dashboard` | Admin | Live headcount |
| `GET` | `/api/admin/cooking-quantities` | Admin | Ingredient calculator |
| `POST` | `/api/admin/wastage` | Admin | Record food wastage |
| `GET` | `/api/admin/students` | Admin | Student roster |
| `PUT` | `/api/admin/students/{id}/status` | Admin | Block/unblock student |
| `POST` | `/api/notifications/broadcast` | Admin | Send push notification |

---

## 🐛 Debugging

### Enable Debug Logging

```bash
ENVIRONMENT=development python -m uvicorn server:app --reload
```

### Common Issues

| Issue | Solution |
|-------|----------|
| MongoDB connection failed | Check `MONGO_URL` and ensure MongoDB is running |
| JWT decode error | Verify `JWT_SECRET` matches across services |
| Firebase errors | Check `FIREBASE_SERVICE_ACCOUNT_PATH` file exists |
| Email not sending | Verify Gmail OAuth credentials and refresh token |

---

## 📄 License

MIT License — see [LICENSE](../LICENSE) for details.