import pytest
from flask import Flask, jsonify # Flask is needed to create app context for some tests
from unittest.mock import patch, MagicMock, mock_open
import json
from decimal import Decimal

# Assuming your Flask app instance is created in backend.app
# You might need to adjust this import based on your project structure
from backend.app import app as flask_app 
from backend.models import sql_models # For creating mock PlayerModel instances
from backend.utils import converters # To potentially cross-check conversion if needed
from backend.services.data_service import DB_TO_GRANULAR_FALLBACK_MAP # For position checks

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Minimal configuration for testing
    flask_app.config.update({
        "TESTING": True,
        # Add other configurations if needed, e.g., for database
    })
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

# --- Mock Data Factories (similar to test_data_service.py but might be used differently) ---
def mock_player_model_for_app(id=1, name="Test Player API", position="F", country=None, date_of_birth_timestamp=788918400, height=180, preferred_foot="Right"):
    player = MagicMock(spec=sql_models.Player)
    player.id = id
    player.name = name
    player.position = position
    player.country = country
    player.date_of_birth_timestamp = date_of_birth_timestamp
    player.height = height
    player.preferred_foot = preferred_foot
    player.contract_until_timestamp = 1735689600 # Example
    # Mock relationships if accessed by converters directly (though converters try to use preloaded data)
    player.player_teams = [] 
    player.player_statistics = []
    return player

def mock_country_model_for_app(id=1, name="Country API"):
    country = MagicMock(spec=sql_models.Country)
    country.id = id
    country.name = name
    return country

# --- Integration Tests for app.py Endpoints ---

@patch('backend.app.get_db') # Patch get_db where it's imported in app.py
def test_players_search_no_query(mock_get_db, client):
    mock_db_session = MagicMock()
    # Simulate get_db yielding the mock session
    mock_get_db.return_value = iter([mock_db_session]) 
    
    mock_country = mock_country_model_for_app(id=1, name="Testlandia")
    mock_player1 = mock_player_model_for_app(id=101, name="Player Alpha", position="F", country=mock_country)
    mock_player2 = mock_player_model_for_app(id=102, name="Player Beta", position="M", country=mock_country)

    mock_query_result = MagicMock()
    mock_query_result.limit.return_value.all.return_value = [mock_player1, mock_player2]
    mock_db_session.query.return_value = mock_query_result
    
    response = client.get('/players/search?limit=2')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert len(data["players"]) == 2
    
    # Check structure of first player (converted by convert_player_model_to_pydantic_summary)
    p1_data = data["players"][0]
    assert p1_data["id"] == "101" # ID is stringified by Pydantic model
    assert p1_data["name"] == "Player Alpha"
    assert p1_data["positions"] == [DB_TO_GRANULAR_FALLBACK_MAP.get("F")]
    assert p1_data["club"] == "Unknown Club" # Default from converter
    assert p1_data["nationality"] == "Testlandia"
    assert p1_data["image_url"] == "/player-image/101"

@patch('backend.app.get_db')
def test_players_search_with_query(mock_get_db, client):
    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])

    mock_country = mock_country_model_for_app(id=1, name="Queryland")
    mock_player_q = mock_player_model_for_app(id=201, name="Queried Player", position="D", country=mock_country)

    # Mock for the .contains() part of the query
    mock_filtered_query = MagicMock()
    mock_filtered_query.limit.return_value.all.return_value = [mock_player_q]
    
    # query(PlayerModel).filter(...).limit().all()
    mock_db_session.query.return_value.filter.return_value = mock_filtered_query
    
    response = client.get('/players/search?query=Queried&limit=1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert len(data["players"]) == 1
    p1_data = data["players"][0]
    assert p1_data["name"] == "Queried Player"
    assert p1_data["score"] is not None # Score should be present

@patch('backend.app.get_db')
@patch('backend.app.send_from_directory') # To mock actual file sending
@patch('backend.app.os.path.exists') # To mock os.path.exists
def test_player_image_found_local(mock_os_path_exists, mock_send_from_directory, mock_get_db, client):
    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])
    
    # Simulate player exists in DB (though image URL is not on model)
    mock_player = mock_player_model_for_app(id=301)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_player
    
    # Simulate local image file exists
    mock_os_path_exists.return_value = True 
    # Mock send_from_directory to return a simple response
    mock_send_from_directory.return_value = MagicMock(status_code=200, data=b"fake_image_data", headers={})
    # To make it a Flask response, we might need to configure it more or let it be a MagicMock
    
    response = client.get('/player-image/301')
    # We are not checking response.status_code == 200 directly from send_from_directory
    # because add_cors_headers modifies it. Instead, we check if it was called.
    mock_send_from_directory.assert_called() 
    # The actual status code and data would depend on how mock_send_from_directory is handled by add_cors_headers
    # For a more robust test, mock_send_from_directory could return a Response object.

@patch('backend.app.get_db')
@patch('backend.app.os.path.exists', return_value=False) # Simulate no local files exist
def test_player_image_not_found(mock_os_path_exists, mock_get_db, client):
    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])
    
    # Simulate player not found in DB for image check (or found but no image path on model)
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    response = client.get('/player-image/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Image not found"

# Basic smoke tests for more complex endpoints
@patch('backend.app.get_db')
@patch('backend.app.session_manager') # Mock the session manager
@patch('core.handlers.handle_player_search') # Mock the specific handler
def test_enhanced_search_smoke(mock_handle_search, mock_session_mgr, mock_get_db, client):
    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])
    
    mock_session_data = MagicMock()
    mock_session_mgr.get_session.return_value = mock_session_data
    
    # Mock the handler to return a basic valid structure
    mock_handle_search.return_value = {"type": "text", "text": "Search handled"}
    
    request_data = {
        "session_id": "test-session",
        "query": "Find tall defenders",
        "is_follow_up": False,
        "language": "english"
    }
    response = client.post('/enhanced_search', json=request_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["response"] == "Search handled"
    # Verify db session was passed to handler
    mock_handle_search.assert_called_once()
    # Check if db_session was part of the call_args (args or kwargs)
    # args, kwargs = mock_handle_search.call_args
    # assert mock_db_session in args or mock_db_session in kwargs.values() # This is more complex to check precisely

@patch('backend.app.get_db')
@patch('backend.app.generate_scout_report_html') # Mock the report generation function itself
def test_scout_report_html_smoke(mock_generate_html, mock_get_db, client):
    mock_db_session = MagicMock()
    mock_get_db.return_value = iter([mock_db_session])

    # Mock player found by find_player_by_id_service
    mock_player = mock_player_model_for_app(id=777, name="Report Player")
    # This mock needs to be for the find_player_by_id_service call inside generate_scout_report (in processor.py)
    # or the one in app.py's scout_report route. The one in app.py is easier to patch here.
    with patch('backend.app.find_player_by_id_service') as mock_find_player_service_in_app:
        mock_find_player_service_in_app.return_value = mock_player
        mock_generate_html.return_value = "path/to/report.html" 
        
        # Mock open for reading the HTML file content
        with patch('builtins.open', mock_open(read_data="<html>Report</html>")) as mock_file:
            response = client.post('/scout_report', json={
                "session_id": "report-session", "player_id": "777", "format": "html"
            })
            assert response.status_code == 200
            assert "<html>Report</html>" in response.get_data(as_text=True)
            mock_generate_html.assert_called_once()

# TODO: Add more tests, especially for error conditions and other routes.
# Test for /player_comparison would be similar to /enhanced_search, mocking its handler.
# Testing file downloads for PDF scout reports is more complex.
# Testing for specific Pydantic model validation errors can also be added.
