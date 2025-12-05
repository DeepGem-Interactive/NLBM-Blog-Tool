# Week 2 Testing Infrastructure - Testing Guide

This guide explains how to run and verify the test suite that was set up in Week 2.

## What Was Added in Week 2

1. **Pytest Framework Setup** - Complete testing infrastructure
2. **Unit Tests** - Tests for authentication, UserSession, UserActivityTracker
3. **Integration Tests** - Placeholder tests for complete flows
4. **CI/CD Integration** - GitHub Actions workflow for automated testing
5. **Code Coverage** - Coverage reporting with 70% target

---

## Prerequisites

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- pytest
- pytest-cov
- pytest-flask
- pytest-asyncio
- pytest-mock
- coverage

---

## Running Tests

### 1. Run All Tests

```bash
pytest
```

**Expected Output**:
```
======================== test session starts ========================
platform win32 -- Python 3.x.x, pytest-7.x.x
collected 25 items

tests/test_auth.py .................                    [ 68%]
tests/test_user_activity.py ....                        [ 84%]
tests/test_user_session.py .....                        [100%]

======================= 25 passed in 2.34s ========================
```

### 2. Run Tests with Coverage

```bash
pytest --cov=app --cov=function_app --cov-report=html --cov-report=term
```

**Expected Output**:
```
---------- coverage: platform win32, python 3.x.x -----------
Name           Stmts   Miss  Cover
----------------------------------
app.py           500    200    60%
----------------------------------
TOTAL           500    200    60%
```

Coverage report will be generated in `htmlcov/index.html` - open it in a browser to see detailed coverage.

### 3. Run Specific Test File

```bash
# Run only authentication tests
pytest tests/test_auth.py

# Run only user session tests
pytest tests/test_user_session.py

# Run only activity tracker tests
pytest tests/test_user_activity.py
```

### 4. Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only authentication tests
pytest -m auth
```

### 5. Run Tests Verbosely

```bash
pytest -v
```

Shows detailed output for each test.

### 6. Run Tests with Output

```bash
pytest -s
```

Shows print statements and other output.

---

## Test Coverage

### Current Coverage Target

**Target**: 70% coverage on critical paths (authentication, user management)

### View Coverage Report

1. Run tests with coverage:
   ```bash
   pytest --cov=app --cov-report=html
   ```

2. Open `htmlcov/index.html` in your browser

3. Review coverage by:
   - File (see which files need more tests)
   - Line (see which lines are not covered)
   - Function (see which functions need tests)

### Coverage by Category

- **Authentication**: Should have 80%+ coverage (critical security)
- **User Management**: Should have 70%+ coverage
- **Activity Tracking**: Should have 70%+ coverage
- **Content Generation**: Lower priority, can be 50%+

---

## Test Structure

### Unit Tests

Located in:
- `tests/test_auth.py` - Authentication tests
- `tests/test_user_session.py` - UserSession class tests
- `tests/test_user_activity.py` - UserActivityTracker tests

**Characteristics**:
- Fast execution (< 1 second total)
- Use mocks (no real database required)
- Test individual functions/classes
- Isolated (no dependencies between tests)

### Integration Tests

Located in:
- `tests/test_integration_auth.py` - Authentication flow tests

**Characteristics**:
- May require test database (currently skipped)
- Test complete workflows
- May require external service mocking

---

## What Each Test File Tests

### test_auth.py

- ✅ Password hashing functions
- ✅ User registration (password hashing)
- ✅ User login (hashed and plain text passwords)
- ✅ Password migration (legacy users)
- ✅ Wrong password rejection
- ✅ Blocked user handling
- ✅ Non-existent user handling

### test_user_session.py

- ✅ Profile updates
- ✅ Session management
- ✅ Custom tone management
- ✅ User blocking checks

### test_user_activity.py

- ✅ Activity logging (success and failure)
- ✅ Activity summary queries
- ✅ Feature usage statistics
- ✅ Error handling

---

## CI/CD Integration

### GitHub Actions Workflow

The workflow (`.github/workflows/tests.yml`) runs tests automatically on:
- Push to main/develop/master branches
- Pull requests

### What the CI Does

1. Sets up Python environment (3.9, 3.10, 3.11)
2. Installs dependencies
3. Runs all tests with coverage
4. Uploads coverage reports
5. Uploads coverage artifacts

### Viewing CI Results

1. Go to your GitHub repository
2. Click "Actions" tab
3. Click on the latest workflow run
4. See test results and coverage

---

## Verifying Tests Work

### Quick Verification

```bash
# Run a simple test
pytest tests/test_auth.py::TestPasswordHashing::test_generate_password_hash_creates_hash -v
```

**Expected**: Test should pass ✅

### Full Test Run

```bash
pytest -v
```

**Expected**: All tests should pass (some integration tests may be skipped)

### Coverage Check

```bash
pytest --cov=app --cov-report=term --cov-fail-under=50
```

**Expected**: Coverage should be at least 50% (target is 70% for critical paths)

---

## Adding New Tests

### Example: Adding a Test for New Feature

1. Create test file or add to existing file:
   ```python
   # tests/test_new_feature.py
   import pytest
   from app import NewFeature
   
   class TestNewFeature:
       def test_new_feature_works(self):
           result = NewFeature.doSomething()
           assert result is True
   ```

2. Run the test:
   ```bash
   pytest tests/test_new_feature.py -v
   ```

3. Add to CI/CD (already configured to run all tests)

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution**: Make sure you're running tests from the project root directory:
```bash
cd /path/to/project
pytest
```

### Issue: "Database connection errors"

**Solution**: Unit tests use mocks and don't require a real database. If you see database errors, the mocks may not be set up correctly. Check that `@patch('app.get_db')` is used.

### Issue: "Tests are slow"

**Solution**: 
- Make sure you're running unit tests (not integration tests)
- Integration tests are skipped by default
- Use `pytest -m unit` to run only fast unit tests

### Issue: "Coverage is low"

**Solution**:
- Add more tests for uncovered code
- Focus on critical paths first (authentication, user management)
- Use coverage report to identify gaps

### Issue: "CI/CD tests failing"

**Solution**:
- Check GitHub Actions logs
- Ensure all dependencies are in `requirements.txt`
- Check that environment variables are set in CI workflow

---

## Success Criteria

Week 2 is successful if:

✅ Pytest framework is set up and working  
✅ Unit tests exist for authentication (20+ tests)  
✅ Unit tests exist for UserSession and UserActivityTracker  
✅ Tests can be run with `pytest` command  
✅ Coverage reporting works  
✅ CI/CD workflow runs tests automatically  
✅ Coverage is at least 50% on critical paths (target: 70%)  

---

## Next Steps

After verifying tests work:

1. Review test coverage report
2. Add more tests for uncovered code
3. Increase coverage to 70%+ on critical paths
4. Proceed to Week 3 (Code Quality improvements)

---

## Test Statistics

After running tests, you should see:

- **Total Tests**: 20-30+ unit tests
- **Test Execution Time**: < 5 seconds
- **Coverage**: 50-70% (depending on what's tested)
- **Pass Rate**: 100% (all tests should pass)

---

**Note**: Integration tests are currently placeholders and will be fully implemented when test database setup is available.


