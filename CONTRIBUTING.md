# Contributing to MessMate

Thank you for your interest in contributing to MessMate! We welcome contributions from the community. This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Security](#security)
- [License](#license)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## Getting Started

### Prerequisites

- **Node.js**: v18.x or v20.x
- **Python**: v3.11, v3.12, or v3.14
- **MongoDB**: Local or Atlas instance
- **Git**: Latest version

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/messmate.git
   cd messmate
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/abu-devel0per/messmate.git
   ```
4. **Set up backend**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your configuration
   pip install -r requirements.txt
   ```
5. **Set up frontend**:
   ```bash
   cd ../frontend
   cp .env.example .env
   # Edit .env with your configuration
   npm install
   ```
6. **Configure Firebase** (for push notifications):
   - Create a Firebase project
   - Download `google-services.json` to `frontend/`
   - Download service account key to `backend/firebase-adminsdk.json`
   - See [Firebase Setup Guide](docs/firebase-setup.md)

## Development Workflow

### Branching Strategy

- `main` - Stable, production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates
- `refactor/*` - Code refactoring

### Making Changes

1. **Create a branch** from `develop`:
   ```bash
   git checkout develop
   git pull upstream develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our [coding standards](#coding-standards)

3. **Write tests** for new functionality

4. **Run the test suite**:
   ```bash
   # Backend tests
   cd backend
   pytest tests/ -v

   # Frontend tests (if available)
   cd ../frontend
   npm test
   ```

5. **Run linters**:
   ```bash
   # Backend
   cd backend
   black .
   isort .
   flake8 .

   # Frontend
   cd ../frontend
   npm run lint
   ```

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

Example:
```
feat: add student meal RSVP cutoff notifications

Adds push notification support for meal cutoff reminders
using Firebase Cloud Messaging.

Closes #123
```

## Pull Request Process

1. **Update your branch** with latest `develop`:
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** against `develop` branch

4. **PR Requirements**:
   - Clear title following conventional commits
   - Description explaining the change
   - Reference related issues
   - All CI checks passing
   - At least one approval from maintainers
   - No merge conflicts

5. **Review Process**:
   - Maintainers will review within 3 business days
   - Address feedback promptly
   - CI must pass before merge

## Coding Standards

### Backend (Python/FastAPI)

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Type hints required for all functions
- Maximum line length: 88 characters (Black default)
- Docstrings for public functions (Google style)

```python
async def calculate_cooking_quantities(
    headcount: int,
    buffer_percentage: float = 0.1
) -> CookingQuantities:
    """Calculate required ingredient quantities for a meal.

    Args:
        headcount: Number of expected diners
        buffer_percentage: Safety margin (default 10%)

    Returns:
        CookingQuantities with ingredient weights in kg

    Raises:
        ValueError: If headcount is negative
    """
    if headcount < 0:
        raise ValueError("Headcount cannot be negative")
    ...
```

### Frontend (TypeScript/React Native)

- Follow [TypeScript ESLint](https://typescript-eslint.io/) rules
- Use [Prettier](https://prettier.io/) for formatting
- Functional components with hooks
- Proper TypeScript types (avoid `any`)
- Maximum line length: 100 characters
- JSDoc for exported functions/components

```typescript
interface MealRSVPProps {
  mealType: MealType;
  cutoffTime: Date;
  onToggle: (mealType: MealType, optedIn: boolean) => void;
}

/**
 * Meal RSVP toggle component with live countdown.
 */
export const MealRSVP: React.FC<MealRSVPProps> = ({
  mealType,
  cutoffTime,
  onToggle,
}) => {
  ...
};
```

### Git Hygiene

- Keep commits atomic and focused
- Write meaningful commit messages
- Rebase instead of merge for feature branches
- Squash fixup commits before PR

## Testing

### Backend Testing

- Unit tests with `pytest`
- Integration tests for API endpoints
- Mock external services (Firebase, Razorpay, MongoDB)
- Target: >80% code coverage

```bash
cd backend
pytest tests/ -v --cov=. --cov-report=html
```

### Frontend Testing

- Unit tests with Jest/React Native Testing Library
- E2E tests with Detox (if configured)
- Component snapshot tests

```bash
cd frontend
npm test
```

### Test Guidelines

- Test happy paths and edge cases
- Mock external dependencies
- Use descriptive test names
- Keep tests independent and isolated

## Security

### Reporting Vulnerabilities

**DO NOT** open public issues for security vulnerabilities. Instead, email security@messmate.app or use GitHub's [private vulnerability reporting](https://github.com/abu-devel0per/messmate/security/advisories/new).

### Security Best Practices

- Never commit secrets, API keys, or credentials
- Use environment variables for configuration
- Validate all user inputs
- Use parameterized queries (no SQL injection)
- Implement rate limiting
- Keep dependencies updated

### Secret Scanning

We use automated secret scanning. If you accidentally commit a secret:
1. Rotate the secret immediately
2. Contact maintainers to purge from history
3. Do not just delete the file - it remains in history

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

## Questions?

- Open a [Discussion](https://github.com/abu-devel0per/messmate/discussions)
- Check existing [Issues](https://github.com/abu-devel0per/messmate/issues)
- Review [Documentation](docs/)

Thank you for contributing to MessMate! 🍽️