"""
Unit tests for validation utilities
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validation import validate_email, validate_password, validate_text_input, sanitize_input


class TestEmailValidation:
    """Test email validation function"""
    
    def test_valid_email_passes(self):
        """Test that valid email addresses pass validation"""
        assert validate_email("test@example.com")[0] is True
        assert validate_email("user.name@example.co.uk")[0] is True
        assert validate_email("user+tag@example.com")[0] is True
    
    def test_invalid_email_fails(self):
        """Test that invalid email addresses fail validation"""
        assert validate_email("notanemail")[0] is False
        assert validate_email("missing@domain")[0] is False
        assert validate_email("@example.com")[0] is False
        assert validate_email("user@")[0] is False
    
    def test_empty_email_fails(self):
        """Test that empty email fails validation"""
        assert validate_email("")[0] is False
        assert validate_email(None)[0] is False
    
    def test_long_email_fails(self):
        """Test that emails exceeding 254 characters fail"""
        long_email = "a" * 250 + "@example.com"
        assert validate_email(long_email)[0] is False


class TestPasswordValidation:
    """Test password validation function"""
    
    def test_strong_password_passes(self):
        """Test that strong passwords pass validation"""
        assert validate_password("TestPassword123!")[0] is True
        assert validate_password("MySecureP@ssw0rd")[0] is True
    
    def test_short_password_fails(self):
        """Test that passwords shorter than 12 characters fail"""
        assert validate_password("Short1!")[0] is False
        assert validate_password("")[0] is False
    
    def test_password_missing_uppercase_fails(self):
        """Test that passwords without uppercase fail"""
        assert validate_password("testpassword123!")[0] is False
    
    def test_password_missing_lowercase_fails(self):
        """Test that passwords without lowercase fail"""
        assert validate_password("TESTPASSWORD123!")[0] is False
    
    def test_password_missing_number_fails(self):
        """Test that passwords without numbers fail"""
        assert validate_password("TestPassword!")[0] is False
    
    def test_password_missing_special_char_fails(self):
        """Test that passwords without special characters fail"""
        assert validate_password("TestPassword123")[0] is False
    
    def test_long_password_fails(self):
        """Test that passwords exceeding 128 characters fail"""
        long_password = "A" * 129 + "a1!"
        assert validate_password(long_password)[0] is False


class TestTextInputValidation:
    """Test text input validation function"""
    
    def test_valid_text_passes(self):
        """Test that valid text passes validation"""
        assert validate_text_input("Valid text", "Field", min_length=1, max_length=100)[0] is True
    
    def test_required_field_empty_fails(self):
        """Test that required empty fields fail"""
        assert validate_text_input("", "Field", required=True)[0] is False
        assert validate_text_input(None, "Field", required=True)[0] is False
    
    def test_text_exceeding_max_length_fails(self):
        """Test that text exceeding max length fails"""
        long_text = "a" * 501
        assert validate_text_input(long_text, "Field", max_length=500)[0] is False
    
    def test_text_below_min_length_fails(self):
        """Test that text below min length fails"""
        assert validate_text_input("ab", "Field", min_length=5)[0] is False


class TestInputSanitization:
    """Test input sanitization function"""
    
    def test_sanitize_removes_html(self):
        """Test that HTML is escaped"""
        result = sanitize_input("<script>alert('XSS')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result
    
    def test_sanitize_removes_null_bytes(self):
        """Test that null bytes are removed"""
        result = sanitize_input("text\x00with\x00nulls")
        assert "\x00" not in result
    
    def test_sanitize_truncates_long_text(self):
        """Test that text exceeding max_length returns None"""
        long_text = "a" * 501
        assert sanitize_input(long_text, max_length=500) is None
    
    def test_sanitize_handles_empty_string(self):
        """Test that empty strings are handled"""
        assert sanitize_input("") == ""
        assert sanitize_input(None) is None

