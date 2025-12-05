"""
Unit tests for UserSession class
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import UserSession


class TestUserSessionProfile:
    """Test user profile management"""
    
    @patch('app.get_db')
    def test_update_profile_updates_database(self, mock_get_db, app):
        """Test that update_profile updates the database"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Use app context for session access
        with app.test_request_context():
            from app import session
            session['user'] = {'username': 'testuser'}
            
            # Update profile
            result = UserSession.update_profile(
                username='testuser',
                firm='New Firm',
                location='New City',
                lawyer_name='New Lawyer',
                state='NY',
                address='123 Main St',
                planning_session='Planning Session',
                other_planning_session='Other Session',
                discovery_call_link='https://example.com/call',
                selected_tone='Professional',
                tone_description='Professional tone',
                keywords='estate planning, legacy'
            )
        
        # Should succeed
        assert result is True
        mock_db.commit.assert_called_once()
        
        # Check that UPDATE was called
        update_calls = [call for call in mock_cursor.execute.call_args_list 
                       if 'UPDATE users' in str(call)]
        assert len(update_calls) > 0
    
    @patch('app.get_db')
    def test_update_profile_updates_session(self, mock_get_db):
        """Test that update_profile updates the session"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Set up session as a mock with proper dict-like behavior
        session_data = {'username': 'testuser', 'firm': 'Old Firm'}
        mock_session = MagicMock()
        mock_session.__getitem__ = lambda self, key: session_data if key == 'user' else None
        mock_session.__contains__ = lambda self, key: key == 'user'
        mock_session.__setitem__ = lambda self, key, value: None
        mock_session.update = lambda self, values: session_data.update(values)
        mock_session.modified = True
        
        # Patch session
        with patch('app.session', mock_session):
            # Update profile
            UserSession.update_profile(
                username='testuser',
                firm='New Firm',
                location='New City',
                lawyer_name='New Lawyer',
                state='NY'
            )
        
        # Session should be updated
        assert session_data['firm'] == 'New Firm'
        assert session_data['location'] == 'New City'
        assert session_data['lawyer_name'] == 'New Lawyer'
        assert session_data['state'] == 'NY'
    
    def test_get_current_user_returns_session_user(self, app):
        """Test that get_current_user returns user from session"""
        # Use app context for session access
        with app.test_request_context():
            from app import session
            
            # Set up session
            test_user = {
                'id': 1,
                'username': 'testuser',
                'email': 'test@example.com'
            }
            session['user'] = test_user
            
            # Get current user
            user = UserSession.get_current_user()
            
            # Should return session user
            assert user == test_user
    
    def test_get_current_user_returns_none_when_not_logged_in(self, app):
        """Test that get_current_user returns None when not logged in"""
        # Use app context for session access
        with app.test_request_context():
            from app import session
            
            # Clear session
            session.clear()
            
            # Get current user
            user = UserSession.get_current_user()
            
            # Should return None
            assert user is None


class TestUserSessionCustomTones:
    """Test custom tone management"""
    
    @patch('app.get_db')
    def test_add_custom_tone(self, mock_get_db, app):
        """Test adding a custom tone"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Use app context for session access
        with app.test_request_context():
            from app import session
            session['user'] = {
                'id': 1,
                'custom_tones': []  # Initialize custom_tones list
            }
            
            # Add custom tone
            result = UserSession.add_custom_tone(
                user_id=1,
                tone_name='Custom Tone',
                tone_description='A custom tone description'
            )
        
        # Should succeed
        assert result is True
        mock_db.commit.assert_called_once()
    
    @patch('app.get_db')
    def test_get_custom_tones(self, mock_get_db):
        """Test getting custom tones for a user"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Mock tone results
        tone1 = Mock()
        tone1.name = 'Tone 1'
        tone1.description = 'Description 1'
        tone2 = Mock()
        tone2.name = 'Tone 2'
        tone2.description = 'Description 2'
        
        mock_cursor.fetchall.return_value = [tone1, tone2]
        
        # Get custom tones
        tones = UserSession.get_custom_tones(user_id=1)
        
        # Should return tones
        assert len(tones) == 2
        assert tones[0]['name'] == 'Tone 1'
        assert tones[1]['name'] == 'Tone 2'


class TestUserSessionBlocking:
    """Test user blocking functionality"""
    
    @patch('app.get_db')
    def test_is_user_blocked_returns_true_for_blocked_user(self, mock_get_db):
        """Test that is_user_blocked returns True for blocked users"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Mock blocked user
        user = Mock()
        user.is_blocked = True
        mock_cursor.fetchone.return_value = user
        
        # Check if blocked
        result = UserSession.is_user_blocked(user_id=1)
        
        # Should return True
        assert result is True
    
    @patch('app.get_db')
    def test_is_user_blocked_returns_false_for_active_user(self, mock_get_db):
        """Test that is_user_blocked returns False for active users"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Mock active user
        user = Mock()
        user.is_blocked = False
        mock_cursor.fetchone.return_value = user
        
        # Check if blocked
        result = UserSession.is_user_blocked(user_id=1)
        
        # Should return False
        assert result is False

