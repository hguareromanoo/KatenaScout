import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from decimal import Decimal

# Modules to test
from backend.services import data_service
from backend.models import sql_models # For creating mock instances

# --- Mock Data Factories ---
def mock_player_model(id=1, name="Test Player", position="F", country_id=1, country=None):
    player = MagicMock(spec=sql_models.Player)
    player.id = id
    player.name = name
    player.position = position # DB uses 'F', 'M', 'D', 'G'
    player.country_id = country_id
    player.country = country
    # Add other attributes as needed by tests for player_search.get_player_info or converters
    player.date_of_birth_timestamp = 788918400 # Example: 1995-01-01
    player.height = 180
    player.preferred_foot = "Right"
    player.contract_until_timestamp = 1735689600 # Example: 2025-01-01
    player.player_teams = [] # Mock relationship
    player.player_statistics = [] # Mock relationship
    return player

def mock_team_model(id=1, name="Test Team", country_id=1, country=None):
    team = MagicMock(spec=sql_models.Team)
    team.id = id
    team.name = name
    team.country_id = country_id
    team.country = country
    return team

def mock_country_model(id=1, name="Test Country"):
    country = MagicMock(spec=sql_models.Country)
    country.id = id
    country.name = name
    return country

def mock_player_statistic_model(player_id=1, rating=Decimal("7.5"), goals=5):
    stat = MagicMock(spec=sql_models.PlayerStatistic)
    stat.player_id = player_id
    stat.rating = rating
    stat.goals = goals
    # Add other stats as needed for avg/sigma tests
    stat.minutes_played = 900
    stat.goal_assist = 3
    stat.total_pass = 500
    stat.accurate_pass = 400
    stat.total_long_balls = 50
    stat.accurate_long_balls = 25
    stat.key_pass = 10
    stat.total_tackle = 20
    stat.touches = 700
    stat.expected_goals = Decimal("4.5")
    stat.expected_assists = Decimal("2.5")
    return stat

# --- Unit Tests for data_service.py ---

def test_find_player_by_id_found(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    mock_player = mock_player_model(id=123, name="Found Player")
    
    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_player
    
    player = data_service.find_player_by_id(player_id=123, db=mock_db_session)
    
    mock_db_session.query.assert_called_once_with(sql_models.Player)
    mock_query.filter.assert_called_once() # Check filter was called
    mock_filter.first.assert_called_once()
    assert player is not None
    assert player.id == 123
    assert player.name == "Found Player"

def test_find_player_by_id_not_found(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    
    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None # Simulate player not found
    
    player = data_service.find_player_by_id(player_id=456, db=mock_db_session)
    
    assert player is None

def test_find_player_by_name_found(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    mock_player = mock_player_model(name="Specific Name")

    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_player

    player = data_service.find_player_by_name(player_name="Specific Name", db=mock_db_session)

    mock_db_session.query.assert_called_once_with(sql_models.Player)
    # sqlalchemy.func.lower(Player.name).ilike(search_term) is complex to assert directly on call
    # We trust the filter was called.
    mock_query.filter.assert_called_once() 
    mock_filter.first.assert_called_once()
    assert player is not None
    assert player.name == "Specific Name"

def test_find_club_by_id_found(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    mock_team = mock_team_model(id=789, name="Found Club")

    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = mock_team
    
    team = data_service.find_club_by_id(club_id=789, db=mock_db_session)
    
    mock_db_session.query.assert_called_once_with(sql_models.Team)
    assert team is not None
    assert team.id == 789
    assert team.name == "Found Club"

def test_get_team_names(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    mock_country1 = mock_country_model(id=1, name="Countryland")
    mock_team1 = mock_team_model(id=10, name="Team A", country=mock_country1)
    mock_team2 = mock_team_model(id=20, name="Team B", country=None) # Team with no country

    mock_query = mock_db_session.query.return_value
    mock_options = mock_query.options.return_value # For joinedload
    mock_options.all.return_value = [mock_team1, mock_team2]

    team_names_dict = data_service.get_team_names(db=mock_db_session)

    mock_db_session.query.assert_called_once_with(sql_models.Team)
    mock_query.options.assert_called_once() # Check joinedload was used
    mock_options.all.assert_called_once()
    
    assert "10" in team_names_dict
    assert team_names_dict["10"]["name"] == "Team A"
    assert team_names_dict["10"]["country"] == "Countryland"
    assert "20" in team_names_dict
    assert team_names_dict["20"]["name"] == "Team B"
    assert team_names_dict["20"]["country"] is None


def test_get_players_with_position(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    player_fwd1 = mock_player_model(id=1, name="Forward Player 1", position="F")
    player_fwd2 = mock_player_model(id=2, name="Forward Player 2", position="F")
    
    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = [player_fwd1, player_fwd2]

    # Test with a granular code that maps to 'F'
    players = data_service.get_players_with_position(position_code="cf", db=mock_db_session)

    mock_db_session.query.assert_called_once_with(sql_models.Player)
    # Check that Player.position == 'F' was part of the filter call
    # This is tricky due to the way SQLAlchemy expressions are built.
    # A simpler check is that filter was called and the right players were returned.
    mock_query.filter.assert_called_once() 
    assert len(players) == 2
    assert players[0].name == "Forward Player 1"

def test_get_players_with_position_invalid_code(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    players = data_service.get_players_with_position(position_code="invalid_pos", db=mock_db_session)
    assert len(players) == 0
    mock_db_session.query.assert_not_called() # Should return early if code not in map

def test_get_average_statistics(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    
    # Mock the row structure returned by the query
    mock_row = MagicMock()
    mock_row.position = "F" # DB position char
    mock_row._fields = ["position", "avg_rating", "avg_goals"] # Match labels in query
    mock_row.avg_rating = Decimal("7.2")
    mock_row.avg_goals = Decimal("0.8")

    mock_query = mock_db_session.query.return_value
    mock_join = mock_query.join.return_value
    mock_group_by = mock_join.group_by.return_value
    mock_group_by.all.return_value = [mock_row]

    avg_stats = data_service.get_average_statistics(db=mock_db_session)

    mock_db_session.query.assert_called() # Called with multiple model attributes
    mock_query.join.assert_called_once()
    mock_join.group_by.assert_called_once()
    mock_group_by.all.assert_called_once()

    assert "F" in avg_stats
    assert avg_stats["F"]["rating"] == Decimal("7.2")
    assert avg_stats["F"]["goals"] == Decimal("0.8")

def test_get_sigma_by_position(mocker):
    mock_db_session = mocker.MagicMock(spec=Session)
    
    mock_row = MagicMock()
    mock_row.position = "M"
    mock_row._fields = ["position", "stddev_rating", "stddev_total_pass"]
    mock_row.stddev_rating = Decimal("0.5")
    mock_row.stddev_total_pass = Decimal("15.3")

    mock_query = mock_db_session.query.return_value
    mock_join = mock_query.join.return_value
    mock_group_by = mock_join.group_by.return_value
    mock_group_by.all.return_value = [mock_row]

    sigma_stats = data_service.get_sigma_by_position(db=mock_db_session)

    mock_db_session.query.assert_called()
    mock_query.join.assert_called_once()
    mock_join.group_by.assert_called_once()
    mock_group_by.all.assert_called_once()

    assert "M" in sigma_stats
    assert sigma_stats["M"]["rating"] == Decimal("0.5")
    assert sigma_stats["M"]["total_pass"] == Decimal("15.3")

# Test for load_json dependent functions (e.g., get_weights_dictionary)
@patch('backend.services.data_service.load_json') # Patch load_json in data_service module
def test_get_weights_dictionary(mock_load_json, mocker):
    mock_weights_data = {"cf": {"goals": 1.0, "shots": 0.5}}
    mock_load_json.return_value = mock_weights_data
    
    weights = data_service.get_weights_dictionary()
    
    mock_load_json.assert_called_once_with('weights_dict.json')
    assert weights == mock_weights_data

@patch('backend.services.data_service.open', new_callable=mocker.mock_open, read_data='{"key": "value"}')
@patch('backend.services.data_service.json.load')
@patch('backend.services.data_service.os.path.abspath') # Mock abspath if used in error messages
@patch('backend.services.data_service.os.path.dirname') # Mock dirname
def test_load_json_success(mock_dirname, mock_abspath, mock_json_load, mock_open_file):
    # Configure mocks
    # Simulate that the file is found in the 'backend/' directory path construction
    # os.path.dirname(os.path.dirname(os.path.abspath(__file__))) -> /app/backend
    # os.path.join(base_dir, filename) -> /app/backend/test.json
    # For this test, we want the primary path `os.path.join('backend', filename)` to work.
    # This means the test needs to be "run" from a context where 'backend/test.json' is valid.
    # Or, more simply, ensure one of the attempted paths in load_json works.
    
    # Let's assume the file is found at `os.path.join('backend', filename)`
    # To do this, we need to make the `open` call for that path succeed.
    # The `patch` on `open` will make it succeed for any path if not configured further.
    
    mock_json_load.return_value = {"key": "value_loaded"}
    
    # Clear cache for this specific test if it's used across tests
    if 'test.json' in data_service._json_data_cache:
        del data_service._json_data_cache['test.json']
        
    result = data_service.load_json('test.json')
    
    # Assert that open was called. The path depends on execution context, so difficult to assert specific path.
    mock_open_file.assert_called() # Check it was called, specific path is tricky
    mock_json_load.assert_called_once()
    assert result == {"key": "value_loaded"}
    assert 'test.json' in data_service._json_data_cache # Check caching

@patch('backend.services.data_service.open', side_effect=FileNotFoundError)
@patch('backend.services.data_service.os.path.abspath', return_value="/abs/path/to/file")
@patch('backend.services.data_service.os.path.dirname', return_value="/abs/path/to")
def test_load_json_not_found(mock_dirname, mock_abspath, mock_open_file):
    # Clear cache
    if 'notfound.json' in data_service._json_data_cache:
        del data_service._json_data_cache['notfound.json']

    with pytest.raises(FileNotFoundError) as excinfo:
        data_service.load_json('notfound.json')
    
    assert "Could not find notfound.json" in str(excinfo.value)
    # Check that multiple paths were attempted by open
    assert mock_open_file.call_count > 1
