"""
Input validation utilities for user inputs.

This module provides functions for validating and sanitizing user inputs
to prevent security vulnerabilities and ensure data quality.
"""
import re
from html import escape
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format according to RFC 5321.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid: bool, error_message: Optional[str])
        - (True, None) if email is valid
        - (False, error_message) if email is invalid
    """
    if not email or len(email) > 254:  # RFC 5321 limit
        return False, "Email is required and must be less than 254 characters"
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength requirements.
    
    Requirements:
        - Minimum 12 characters
        - Maximum 128 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid: bool, error_message: Optional[str])
        - (True, None) if password meets requirements
        - (False, error_message) if password is invalid
    """
    if not password:
        return False, "Password is required"
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, None


def sanitize_input(text: Optional[str], max_length: int = 500) -> Optional[str]:
    """
    Sanitize text input to prevent XSS attacks.
    
    Performs HTML escaping and removes null bytes. Truncates if exceeds max_length.
    
    Args:
        text: Text to sanitize
        max_length: Maximum allowed length (default: 500)
        
    Returns:
        Sanitized text, or None if text exceeds max_length
    """
    if not text:
        return text
    if len(text) > max_length:
        return None
    # Remove potentially dangerous characters but allow normal text
    # Escape HTML to prevent XSS
    sanitized = escape(text.strip())
    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')
    return sanitized


def validate_text_input(text: Optional[str], field_name: str, min_length: int = 0, 
                       max_length: int = 500, required: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate text input with length and requirement constraints.
    
    Args:
        text: Text to validate
        field_name: Name of the field (for error messages)
        min_length: Minimum required length
        max_length: Maximum allowed length
        required: Whether the field is required
        
    Returns:
        Tuple of (is_valid: bool, error_message: Optional[str])
        - (True, None) if text is valid
        - (False, error_message) if text is invalid
    """
    if required and not text:
        return False, f"{field_name} is required"
    if text and len(text) > max_length:
        return False, f"{field_name} must be less than {max_length} characters"
    if text and len(text) < min_length:
        return False, f"{field_name} must be at least {min_length} characters"
    return True, None

