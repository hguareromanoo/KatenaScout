"""
Data services for KatenaScout

This module handles loading and accessing player and team data using SQLAlchemy,
and loads auxiliary statistical files from JSON.
"""

import json
import os 
from typing import Dict, Any, Optional, List

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func as sql_alchemy_func # Renamed to avoid conflict if we define a 'func'
from sqlalchemy.sql import func as sql_func # For avg, stddev_samp etc.

from backend.models.sql_models import Player, Team, Country, PlayerStatistic

# Cache for loaded auxiliary JSON files
_json_data_cache: Dict[str, Any] = {}

def load_json(filename: str) -> Dict[str, Any]:
    """
    Load an auxiliary JSON file (e.g., statistics, weights) from the 'backend' directory.
    
    Args:
        filename: The name of the JSON file to load (e.g., 'average_statistics_by_position.json').
        
    Returns:
        The parsed JSON data.
        
    Raises:
        FileNotFoundError: If the file could not be found in 'backend/{filename}'.
        ValueError: If the JSON file is malformed.
    """
    if filename in _json_data_cache:
        return _json_data_cache[filename]
    
    # Construct path: assumes JSON files are in the 'backend' directory,
    # and this script is run from a context where 'backend' is a subdir.
    path_to_file = os.path.join('backend', filename)

    try:
        with open(path_to_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            _json_data_cache[filename] = data
            return data
    except FileNotFoundError:
        # Fallback for cases where CWD might be backend/ already (e.g. some test setups)
        alternate_path = filename
        try:
            with open(alternate_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                _json_data_cache[filename] = data
                return data
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find {filename}. Tried: {os.path.abspath(path_to_file)} and {os.path.abspath(alternate_path)}"
            )
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON from {filename} (tried path: {path_to_file}): {e}")

# --- Position Mapping Definitions ---
# For converting granular frontend/logic codes to DB's single char storage
GRANULAR_TO_DB_POSITION_MAP = {
    # Goalkeepers
    'gk': 'G',
    # Defenders
    'cb': 'D', 'lcb': 'D', 'rcb': 'D',
    'lb': 'D', 'lwb': 'D',
    'rb': 'D', 'rwb': 'D',
    # Midfielders
    'dmf': 'M', 'ldmf': 'M', 'rdmf': 'M',
    'cmf': 'M', 'lcmf': 'M', 'rcmf': 'M',
    'amf': 'M', 'lamf': 'M', 'ramf': 'M',
    # Forwards
    'lw': 'F', 'lwf': 'F',
    'rw': 'F', 'rwf': 'F',
    'cf': 'F',
}

# For mapping DB's single char to a default granular code (FR11)
DB_TO_GRANULAR_FALLBACK_MAP = {
    'G': 'gk',
    'D': 'cb', # Default for Defenders
    'M': 'cmf',# Default for Midfielders (rcmf was in PRD, but cmf is more general)
    'F': 'cf'  # Default for Forwards
}


# --- Database-Derived Statistics and Auxiliary Data Functions ---

def get_average_statistics(db: Session) -> Dict[str, Dict[str, Optional[float]]]:
    """
    Calculate average player statistics by general DB position (G, D, M, F).
    Args:
        db: SQLAlchemy Session object.
    Returns:
        Dictionary where keys are DB position characters ('G', 'D', 'M', 'F')
        and values are dictionaries of average statistic values.
        Example: {'D': {'avg_goals': 0.5, 'avg_accurate_pass': 75.2}, ...}
    """
    stats_query = db.query(
        Player.position,
        sql_func.avg(PlayerStatistic.rating).label('avg_rating'),
        sql_func.avg(PlayerStatistic.minutes_played).label('avg_minutes_played'),
        sql_func.avg(PlayerStatistic.goals).label('avg_goals'),
        sql_func.avg(PlayerStatistic.goal_assist).label('avg_goal_assist'),
        sql_func.avg(PlayerStatistic.total_pass).label('avg_total_pass'),
        sql_func.avg(PlayerStatistic.accurate_pass).label('avg_accurate_pass'),
        sql_func.avg(PlayerStatistic.total_long_balls).label('avg_total_long_balls'),
        sql_func.avg(PlayerStatistic.accurate_long_balls).label('avg_accurate_long_balls'),
        sql_func.avg(PlayerStatistic.key_pass).label('avg_key_pass'),
        sql_func.avg(PlayerStatistic.total_tackle).label('avg_total_tackle'),
        sql_func.avg(PlayerStatistic.touches).label('avg_touches'),
        sql_func.avg(PlayerStatistic.expected_goals).label('avg_expected_goals'),
        sql_func.avg(PlayerStatistic.expected_assists).label('avg_expected_assists')
        # Add other relevant fields from PlayerStatistic model here
    ).join(Player, PlayerStatistic.player_id == Player.id).group_by(Player.position)

    results = {}
    for row in stats_query.all():
        pos = row.position
        if pos: # Ensure position is not None
            results[pos] = {
                stat_name.replace('avg_', ''): getattr(row, stat_name)
                for stat_name in row._fields if stat_name != 'position' # type: ignore
            }
            # Convert Decimal to float for JSON compatibility if necessary, though SQLAlchemy usually handles this.
            # For any fields that might be None (e.g., if all values for a group are NULL),
            # they will be None here. The Optional[float] handles this.
    return results


def get_sigma_by_position(db: Session) -> Dict[str, Dict[str, Optional[float]]]:
    """
    Calculate standard deviation of player statistics by general DB position.
    Args:
        db: SQLAlchemy Session object.
    Returns:
        Dictionary similar to get_average_statistics but with stddev values.
        Example: {'D': {'stddev_goals': 0.1, ...}, ...}
    """
    stats_query = db.query(
        Player.position,
        sql_func.stddev_samp(PlayerStatistic.rating).label('stddev_rating'),
        sql_func.stddev_samp(PlayerStatistic.minutes_played).label('stddev_minutes_played'),
        sql_func.stddev_samp(PlayerStatistic.goals).label('stddev_goals'),
        sql_func.stddev_samp(PlayerStatistic.goal_assist).label('stddev_goal_assist'),
        sql_func.stddev_samp(PlayerStatistic.total_pass).label('stddev_total_pass'),
        sql_func.stddev_samp(PlayerStatistic.accurate_pass).label('stddev_accurate_pass'),
        # Add other fields as needed
    ).join(Player, PlayerStatistic.player_id == Player.id).group_by(Player.position)

    results = {}
    for row in stats_query.all():
        pos = row.position
        if pos:
            results[pos] = {
                stat_name.replace('stddev_', ''): getattr(row, stat_name)
                for stat_name in row._fields if stat_name != 'position' # type: ignore
            }
    return results

def get_weights_dictionary() -> Dict[str, Any]:
    """
    Get weights dictionary for scoring.
    Currently loads from 'weights_dict.json'. Future implementation might change source.
    """
    try:
        return load_json('weights_dict.json')
    except (FileNotFoundError, ValueError) as e:
        print(f"Warning/Error loading 'weights_dict.json': {e}. Using mock data.")
        # This mock data should ideally match the structure expected by consuming components.
        return {
            "cb": {"goals": 0.1, "accurate_pass": 0.8, "total_tackle": 0.9}, # Example for 'cb'
            "cmf": {"goals": 0.5, "assists": 0.7, "passing": 0.9, "progressivePasses": 0.8},
            "amf": {"goals": 0.8, "assists": 0.9, "passing": 0.7, "progressivePasses": 0.6},
            "cf": {"goals": 1.0, "shot_off_target": -0.2} # Example for 'cf'
        }

# --- SQLAlchemy based Core Data Access Functions ---

def get_team_names(db: Session) -> Dict[str, Dict[str, Any]]:
    """
    Get team names and their countries from the database.
    
    Args:
        db: SQLAlchemy Session object.
        
    Returns:
        Dictionary mapping team ID (as string) to team name and country name.
    """
    # Using sql_alchemy_func for general SQLAlchemy functions like lower, ilike
    teams_data = db.query(Team).options(joinedload(Team.country)).all()
    return {
        str(team.id): {
            "name": team.name,
            "country": team.country.name if team.country else None
        }
        for team in teams_data
    }

def find_player_by_id(player_id: int, db: Session) -> Optional[Player]:
    """
    Find a player by their ID.
    
    Args:
        player_id: The integer ID of the player to find.
        db: SQLAlchemy Session object.
        
    Returns:
        A Player object if found, else None.
    """
    return db.query(Player).filter(Player.id == player_id).first()

def find_player_by_name(player_name: str, db: Session) -> Optional[Player]:
    """
    Find a player by their name (case-insensitive, partial match).
    Returns the first match found.
    
    Args:
        player_name: The name of the player to search for.
        db: SQLAlchemy Session object.
        
    Returns:
        A Player object if found, else None.
    """
    search_term = f"%{player_name.lower()}%"
    return db.query(Player).filter(sql_alchemy_func.lower(Player.name).ilike(search_term)).first()

def find_club_by_id(club_id: int, db: Session) -> Optional[Team]:
    """
    Find a club (team) by its ID.
    
    Args:
        club_id: The integer ID of the club to find.
        db: SQLAlchemy Session object.
        
    Returns:
        A Team object if found, else None.
    """
    return db.query(Team).filter(Team.id == club_id).first()

def get_players_with_position(position_code: str, db: Session) -> List[Player]:
    """
    Get all players that play in the specified granular position.
    Uses GRANULAR_TO_DB_POSITION_MAP to convert to DB's single character code.
    
    Args:
        position_code: The granular position code (e.g., 'cb', 'amf', 'gk').
        db: SQLAlchemy Session object.
        
    Returns:
        List of Player objects matching the translated DB position.
        Returns an empty list if the granular position code is not recognized.
    """
    db_position_char = GRANULAR_TO_DB_POSITION_MAP.get(position_code.lower().strip())
    
    if not db_position_char:
        # Or raise ValueError("Invalid position_code")
        print(f"Warning: Unrecognized granular position_code '{position_code}'. Returning empty list.")
        return []
        
    return db.query(Player).filter(Player.position == db_position_char).all()

# The `if __name__ == "__main__":` block has been removed as its original utility
# (testing old JSON-based functions) is no longer applicable. Testing SQLAlchemy functions
# requires a database session and is best done in dedicated test files.