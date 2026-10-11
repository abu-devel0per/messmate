# 🏛️ MessMate — Architecture & System Design

MessMate is a multi-tenant cloud application engineered to streamline university and private hostel dining operations, reduce institutional food waste, and automate daily student attendance and kitchen inventory.

---

## 1. High-Level System Architecture

```mermaid
graph TD
    subgraph Clients ["Client Platforms"]
        AndroidApp["Android App (React Native)"]
        iOSApp["iOS App (React Native)"]
        WebApp["Web Portal (React Native Web)"]
    end

    subgraph Gateway ["Edge & Network Layer"]
        LoadBalancer["Reverse Proxy / SSL Termination"]
        RateLimiter["Rate Limiter (FastAPI Middleware)"]
    end

    subgraph Services ["Application Layer (FastAPI Core)"]
        AuthSvc["Auth & Session Manager (JWT + SID Rotation)"]
        MealSvc["Meal Planning & Cut-off Engine"]
        WastageSvc["Wastage Analytics & Carbon Tracker"]
        NotifSvc["FCM Notification Dispatcher"]
        BillingSvc["Razorpay Subscription Service"]
        WSServer["Headcount WebSocket Broadcaster"]
    end

    subgraph Storage ["Persistence Layer"]
        MongoDB[("MongoDB Clusters (Multi-Tenant Collections)")]
        SecureStore[("Expo SecureStore / Local Storage")]
    end

    Clients --> LoadBalancer
    LoadBalancer --> RateLimiter
    RateLimiter --> AuthSvc
    RateLimiter --> MealSvc
    RateLimiter --> WastageSvc
    RateLimiter --> NotifSvc
    RateLimiter --> BillingSvc
    Clients --> WSServer

    AuthSvc --> MongoDB
    MealSvc --> MongoDB
    WastageSvc --> MongoDB
    NotifSvc --> MongoDB
    BillingSvc --> MongoDB
    WSServer --> MongoDB

    Clients -.-> SecureStore
```

---

## 2. Multi-Tenancy Architecture

MessMate implements logical tenant isolation at the application and database layer:
* **Tenant Identification**: Every user, menu item, daily plan, wastage entry, and subscription is partitioned by `hostel` / `institution_or_hostel_name`.
* **Tenant Scoping Dependency**: All protected endpoints enforce the `require_tenant_access` dependency. Requests attempting cross-hostel access are blocked with HTTP 403 Forbidden.
* **Flexible Database Router (`db_router.py`)**: Supports single database tenancy as well as dynamic connection routing across multiple distributed database clusters.

---

## 3. Single-Device Session Security Protocol

To ensure students cannot share accounts or manipulate food attendance on behalf of absentees:

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student (Device A)
    participant API as FastAPI Backend
    participant DB as MongoDB
    actor Imposter as Friend (Device B)

    Student->>API: POST /api/auth/login
    API->>DB: Mint new active_session_id (SID_1)
    API-->>Student: Return JWT containing sid: SID_1
    Student->>API: GET /api/student/today (with SID_1)
    API-->>Student: 200 OK (Allowed)

    Imposter->>API: POST /api/auth/login (Same credentials on Device B)
    API->>DB: Overwrite active_session_id to SID_2
    API-->>Imposter: Return JWT containing sid: SID_2

    Student->>API: GET /api/student/today (with SID_1)
    API->>DB: Check if SID_1 == active_session_id (SID_2)
    API-->>Student: 401 Unauthorized {"code": "session_invalidated"}
    Note over Student: Device A auto-clears tokens and redirects to Login
```

---

## 4. Key Database Collections

| Collection | Description | Primary Indexes |
| :--- | :--- | :--- |
| `users` | Student, Warden, and Admin accounts | `email` (unique), `hostel`, `active_session_id` |
| `daily_plans` | Daily meal participation flags (Breakfast, Lunch, Dinner, Snacks) | `user_id`, `date`, `hostel` |
| `menus` | Weekly cyclical meal items and serving timings | `hostel`, `day_of_week` |
| `wastage_logs` | Kitchen food cooked vs. left waste measurements | `hostel`, `date` |
| `notifications` | Push and in-app broadcast alerts | `hostel`, `created_at` |
| `subscriptions` | Mess subscription plans, dues, and Razorpay invoices | `hostel`, `status` |
