# Week 3 Testing Guide - Code Quality Improvements

**Date**: After Week 3 Implementation  
**Focus**: Logging, Input Validation, Error Handling, CSRF Protection

---

## Changes Implemented

### ✅ H2: Replaced Print Statements with Logging
- **Status**: COMPLETED
- **Changes**:
  1. Configured Python `logging` module with RotatingFileHandler
  2. Replaced all 91+ `print()` statements with appropriate log levels
  3. Log levels used: `DEBUG`, `INFO`, `WARNING`, `ERROR`
  4. Logging configured to write to `app.log` (10MB per file, 10 backups)
  5. Console logging also enabled for development

### ✅ H3: Added Input Validation
- **Status**: COMPLETED
- **Changes**:
  1. **Email Validation**: Regex pattern validation, length limits (max 254 chars)
  2. **Password Strength**: 
     - Minimum 12 characters (increased from 6)
     - Must contain: uppercase, lowercase, number, special character
     - Maximum 128 characters
  3. **Text Input Validation**: Length limits, required field checks
  4. **Input Sanitization**: HTML escaping to prevent XSS attacks
  5. Applied to: Registration, Login, Password Reset, Forgot Password

### ✅ M2: Standardized Error Handling
- **Status**: COMPLETED
- **Changes**:
  1. Added Flask error handlers for 400, 403, 404, 500 errors
  2. All errors logged with appropriate context
  3. User-friendly error messages returned
  4. Consistent error handling pattern throughout

### ✅ M3: Added CSRF Protection
- **Status**: COMPLETED
- **Changes**:
  1. Installed Flask-WTF
  2. CSRF protection enabled globally
  3. CSRF token time limit: 1 hour
  4. All forms now require CSRF tokens

---

## Testing Instructions

### 1. Test Logging

**Objective**: Verify logging is working and no print statements remain

**Steps**:
1. Start the application:
   ```bash
   python app.py
   ```

2. Perform various actions:
   - Register a new user
   - Login
   - Generate content
   - Access invalid routes

3. Check log file:
   ```bash
   tail -f app.log
   ```

4. Verify:
   - ✅ Log file `app.log` is created
   - ✅ Logs contain timestamps, log levels, and messages
   - ✅ No print statements appear in console (except Flask startup messages)
   - ✅ Errors are logged with stack traces (`exc_info=True`)

**Expected Result**: All actions are logged to `app.log` with appropriate log levels.

---

### 2. Test Input Validation - Registration

**Objective**: Verify registration form validates inputs correctly

**Test Cases**:

#### 2.1 Invalid Email Format
1. Go to `/register`
2. Enter invalid email: `notanemail`
3. Enter valid password: `TestPassword123!`
4. Fill other required fields
5. Submit form

**Expected**: Error message "Invalid email format"

#### 2.2 Weak Password
1. Go to `/register`
2. Enter valid email: `test@example.com`
3. Enter weak password: `short` (less than 12 chars)
4. Fill other required fields
5. Submit form

**Expected**: Error message "Password must be at least 12 characters long"

#### 2.3 Password Missing Requirements
1. Go to `/register`
2. Enter valid email: `test@example.com`
3. Enter password without uppercase: `testpassword123!`
4. Fill other required fields
5. Submit form

**Expected**: Error message "Password must contain at least one uppercase letter"

4. Test password without lowercase: `TESTPASSWORD123!`
   **Expected**: "Password must contain at least one lowercase letter"

5. Test password without number: `TestPassword!`
   **Expected**: "Password must contain at least one number"

6. Test password without special char: `TestPassword123`
   **Expected**: "Password must contain at least one special character"

#### 2.4 Missing Required Fields
1. Go to `/register`
2. Leave email empty
3. Submit form

**Expected**: Error message "Email is required and must be less than 254 characters"

#### 2.5 Valid Registration
1. Go to `/register`
2. Enter valid email: `test@example.com`
3. Enter strong password: `TestPassword123!`
4. Fill all required fields with valid data
5. Submit form

**Expected**: ✅ Registration successful, redirected to dashboard

---

### 3. Test Input Validation - Login

**Objective**: Verify login form validates inputs

**Test Cases**:

#### 3.1 Invalid Email Format
1. Go to `/login`
2. Enter invalid email: `notanemail`
3. Enter any password
4. Submit form

**Expected**: Error message "Invalid email format"

#### 3.2 Missing Credentials
1. Go to `/login`
2. Leave email or password empty
3. Submit form

**Expected**: Error message "Email and password are required"

#### 3.3 Valid Login
1. Go to `/login`
2. Enter valid credentials
3. Submit form

**Expected**: ✅ Login successful, redirected to dashboard

---

### 4. Test Input Validation - Password Reset

**Objective**: Verify password reset validates new password strength

**Test Cases**:

1. Go to `/forgot_password`
2. Enter valid email
3. Follow reset link (or use token from logs)
4. Enter weak password: `short`
5. Submit form

**Expected**: Error message about password requirements

6. Enter strong password: `NewPassword123!`
7. Submit form

**Expected**: ✅ Password reset successful

---

### 5. Test CSRF Protection

**Objective**: Verify CSRF tokens are required for POST requests

**Test Cases**:

#### 5.1 CSRF Token Present (Normal Flow)
1. Go to `/register` or `/login`
2. Fill out the form
3. Submit form

**Expected**: ✅ Form submits successfully (CSRF token included automatically by Flask-WTF)

#### 5.2 CSRF Token Missing
1. Open browser developer tools
2. Go to `/register`
3. Remove CSRF token from form (inspect element, delete hidden input)
4. Submit form

**Expected**: Error message "The CSRF token is missing" or similar

**Note**: This test may require disabling CSRF for specific routes or using a tool like Postman with CSRF disabled to properly test.

---

### 6. Test Error Handlers

**Objective**: Verify error handlers return user-friendly pages

**Test Cases**:

#### 6.1 404 Error
1. Navigate to invalid route: `http://localhost:8000/nonexistent`
2. Check response

**Expected**: 
- ✅ Custom error page shown (or Flask default if template missing)
- ✅ Error logged to `app.log` with warning level
- ✅ Status code 404

#### 6.2 500 Error (Simulate)
1. This would require causing an internal server error
2. Check logs

**Expected**: 
- ✅ Error logged with full stack trace
- ✅ User sees error page (if template exists)

---

### 7. Test Input Sanitization

**Objective**: Verify XSS protection in user inputs

**Test Cases**:

1. Go to `/register`
2. In "Firm name" field, enter: `<script>alert('XSS')</script>`
3. Fill other required fields
4. Submit form

**Expected**: 
- ✅ Script tags are escaped/removed
- ✅ No JavaScript execution in stored data
- ✅ Data stored safely in database

---

## Automated Testing

Run the existing test suite to ensure nothing broke:

```bash
pytest tests/ -v
```

**Expected**: All tests pass (some may need updates for new validation rules)

---

## Verification Checklist

- [ ] Logging works - `app.log` file created and populated
- [ ] No print statements in console output
- [ ] Email validation works - rejects invalid formats
- [ ] Password strength validation works - enforces 12+ chars, complexity
- [ ] Required field validation works
- [ ] Input sanitization works - XSS protection
- [ ] CSRF protection enabled (check forms have CSRF tokens)
- [ ] Error handlers work - 404, 500 errors handled gracefully
- [ ] Existing functionality still works - login, registration, content generation
- [ ] All tests pass

---

## Known Issues / Notes

1. **CSRF Testing**: Testing CSRF protection may require temporarily disabling it or using API testing tools
2. **Error Templates**: If `error.html` template doesn't exist, Flask will show default error pages. Consider creating error templates.
3. **Password Requirements**: Users with existing accounts may need to reset passwords to meet new requirements
4. **Log File Location**: Log file is created in the project root directory (`app.log`)

---

## Rollback Instructions

If issues are found:

1. **Disable CSRF** (if causing issues):
   - Comment out `csrf = CSRFProtect(app)` in `app.py`
   - Set `app.config['WTF_CSRF_ENABLED'] = False`

2. **Revert Password Requirements**:
   - Change `validate_password()` minimum length back to 6
   - Remove complexity requirements

3. **Disable Logging**:
   - Comment out logging configuration
   - Restore print statements if needed

---

## Next Steps

After Week 3 testing:
1. Review test results
2. Fix any issues found
3. Perform mini code audit
4. Move to Week 4 improvements

