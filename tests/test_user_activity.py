"""
Unit tests for UserActivityTracker class
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import UserActivityTracker


class TestUserActivityLogging:
    """Test user activity logging"""
    
    @patch('app.get_db')
    def test_log_activity_logs_successful_activity(self, mock_get_db):
        """Test that log_activity logs successful activities"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Log activity
        result = UserActivityTracker.log_activity(
            user_id=1,
            activity_type="content_generation",
            feature_name="AI Article Generation",
            api_endpoint="/api/generate",
            request_payload_size=1000,
            response_status=200,
            response_size=5000,
            processing_time_ms=1500,
            success=True
        )
        
        # Should succeed
        assert result is True
        mock_db.commit.assert_called_once()
        
        # Check that INSERT was called
        insert_calls = [call for call in mock_cursor.execute.call_args_list 
                       if 'INSERT INTO user_activity' in str(call)]
        assert len(insert_calls) > 0
    
    @patch('app.get_db')
    def test_log_activity_logs_failed_activity(self, mock_get_db):
        """Test that log_activity logs failed activities"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Log failed activity
        result = UserActivityTracker.log_activity(
            user_id=1,
            activity_type="content_generation",
            feature_name="AI Article Generation",
            success=False,
            error_message="API timeout"
        )
        
        # Should succeed
        assert result is True
        mock_db.commit.assert_called_once()
    
    @patch('app.get_db')
    def test_log_activity_handles_database_errors(self, mock_get_db):
        """Test that log_activity handles database errors gracefully"""
        # Setup mock database to raise exception
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")
        mock_get_db.return_value = mock_db
        
        # Log activity (should handle error)
        result = UserActivityTracker.log_activity(
            user_id=1,
            activity_type="test",
            feature_name="Test Feature"
        )
        
        # Should return False on error
        assert result is False


class TestUserActivityQueries:
    """Test user activity query functions"""
    
    @patch('app.get_db')
    def test_get_user_activity_summary_for_user(self, mock_get_db):
        """Test getting activity summary for specific user"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Mock activity results
        activity1 = Mock()
        activity1.activity_type = 'content_generation'
        activity1.feature_name = 'AI Article Generation'
        activity1.usage_count = 10
        activity1.avg_processing_time = 1500.0
        activity1.success_count = 9
        activity1.error_count = 1
        
        mock_cursor.fetchall.return_value = [activity1]
        
        # Get activity summary
        summary = UserActivityTracker.get_user_activity_summary(user_id=1, days=30)
        
        # Should return results
        assert len(summary) == 1
        assert summary[0].activity_type == 'content_generation'
    
    @patch('app.get_db')
    def test_get_user_activity_summary_overall(self, mock_get_db):
        """Test getting overall activity summary"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Mock activity results
        mock_cursor.fetchall.return_value = []
        
        # Get overall activity summary
        summary = UserActivityTracker.get_user_activity_summary(days=30)
        
        # Should return results (even if empty)
        assert isinstance(summary, list)
    
    @patch('app.get_db')
    def test_get_feature_usage_stats(self, mock_get_db):
        """Test getting feature usage statistics"""
        # Setup mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db
        
        # Mock feature stats
        feature1 = Mock()
        feature1.feature_name = 'AI Article Generation'
        feature1.total_usage = 50
        feature1.unique_users = 10
        feature1.avg_processing_time = 1500.0
        feature1.success_count = 48
        feature1.error_count = 2
        
        mock_cursor.fetchall.return_value = [feature1]
        
        # Get feature usage stats
        stats = UserActivityTracker.get_feature_usage_stats(days=30)
        
        # Should return results
        assert len(stats) == 1
        assert stats[0].feature_name == 'AI Article Generation'
    
    @patch('app.get_db')
    def test_get_user_activity_summary_handles_errors(self, mock_get_db):
        """Test that get_user_activity_summary handles errors gracefully"""
        # Setup mock database to raise exception
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")
        mock_get_db.return_value = mock_db
        
        # Get activity summary (should handle error)
        summary = UserActivityTracker.get_user_activity_summary(user_id=1, days=30)
        
        # Should return empty list on error
        assert summary == []
    
    @patch('app.get_db')
    def test_get_feature_usage_stats_handles_errors(self, mock_get_db):
        """Test that get_feature_usage_stats handles errors gracefully"""
        # Setup mock database to raise exception
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")
        mock_get_db.return_value = mock_db
        
        # Get feature usage stats (should handle error)
        stats = UserActivityTracker.get_feature_usage_stats(days=30)
        
        # Should return empty list on error
        assert stats == []


