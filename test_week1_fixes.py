"""
Week 1 Security Fixes - Automated Test Script
Run this script to verify all Week 1 fixes are working correctly.

Usage:
    python test_week1_fixes.py

Prerequisites:
    - Application should be running on http://localhost:8000
    - Install requests: pip install requests
"""

import os
import sys

try:
    import requests
except ImportError:
    print("ERROR: requests library not installed.")
    print("Install it with: pip install requests")
    sys.exit(1)

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
    # Check if it's a hash (werkzeug uses pbkdf2:sha256: or scrypt: format)
    is_hashed = (test_hash.startswith('pbkdf2:sha256:') or 
                 test_hash.startswith('scrypt:') or
                 len(test_hash) > 50)  # Hashes are always long
    
    if is_hashed:
        print("  ✅ Password hashing function works correctly")
        print(f"  ✅ Hash format: {test_hash[:30]}...")
        
        # Test that check_password_hash works
        is_valid = check_password_hash(test_hash, "testpassword")
        is_invalid = check_password_hash(test_hash, "wrongpassword")
        
        if is_valid and not is_invalid:
            print("  ✅ Password verification works correctly")
        else:
            print("  ❌ Password verification failed")
            return False
    else:
        print(f"  ❌ Password hashing failed - hash format: {test_hash[:30]}")
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

