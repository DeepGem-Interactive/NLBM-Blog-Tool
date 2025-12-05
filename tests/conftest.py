"""
Pytest configuration and fixtures for testing
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
import tempfile
import shutil

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    # Set test environment variables
    os.environ['FLASK_SECRET_KEY'] = 'test-secret-key-for-testing-only'
    os.environ['FLASK_DEBUG'] = 'false'
    os.environ['AZURE_SQL_SERVER'] = 'test-server'
    os.environ['AZURE_SQL_DATABASE'] = 'test-db'
    os.environ['AZURE_SQL_USERNAME'] = 'test-user'
    os.environ['AZURE_SQL_PASSWORD'] = 'test-password'
    os.environ['AZURE_FUNCTION_APP_URL'] = 'https://test-function-app.azurewebsites.net'
    os.environ['FUNCTION_KEY'] = 'test-function-key'
    os.environ['AZURE_OPENAI_KEY'] = 'test-openai-key'
    os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://test-openai.openai.azure.com'
    os.environ['AZURE_OPENAI_DEPLOYMENT'] = 'test-deployment'
    os.environ['AZURE_DALLE_KEY'] = 'test-dalle-key'
    os.environ['AZURE_DALLE_ENDPOINT'] = 'https://test-dalle.openai.azure.com'
    os.environ['AZURE_DALLE_DEPLOYMENT'] = 'test-dalle-deployment'
    os.environ['SIMULATE_OPENAI'] = 'true'
    
    # Import app after environment is set
    from app import app as flask_app
    
    # Configure for testing
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    yield flask_app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def mock_db():
    """Mock database connection"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.execute.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []
    return mock_conn, mock_cursor

@pytest.fixture
def mock_user():
    """Mock user object"""
    user = Mock()
    user.id = 1
    user.username = 'testuser'
    user.email = 'test@example.com'
    user.password = 'pbkdf2:sha256:260000$test$hashedpassword'
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
    return user

@pytest.fixture
def sample_session_data():
    """Sample session data for testing"""
    return {
        'user': {
            'id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'firm': 'Test Firm',
            'location': 'Test City',
            'lawyer_name': 'Test Lawyer',
            'state': 'CA',
            'is_admin': False
        }
    }

@pytest.fixture(autouse=True)
def reset_env():
    """Reset environment variables after each test"""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


