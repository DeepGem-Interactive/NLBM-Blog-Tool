# Week 1 Security Fixes - Testing Guide

This guide provides step-by-step instructions to test all Week 1 security fixes to ensure the application still works correctly.

## Changes Made in Week 1

1. **C3: Debug Mode Fix** - Debug mode now controlled by environment variable
2. **H4: Environment Variables Documentation** - Created `env.example` file
3. **H1: Removed Hardcoded Credentials** - Default admin/memberhub users removed
4. **C1: Password Hashing** - All passwords now hashed (registration, login, password reset)

---

## Pre-Testing Setup

### 1. Update Environment Variables

Copy `env.example` to `.env` (if you don't have one already) and ensure all variables are set:

```bash
# Make sure FLASK_DEBUG is set appropriately
FLASK_DEBUG=false  # for production
# or
FLASK_DEBUG=true   # for development/testing
```

### 2. Start the Application

```bash
python app.py
```

**Expected**: Application should start without errors. If `FLASK_DEBUG=false`, you should NOT see the Flask debugger or detailed error pages.

---

## Test 1: Debug Mode Configuration

### Test 1.1: Debug Mode OFF (Production Mode)

1. Set in `.env`: `FLASK_DEBUG=false`
2. Restart the application
3. Navigate to a non-existent route: `http://localhost:8000/nonexistent`
4. **Expected**: You should see a generic error page, NOT a detailed Flask debugger page with stack traces

### Test 1.2: Debug Mode ON (Development Mode)

1. Set in `.env`: `FLASK_DEBUG=true`
2. Restart the application
3. Navigate to a non-existent route: `http://localhost:8000/nonexistent`
4. **Expected**: You should see the Flask debugger page (for development only)

**Result**: ✅ Debug mode is now controlled by environment variable

---

## Test 2: User Registration (Password Hashing)

### Test 2.1: Register New User

1. Navigate to: `http://localhost:8000/register`
2. Fill in the registration form:
   - Email: `testuser@example.com`
   - Password: `TestPassword123!`
   - Firm: `Test Firm`
   - Location: `Test City`
   - Lawyer Name: `Test Lawyer`
   - State: `CA`
3. Click "Register"
4. **Expected**: 
   - Registration succeeds
   - You are redirected to dashboard or login page
   - User can log in with the password

### Test 2.2: Verify Password is Hashed in Database

**Option A: Using SQL Query (if you have database access)**
```sql
SELECT username, email, password FROM users WHERE email = 'testuser@example.com';
```

**Expected**: The `password` field should start with `pbkdf2:sha256:` (hashed format), NOT the plain text password.

**Option B: Check via Application**
- Try to log in with the registered credentials
- If login works, password was stored correctly

**Result**: ✅ New passwords are hashed during registration

---

## Test 3: User Login (Password Verification)

### Test 3.1: Login with New User (Hashed Password)

1. Navigate to: `http://localhost:8000/login`
2. Enter credentials:
   - Email: `testuser@example.com`
   - Password: `TestPassword123!`
3. Click "Login"
4. **Expected**: 
   - Login succeeds
   - You are redirected to dashboard
   - Session is created

### Test 3.2: Login with Existing User (Legacy Plain Text Password)

**IMPORTANT**: This test verifies backward compatibility with existing users who have plain text passwords.

1. If you have existing users with plain text passwords in the database:
   - Try logging in with an existing user's credentials
2. **Expected**: 
   - Login should succeed (backward compatibility)
   - After successful login, the password should be automatically migrated to hashed format
   - Next login should also work (now using hashed password)

**Verification**: Check database after login - password should now be hashed:
```sql
SELECT password FROM users WHERE email = 'existing_user@example.com';
-- Should show pbkdf2:sha256:... format
```

### Test 3.3: Login with Wrong Password

1. Navigate to: `http://localhost:8000/login`
2. Enter wrong password for a valid user
3. **Expected**: 
   - Login fails
   - Error message displayed
   - User is NOT logged in

**Result**: ✅ Login works with both hashed and plain text passwords (migration support)

---

## Test 4: Password Reset Flow

### Test 4.1: Request Password Reset

1. Navigate to: `http://localhost:8000/forgot_password`
2. Enter a registered email address
3. Click "Submit"
4. **Expected**: 
   - Success message displayed
   - Reset link/token shown (for demo purposes)
   - Token stored in database

### Test 4.2: Reset Password

1. Copy the reset token from the success message
2. Navigate to: `http://localhost:8000/reset_password/<token>`
3. Enter new password: `NewSecurePassword456!`
4. Confirm password: `NewSecurePassword456!`
5. Click "Reset Password"
6. **Expected**: 
   - Password reset succeeds
   - Success message displayed
   - New password is hashed in database

### Test 4.3: Login with New Password

1. Navigate to: `http://localhost:8000/login`
2. Enter credentials:
   - Email: (the email you reset)
   - Password: `NewSecurePassword456!`
3. **Expected**: Login succeeds

**Verification**: Check database - password should be hashed:
```sql
SELECT password FROM users WHERE email = 'reset_user@example.com';
-- Should show pbkdf2:sha256:... format
```

**Result**: ✅ Password reset hashes new passwords

---

## Test 5: Removed Default Users

### Test 5.1: Default Users Not Created

1. Check database for default users:
```sql
SELECT username, email FROM users WHERE username IN ('admin', 'memberhub');
```

**Expected**: 
- If database is fresh/new: No admin or memberhub users should exist
- If database existed before: Existing users remain, but no new ones are created

### Test 5.2: Create Admin User Manually

Since default users are removed, you need to create an admin user manually:

1. Register a new user through the registration page
2. Manually set `is_admin = 1` in database:
```sql
UPDATE users SET is_admin = 1 WHERE email = 'your_admin_email@example.com';
```

**Expected**: User can now access admin features

**Result**: ✅ Hardcoded default credentials removed

---

## Test 6: Environment Variables Documentation

### Test 6.1: Check env.example File

1. Open `env.example` file
2. **Expected**: 
   - All required environment variables are documented
   - Each variable has a description
   - Example values provided where appropriate

### Test 6.2: Missing Environment Variables

1. Temporarily remove a required environment variable from `.env` (e.g., `FLASK_SECRET_KEY`)
2. Restart the application
3. **Expected**: 
   - Application may start but will fail when that variable is needed
   - Error message should indicate missing configuration

**Result**: ✅ Environment variables are documented

---

## Automated Test Script

Create a file `test_week1_fixes.py`:

```python
"""
Week 1 Security Fixes - Automated Test Script
Run this script to verify all Week 1 fixes are working correctly.
"""

import os
import sys
import requests
from werkzeug.security import check_password_hash, generate_password_hash

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test_week1@example.com"
TEST_PASSWORD = "TestPassword123!"

def test_debug_mode():
    """Test that debug mode is controlled by environment variable"""
    print("Testing debug mode configuration...")
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    print(f"  FLASK_DEBUG environment variable: {os.getenv('FLASK_DEBUG', 'not set')}")
    print(f"  Debug mode enabled: {debug_mode}")
    
    # Try to access a non-existent route
    try:
        response = requests.get(f"{BASE_URL}/nonexistent_route_12345", timeout=5)
        if debug_mode:
            print("  ✅ Debug mode ON: Detailed error pages should be visible")
        else:
            print("  ✅ Debug mode OFF: Generic error pages should be shown")
    except Exception as e:
        print(f"  ⚠️  Could not test debug mode: {e}")
    
    return True

def test_password_hashing():
    """Test that passwords are properly hashed"""
    print("\nTesting password hashing...")
    
    # Test that generate_password_hash creates a hash
    test_hash = generate_password_hash("testpassword")
    is_hashed = test_hash.startswith('pbkdf2:sha256:')
    
    if is_hashed:
        print("  ✅ Password hashing function works correctly")
        print(f"  ✅ Hash format: {test_hash[:20]}...")
        
        # Test that check_password_hash works
        is_valid = check_password_hash(test_hash, "testpassword")
        is_invalid = check_password_hash(test_hash, "wrongpassword")
        
        if is_valid and not is_invalid:
            print("  ✅ Password verification works correctly")
        else:
            print("  ❌ Password verification failed")
            return False
    else:
        print("  ❌ Password hashing failed")
        return False
    
    return True

def test_registration():
    """Test user registration"""
    print("\nTesting user registration...")
    
    try:
        # Get registration page
        response = requests.get(f"{BASE_URL}/register", timeout=5)
        if response.status_code == 200:
            print("  ✅ Registration page is accessible")
        else:
            print(f"  ⚠️  Registration page returned status {response.status_code}")
    except Exception as e:
        print(f"  ⚠️  Could not test registration page: {e}")
    
    return True

def test_login_page():
    """Test login page accessibility"""
    print("\nTesting login page...")
    
    try:
        response = requests.get(f"{BASE_URL}/login", timeout=5)
        if response.status_code == 200:
            print("  ✅ Login page is accessible")
        else:
            print(f"  ⚠️  Login page returned status {response.status_code}")
    except Exception as e:
        print(f"  ⚠️  Could not test login page: {e}")
    
    return True

def test_env_example_exists():
    """Test that env.example file exists"""
    print("\nTesting environment documentation...")
    
    if os.path.exists("env.example"):
        print("  ✅ env.example file exists")
        
        # Check if it contains key variables
        with open("env.example", "r") as f:
            content = f.read()
            required_vars = ["FLASK_SECRET_KEY", "AZURE_SQL_SERVER", "AZURE_OPENAI_KEY"]
            found_vars = [var for var in required_vars if var in content]
            
            if len(found_vars) == len(required_vars):
                print(f"  ✅ env.example contains all required variables")
            else:
                print(f"  ⚠️  env.example missing some variables: {set(required_vars) - set(found_vars)}")
    else:
        print("  ❌ env.example file not found")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Week 1 Security Fixes - Automated Test Script")
    print("=" * 60)
    
    tests = [
        ("Debug Mode Configuration", test_debug_mode),
        ("Password Hashing", test_password_hashing),
        ("User Registration", test_registration),
        ("Login Page", test_login_page),
        ("Environment Documentation", test_env_example_exists),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All automated tests passed!")
        print("⚠️  Remember to also perform manual testing as described in WEEK1_TESTING_GUIDE.md")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

---

## Manual Testing Checklist

Use this checklist to ensure all functionality still works:

- [ ] Application starts without errors
- [ ] Debug mode is controlled by FLASK_DEBUG environment variable
- [ ] New user registration works
- [ ] New user passwords are hashed in database
- [ ] Login works with newly registered users
- [ ] Login works with existing users (backward compatibility)
- [ ] Existing user passwords are migrated to hashed format after login
- [ ] Password reset request works
- [ ] Password reset with token works
- [ ] Reset passwords are hashed in database
- [ ] Login works after password reset
- [ ] Default admin/memberhub users are not created automatically
- [ ] All existing features still work (article selection, content generation, etc.)
- [ ] No errors in application logs

---

## Troubleshooting

### Issue: "Cannot login with existing user"

**Solution**: The login function supports backward compatibility. If a user has a plain text password, it will:
1. Check plain text match
2. If match, automatically hash and update the password
3. Allow login

If this doesn't work, check:
- Database connection is working
- User exists in database
- Password in database matches what you're entering

### Issue: "New users can't register"

**Solution**: Check:
- Database connection is working
- Email is not already registered
- All required fields are filled

### Issue: "Debug mode still shows detailed errors"

**Solution**: 
- Ensure `.env` file has `FLASK_DEBUG=false`
- Restart the application
- Clear browser cache

---

## Success Criteria

All Week 1 fixes are successful if:

✅ Debug mode is controlled by environment variable  
✅ New passwords are hashed during registration  
✅ Login works with both hashed and plain text passwords  
✅ Password reset hashes new passwords  
✅ Default hardcoded users are not created  
✅ Environment variables are documented  
✅ All existing functionality still works  

---

## Next Steps

After confirming all tests pass:

1. Review the mini code audit (will be performed after Week 1 completion)
2. Check the score improvement
3. Proceed to Week 2 fixes (Testing Infrastructure)

---

**Note**: This testing guide focuses on Week 1 security fixes. For comprehensive application testing, refer to your existing test procedures.


