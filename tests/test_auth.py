"""
Unit tests for authentication functionality
"""
import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from unittest.mock import Mock, patch, MagicMock, PropertyMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import UserSession


class TestPasswordHashing:
    """Test password hashing functions"""
    
    def test_generate_password_hash_creates_hash(self):
        """Test that generate_password_hash creates a proper hash"""
        password = "TestPassword123!"
        hashed = generate_password_hash(password)
        
        assert hashed is not None
        assert len(hashed) > 50  # Hashes are always long
        assert hashed != password  # Hash should be different from plain text
        # Should start with pbkdf2:sha256: or scrypt:
        assert (hashed.startswith('pbkdf2:sha256:') or 
                hashed.startswith('scrypt:'))
    
    def test_check_password_hash_verifies_correct_password(self):
        """Test that check_password_hash verifies correct passwords"""
        password = "TestPassword123!"
        hashed = generate_password_hash(password)
        
        assert check_password_hash(hashed, password) is True
    
    def test_check_password_hash_rejects_wrong_password(self):
        """Test that check_password_hash rejects wrong passwords"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = generate_password_hash(password)
        
        assert check_password_hash(hashed, wrong_password) is False
    
    def test_password_hash_is_deterministic(self):
        """Test that same password produces different hashes (security feature)"""
        password = "TestPassword123!"
        hash1 = generate_password_hash(password)
        hash2 = generate_password_hash(password)
        
        # Hashes should be different (due to salt)
        assert hash1 != hash2
        # But both should verify the same password
        assert check_password_hash(hash1, password) is True
        assert check_password_hash(hash2, password) is True


class TestUserRegistration:
    """Test user registration functionality"""
    
    @patch('app.get_db')
    def test_register_hashes_password(self, mock_get_db):
        """Test that registration hashes the password before storing"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Register user
        result = UserSession.register(
            email="newuser@example.com",
            password="PlainTextPassword123!",
            firm="Test Firm",
            location="Test City",
            lawyer_name="Test Lawyer",
            state="CA"
        )
        
        # Check that password was hashed
        call_args = mock_cursor.execute.call_args
        assert call_args is not None
        
        # Get the password argument (3rd positional arg, index 2)
        executed_sql = call_args[0][0]
        password_arg = call_args[0][1][2]  # password is 3rd parameter
        
        # Password should be hashed
        assert password_arg.startswith('pbkdf2:sha256:') or password_arg.startswith('scrypt:')
        assert password_arg != "PlainTextPassword123!"
        
        # Registration should succeed (now returns tuple)
        assert result[0] is True  # success
        assert result[1] is None  # no error
        mock_db.commit.assert_called_once()
    
    @patch('app.get_db')
    def test_register_creates_username_from_email(self, mock_get_db):
        """Test that username is created from email"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        UserSession.register(
            email="testuser@example.com",
            password="Password123!",
            firm="Test Firm",
            location="Test City",
            lawyer_name="Test Lawyer",
            state="CA"
        )
        
        # Check username was created from email
        call_args = mock_cursor.execute.call_args
        username_arg = call_args[0][1][0]  # username is 1st parameter
        
        assert username_arg == "testuser"  # Lowercase, before @
    
    @patch('app.get_db')
    def test_register_handles_duplicate_email(self, mock_get_db):
        """Test that registration handles duplicate emails gracefully"""
        import pyodbc
        
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = pyodbc.IntegrityError("Duplicate key")
        mock_get_db.return_value = mock_db
        
        result = UserSession.register(
            email="existing@example.com",
            password="Password123!",
            firm="Test Firm",
            location="Test City",
            lawyer_name="Test Lawyer",
            state="CA"
        )
        
        # Should return False for duplicate (now returns tuple)
        assert result[0] is False  # success = False
        assert "already registered" in result[1].lower()  # error message


class TestUserLogin:
    """Test user login functionality"""
    
    @patch('app.get_db')
    @patch('app.UserActivityTracker.log_activity')
    def test_login_with_hashed_password(self, mock_log_activity, mock_get_db, app):
        """Test login with hashed password (new users)"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Create mock user with hashed password - use a simple class to ensure attributes work
        hashed_pwd = generate_password_hash("CorrectPassword123!")
        
        # Verify the hash format (werkzeug can use pbkdf2:sha256: or scrypt:)
        assert hashed_pwd.startswith('pbkdf2:sha256:') or hashed_pwd.startswith('scrypt:'), \
            f"Unexpected hash format: {hashed_pwd[:50]}"
        
        class MockUser:
            def __init__(self):
                self.id = 1
                self.username = 'testuser'
                self.email = 'test@example.com'
                self.password = hashed_pwd
                self.firm = 'Test Firm'
                self.location = 'Test City'
                self.lawyer_name = 'Test Lawyer'
                self.state = 'CA'
                self.address = ''
                self.planning_session = ''
                self.other_planning_session = ''
                self.discovery_call_link = ''
                self.is_admin = False
                self.is_blocked = False
        
        user = MockUser()
        mock_cursor.fetchone.return_value = user
        mock_cursor.fetchall.return_value = []  # No custom tones
        
        # Use app context for session access
        with app.test_request_context():
            from app import session
            
            # Verify password check works before testing login
            from werkzeug.security import check_password_hash
            password_check_result = check_password_hash(hashed_pwd, "CorrectPassword123!")
            assert password_check_result is True, "Password hash verification should work"
            
            # Attempt login
            result = UserSession.login("test@example.com", "CorrectPassword123!")
            
            # Should succeed
            assert result is True, f"Login failed. Hash format: {hashed_pwd[:50]}..., Password check: {password_check_result}"
            assert 'user' in session
            assert session['user']['id'] == 1
            assert session['user']['email'] == 'test@example.com'
    
    @patch('app.get_db')
    @patch('app.session', {})
    def test_login_with_plain_text_password_migration(self, mock_get_db, mock_user):
        """Test login with plain text password (legacy users) - should migrate"""
        from app import session
        
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Create mock user with plain text password (legacy)
        user = Mock()
        user.id = 1
        user.username = 'legacyuser'
        user.email = 'legacy@example.com'
        user.password = "PlainTextPassword123!"  # Plain text
        user.firm = 'Test Firm'
        user.location = 'Test City'
        user.lawyer_name = 'Test Lawyer'
        user.state = 'CA'
        user.address = ''
        user.planning_session = ''
        user.other_planning_session = ''
        user.discovery_call_link = ''
        user.is_admin = False
        user.is_blocked = False
        
        mock_cursor.fetchone.return_value = user
        mock_cursor.fetchall.return_value = []  # No custom tones
        
        # Attempt login
        result = UserSession.login("legacy@example.com", "PlainTextPassword123!")
        
        # Should succeed
        assert result is True
        
        # Password should be migrated to hashed format
        update_calls = [call for call in mock_cursor.execute.call_args_list 
                       if 'UPDATE users SET password' in str(call)]
        assert len(update_calls) > 0  # Should have updated password
    
    @patch('app.get_db')
    def test_login_with_wrong_password(self, mock_get_db):
        """Test login with wrong password"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Create mock user
        user = Mock()
        user.id = 1
        user.password = generate_password_hash("CorrectPassword123!")
        
        mock_cursor.fetchone.return_value = user
        
        # Attempt login with wrong password
        result = UserSession.login("test@example.com", "WrongPassword456!")
        
        # Should fail
        assert result is False
    
    @patch('app.get_db')
    def test_login_with_nonexistent_user(self, mock_get_db):
        """Test login with non-existent user"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # No user found
        mock_cursor.fetchone.return_value = None
        
        # Attempt login
        result = UserSession.login("nonexistent@example.com", "Password123!")
        
        # Should fail
        assert result is False
    
    @patch('app.get_db')
    @patch('app.session', {})
    def test_login_blocks_blocked_user(self, mock_get_db):
        """Test that blocked users cannot login"""
        from app import session
        
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Create mock blocked user
        user = Mock()
        user.id = 1
        user.username = 'blockeduser'
        user.email = 'blocked@example.com'
        user.password = generate_password_hash("Password123!")
        user.is_blocked = True  # User is blocked
        
        mock_cursor.fetchone.return_value = user
        
        # Attempt login
        result = UserSession.login("blocked@example.com", "Password123!")
        
        # Should fail
        assert result is False
        assert 'user' not in session


@pytest.mark.integration
class TestAuthenticationIntegration:
    """Integration tests for authentication flows"""
    
    def test_register_then_login_flow(self, client):
        """Test complete flow: register user, then login"""
        # This would require a test database setup
        # For now, we'll mark it as integration test
        pytest.skip("Requires test database setup")
    
    def test_password_reset_flow(self, client):
        """Test password reset flow"""
        # This would require a test database setup
        pytest.skip("Requires test database setup")

