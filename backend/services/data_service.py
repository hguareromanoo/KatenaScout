"""
Data services for KatenaScout

This module handles loading and accessing player data.
"""

import os
import json
from typing import Dict, Any, Optional, List

# Cache for loaded data files
_data_cache = {}


def find_club_by_id(club_id: str) -> Optional[Dict[str, Any]]:
    team_json = load_json('team.json')
    return team_json[club_id] if club_id in team_json else None
def load_json(filename: str) -> Dict[str, Any]:
    """
    Load a JSON file, trying different paths
    
    Args:
        filename: The name of the JSON file to load
        
    Returns:
        The parsed JSON data
        
    Raises:
        FileNotFoundError: If the file could not be found in any expected location
    """
    # Check if already cached
    if filename in _data_cache:
        return _data_cache[filename]
    
    # Try different paths
    paths = [
        filename,  # Current directory
        os.path.join('backend', filename),  # Backend subdirectory
        os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)  # From services directory
    ]
    
    for path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Cache the result
                _data_cache[filename] = data
                return data
        except FileNotFoundError:
            continue
    
    raise FileNotFoundError(f"Could not find {filename} in any expected location")

def get_player_database() -> Dict[str, Any]:
    """Get the player database by name"""
    try:
        return load_json('database.json')
    except FileNotFoundError:
        # Return mock data for testing
        return {
            "João Silva": {
                "wyId": "123456",
                "age": 25,
                "height": 180,
                "weight": 75,
                "positions": [
                    {"position": {"code": "cmf", "name": "Central Midfielder"}}
                ],
                "stats": {
                    "goals": 5,
                    "assists": 8,
                    "passing": 85.5,
                    "progressivePasses": 12.3
                },
                "nationality": {"name": "Brazil"},
                "foot": "right"
            },
            "Carlos Mendez": {
                "wyId": "789012",
                "age": 24,
                "height": 178,
                "weight": 72,
                "positions": [
                    {"position": {"code": "cmf", "name": "Central Midfielder"}},
                    {"position": {"code": "amf", "name": "Attacking Midfielder"}}
                ],
                "stats": {
                    "goals": 7,
                    "assists": 6,
                    "passing": 82.1,
                    "progressivePasses": 10.8
                },
                "nationality": {"name": "Spain"},
                "foot": "left"
            }
        }

def get_player_database_by_id() -> Dict[str, Any]:
    """Get the player database by ID"""
    try:
        return load_json('db_by_id.json')
    except FileNotFoundError:
        # Return mock data for testing
        return {
            "123456": {
                "wyId": "123456",
                "name": "João Silva",
                "age": 25,
                "height": 180,
                "weight": 75,
                "positions": [
                    {"position": {"code": "cmf", "name": "Central Midfielder"}}
                ],
                "stats": {
                    "goals": 5,
                    "assists": 8,
                    "passing": 85.5,
                    "progressivePasses": 12.3
                },
                "nationality": {"name": "Brazil"},
                "foot": "right"
            },
            "789012": {
                "wyId": "789012",
                "name": "Carlos Mendez",
                "age": 24,
                "height": 178,
                "weight": 72,
                "positions": [
                    {"position": {"code": "cmf", "name": "Central Midfielder"}},
                    {"position": {"code": "amf", "name": "Attacking Midfielder"}}
                ],
                "stats": {
                    "goals": 7,
                    "assists": 6,
                    "passing": 82.1,
                    "progressivePasses": 10.8
                },
                "nationality": {"name": "Spain"},
                "foot": "left"
            }
        }

def get_average_statistics() -> Dict[str, Any]:
    """Get average statistics by position"""
    try:
        return load_json('average_statistics_by_position.json')
    except FileNotFoundError:
        # Return mock data for testing
        return {
            "cmf": {
                "goals": 3,
                "assists": 5,
                "passing": 78,
                "progressivePasses": 8
            },
            "amf": {
                "goals": 6,
                "assists": 7,
                "passing": 75,
                "progressivePasses": 9
            }
        }

def get_weights_dictionary() -> Dict[str, Any]:
    """Get weights dictionary for scoring"""
    try:
        return load_json('weights_dict.json')
    except FileNotFoundError:
        # Return mock data for testing
        return {
            "cmf": {
                "goals": 0.5,
                "assists": 0.7,
                "passing": 0.9,
                "progressivePasses": 0.8
            },
            "amf": {
                "goals": 0.8,
                "assists": 0.9,
                "passing": 0.7,
                "progressivePasses": 0.6
            }
        }

def get_team_names() -> Dict[str, Any]:
    """Get team names dictionary"""
    try:
        return load_json('team.json')
    except FileNotFoundError:
        # Return mock data for testing
        return {
            "1": {"name": "Barcelona", "country": "Spain"},
            "2": {"name": "Real Madrid", "country": "Spain"},
            "3": {"name": "Manchester United", "country": "England"}
        }

def find_player_by_id(player_id: str) -> Optional[Dict[str, Any]]:
    """
    Find a player by ID in the database
    
    Args:
        player_id: The player ID to find
        
    Returns:
        The player data or None if not found
    """
    db_by_id = get_player_database_by_id()
    player_id_str = str(player_id)
    
    if player_id_str in db_by_id:
        return db_by_id[player_id_str]
    return None

def find_player_by_name(player_name: str) -> Optional[Dict[str, Any]]:
    """
    Find a player by name in the database
    
    Args:
        player_name: The player name to find
        
    Returns:
        The player data or None if not found
    """
    db = get_player_database()
    
    # Case-insensitive search
    player_name_lower = player_name.lower()
    
    for name, data in db.items():
        if name.lower() == player_name_lower:
            return data
    
    # Try a more flexible search if exact match not found
    for name, data in db.items():
        if player_name_lower in name.lower():
            return data
    
    return None

def get_players_with_position(
    position_code: str, 
    database: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Get all players that can play in the specified position
    
    Args:
        position_code: The position code to filter by
        database: Optional player database (loaded from file if not provided)
        
    Returns:
        List of players that can play in the position
    """
    import unidecode
    
    # Load the database if not provided
    if database is None:
        database = get_player_database()
    
    players_list = []
    
    for player_name, player_data in database.items():
        if any(pos["position"]["code"] == position_code for pos in player_data.get("positions", [])):
            # Add the player name to the data for easier access
            player_data_copy = player_data.copy()
            player_data_copy["name"] = unidecode.unidecode(player_name)
            players_list.append(player_data_copy)
    
    return players_list

def get_sigma_by_position():
    return load_json('sigma_statistics_by_position.json')


if __name__ == "__main__":
   team = find_club_by_id("3161")
   print(team)