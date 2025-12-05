# Test Suite Documentation

This directory contains the test suite for the NLBM Blog Drafting Tool.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                # Pytest fixtures and configuration
├── test_auth.py               # Authentication unit tests
├── test_user_session.py       # UserSession class tests
├── test_user_activity.py      # UserActivityTracker class tests
├── test_integration_auth.py  # Authentication integration tests
└── README.md                  # This file
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov=function_app --cov-report=html
```

### Run Only Unit Tests

```bash
pytest -m unit
```

### Run Only Integration Tests

```bash
pytest -m integration
```

### Run Tests Verbosely

```bash
pytest -v
```

### Run Tests with Output

```bash
pytest -s
```

## Test Coverage

The test suite aims for **70% code coverage** on critical paths, including:

- Authentication flows (login, register, password reset)
- User management (profile updates, custom tones)
- Activity tracking
- Password hashing and security

### View Coverage Report

After running tests with coverage, open `htmlcov/index.html` in a browser to view the detailed coverage report.

## Test Categories

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Fast, isolated unit tests
- `@pytest.mark.integration` - Integration tests (may require database/external services)
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.auth` - Authentication-related tests
- `@pytest.mark.content` - Content generation tests
- `@pytest.mark.admin` - Admin functionality tests

## Writing New Tests

### Unit Test Example

```python
import pytest
from unittest.mock import patch, MagicMock
from app import UserSession

class TestUserRegistration:
    @patch('app.get_db')
    def test_register_hashes_password(self, mock_get_db):
        """Test that registration hashes the password"""
        # Setup mocks
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Test
        result = UserSession.register(
            email="test@example.com",
            password="Password123!",
            firm="Test Firm",
            location="Test City",
            lawyer_name="Test Lawyer",
            state="CA"
        )
        
        # Assert
        assert result is True
```

### Integration Test Example

```python
@pytest.mark.integration
class TestAuthenticationFlow:
    def test_register_then_login(self, client):
        """Test complete register -> login flow"""
        # Test implementation
        pass
```

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `app` - Flask application instance
- `client` - Test client for making requests
- `runner` - CLI test runner
- `mock_db` - Mock database connection
- `mock_user` - Mock user object
- `sample_session_data` - Sample session data

## CI/CD Integration

Tests run automatically on:
- Push to main/develop/master branches
- Pull requests

See `.github/workflows/tests.yml` for CI/CD configuration.

## Requirements

Install test dependencies:

```bash
pip install -r requirements.txt
```

Test dependencies include:
- pytest
- pytest-cov
- pytest-flask
- pytest-asyncio
- pytest-mock
- coverage

## Notes

- Unit tests use mocks to avoid requiring a real database
- Integration tests may require test database setup (currently skipped)
- Some tests are skipped if they require external services (Azure Functions)
- All tests should be fast and isolated when possible

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running tests from the project root:

```bash
cd /path/to/project
pytest
```

### Database Connection Errors

Unit tests use mocks and don't require a real database. If you see database errors, check that mocks are properly set up.

### Coverage Not Showing

Make sure you're running with coverage flags:

```bash
pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in a browser.


