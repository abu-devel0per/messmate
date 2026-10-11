# 📖 MessMate — API Documentation

This document describes the REST API endpoints available in the MessMate FastAPI backend.

All secured endpoints require the standard Bearer authentication header:
```http
Authorization: Bearer <your_jwt_access_token>
```

---

## 1. Authentication Endpoints

### `POST /api/auth/register`
Register a new student or administrator account.
* **Body**:
  ```json
  {
    "full_name": "Alex Johnson",
    "email": "alex@university.edu",
    "password": "SecurePassword123!",
    "role": "student",
    "hostel": "Aryabhatta Hostel",
    "room_number": "B-204",
    "phone": "+919876543210"
  }
  ```
* **Response `201 Created`**:
  ```json
  {
    "message": "Registration successful. Please verify your email with the OTP sent.",
    "user_id": "6704..."
  }
  ```

### `POST /api/auth/verify-email`
Verifies registration with the 6-digit email OTP and issues the initial session JWT.
* **Body**: `{"email": "alex@university.edu", "otp": "492019"}`
* **Response `200 OK`**: `{"access_token": "...", "token_type": "bearer", "user": {...}}`

### `POST /api/auth/login`
Authenticates an active user, rotates `active_session_id`, and issues a session-bound JWT.
* **Body**: `{"email": "alex@university.edu", "password": "SecurePassword123!"}`
* **Response `200 OK`**: `{"access_token": "...", "user": {...}}`

### `GET /api/auth/me`
Fetches the currently authenticated profile and validates session freshness.
* **Response `200 OK`**: Current profile object.
* **Response `401 Unauthorized`**: If session was revoked by another device login (`{"code": "session_invalidated"}`).

---

## 2. Student Endpoints

### `GET /api/student/today`
Returns today's active menu and student's meal participation status.
* **Response `200 OK`**:
  ```json
  {
    "date": "2026-10-11",
    "breakfast": {"attending": true, "menu": "Masala Dosa, Sambar, Chutney", "cutoff": "07:30"},
    "lunch": {"attending": true, "menu": "Rice, Dal Tadka, Paneer Butter Masala", "cutoff": "11:30"},
    "dinner": {"attending": false, "menu": "Roti, Mix Veg, Gulab Jamun", "cutoff": "18:30"}
  }
  ```

### `PUT /api/student/today`
Updates meal RSVP flags prior to the meal cutoff time.
* **Body**:
  ```json
  {
    "date": "2026-10-11",
    "meals": {
      "breakfast": true,
      "lunch": true,
      "dinner": false
    }
  }
  ```

### `GET /api/student/weekly-menu`
Returns the 7-day cyclical menu for the student's assigned hostel.

---

## 3. Admin & Mess Manager Endpoints

### `GET /api/admin/dashboard`
Fetches real-time headcounts, today's attendance summary, and active alerts.
* **Response `200 OK`**:
  ```json
  {
    "total_students": 350,
    "breakfast_rsvps": 284,
    "lunch_rsvps": 312,
    "dinner_rsvps": 265,
    "pending_approvals": 4
  }
  ```

### `GET /api/admin/cooking-quantities`
Computes required raw cooking quantities based on attending RSVPs and configured buffer margin.
* **Parameters**: `meal=lunch&buffer_percent=5`
* **Response `200 OK`**:
  ```json
  {
    "attending_count": 312,
    "buffered_headcount": 328,
    "items": [
      {"name": "Rice", "quantity_kg": 49.2},
      {"name": "Dal", "quantity_kg": 24.6},
      {"name": "Paneer", "quantity_kg": 36.0}
    ]
  }
  ```

### `POST /api/admin/wastage`
Records post-meal leftover food weights and calculates financial waste.
* **Body**:
  ```json
  {
    "date": "2026-10-11",
    "meal": "lunch",
    "food_prepared_kg": 140.0,
    "food_wasted_kg": 6.5,
    "cost_per_kg": 85.0
  }
  ```

### `GET /api/admin/students`
Lists students with optional filters (`status=pending`, `status=active`, `status=blocked`).

### `PUT /api/admin/students/{user_id}/status`
Updates account status (`active`, `blocked`, or `approved`).

---

## 4. Notifications & Broadcasts

### `POST /api/notifications/broadcast`
Broadcasts an instant push notification via Firebase Cloud Messaging (FCM) to all students in the hostel.
* **Body**:
  ```json
  {
    "title": "Special Dinner Notice",
    "body": "Special Diwali Feast scheduled for tonight. Meal cutoff extended to 19:30.",
    "priority": "high"
  }
  ```
