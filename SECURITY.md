# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please report via one of these channels:

1. **GitHub Security Advisories** (Preferred):
   - Go to the [Security tab](https://github.com/abu-devel0per/messmate/security)
   - Click "Report a vulnerability"
   - Fill in the details privately

2. **Email**:
   - Send details to: security@messmate.app

### What to Include

Please provide as much information as possible:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Affected versions
- Suggested fix (if any)
- Your contact information

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 5 business days
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Within 60 days

We will keep you informed of progress throughout the process.

## Security Best Practices

### For Users

- Always use the latest stable release
- Keep your environment variables secure
- Rotate API keys and secrets regularly
- Enable 2FA on all accounts
- Monitor for security advisories

### For Contributors

- Never commit secrets, API keys, or credentials
- Use `.env.example` files for configuration templates
- Validate all user inputs (see `backend/security.py`)
- Use parameterized queries (MongoDB with Motor)
- Implement rate limiting on all endpoints
- Keep dependencies updated (`pip-audit`, `npm audit`)
- Follow OWASP Top 10 guidelines

### Secrets Management

All sensitive configuration must use environment variables:

```bash
# Backend (.env)
MONGO_URL=mongodb://...
JWT_SECRET=your-super-secret-key
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-adminsdk.json
RAZORPAY_KEY_ID=rzp_...
RAZORPAY_KEY_SECRET=...
GMAIL_CLIENT_ID=...
GMAIL_CLIENT_SECRET=...

# Frontend (.env)
EXPO_PUBLIC_BACKEND_URL=https://...
EXPO_PUBLIC_FIREBASE_API_KEY=...
```

Example files are provided:
- `backend/.env.example`
- `frontend/.env.example`
- `frontend/google-services.json.example`
- `backend/firebase-adminsdk.json.example`

### Dependency Security

We regularly audit dependencies:

```bash
# Python
pip-audit -r backend/requirements.txt

# Node.js
cd frontend && npm audit
```

Automated checks run in CI on every PR.

## Security Features

### Authentication & Authorization

- JWT-based authentication with HS256
- Single-device session enforcement
- bcrypt password hashing (cost factor 12)
- Rate limiting on auth endpoints
- Email verification required

### Data Protection

- MongoDB with Motor (async driver)
- No plaintext passwords stored
- Personal data encrypted at rest (MongoDB Atlas)
- TLS 1.2+ for all connections

### API Security

- CORS configured for known origins
- Helmet-style security headers
- Input validation with Pydantic
- Rate limiting per IP/user
- Request size limits

### Push Notifications (FCM)

- Service account with minimal permissions
- Token validation on each send
- No sensitive data in notification payloads

### Payments (Razorpay)

- Server-side payment verification
- Webhook signature validation
- No card data handled by our servers

## Vulnerability Disclosure

We believe in coordinated disclosure. Once a vulnerability is confirmed and fixed:

1. We will release a patch
2. Publish a Security Advisory on GitHub
3. Credit the reporter (if desired)
4. Update this document if needed

## Contact

For security-related questions or concerns:

- **Email**: security@messmate.app
- **GitHub Security**: https://github.com/abu-devel0per/messmate/security

Thank you for helping keep MessMate secure! 🔒