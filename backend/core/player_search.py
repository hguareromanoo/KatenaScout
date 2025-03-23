"""
Player search functionality for KatenaScout

This module provides the core functionality for searching players based on parameters.
All player search operations should use the functions in this module to ensure consistency.
"""

from typing import List, Dict, Any, Optional
import os
import json
import unidecode
from models.parameters import SearchParameters
from config import MIN_SCORE_THRESHOLD, DEFAULT_SEARCH_LIMIT
from services.data_service import (
    get_player_database, 
    get_player_database_by_id,
    get_weights_dictionary,
    get_average_statistics,
    get_players_with_position,
    find_player_by_id,
    find_player_by_name
)

def search_players(
    params: SearchParameters,
    limit: int = DEFAULT_SEARCH_LIMIT,
    database: Optional[Dict[str, Any]] = None,
    database_id: Optional[Dict[str, Any]] = None,
    weights: Optional[Dict[str, Any]] = None,
    average_stats: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Search for players based on the given parameters and return the top matches
    
    Args:
        params: The search parameters - primary input for search logic
        limit: Maximum number of players to return
        database: Optional player database by name (loaded from file if not provided)
        database_id: Optional player database by ID (loaded from file if not provided)
        weights: Optional weights dictionary for scoring (loaded from file if not provided)
        average_stats: Optional average statistics by position (loaded from file if not provided)
            
    Returns:
        A list of the top N players matching the parameters
    """
    # Load required data sources if not provided
    if database is None:
        database = get_player_database()
    
    if database_id is None:
        database_id = get_player_database_by_id()
    
    if weights is None:
        weights = get_weights_dictionary()
    
    if average_stats is None:
        average_stats = get_average_statistics()
    
    # Special case: Handle name-based search
    if params.is_name_search and params.player_name:
        print(f"\n=== NAME-BASED SEARCH ===")
        print(f"Looking for player by name: {params.player_name}")
        print(f"=========================\n")
        
        # First try exact match with database keys
        results = []
        for name, player_data in database.items():
            # Compare names case-insensitive
            if params.player_name.lower() in unidecode.unidecode(name).lower():
                # Create a player info entry
                player_info = get_player_info(
                    player_id=player_data.get('wyId', player_data.get('id', name)),
                    database=database,
                    database_id=database_id,
                    params=None  # Get all available data
                )
                if player_info and not player_info.get('error'):
                    results.append(player_info)
        
        print(f"Found {len(results)} players by name search.")
        return results[:limit]  # Limit the results
    
    # Normal parameter-based search
    # Log important search parameters at the start
    active_params = params.get_true_parameters()
    scoring_params = [p for p in active_params if p not in ["key_description_word", "position_codes", "age", "height", "weight", "player_name", "is_name_search", "foot", "contract_expiration"]]
    print(f"\n=== SEARCH PARAMETERS ===")
    print(f"Positions: {params.position_codes}")
    print(f"Description: {params.key_description_word}")
    if params.foot and params.foot != "both":
        print(f"Preferred foot: {params.foot}")
    if params.contract_expiration:
        print(f"Contract expiration: {params.contract_expiration}")
    print(f"Statistical params for scoring ({len(scoring_params)}): {scoring_params}")
    print(f"=========================\n")
    
    # Keep track of player scores
    players_score = {}
    
    # Search for players in each of the specified positions
    for pos in params.position_codes:
        # Get players for this position from the service - be careful of parameter order
        print(f"DEBUG - Searching for players in position: {pos}")
        # Correct parameter order: position_code first, then database
        players_list = get_players_with_position(position_code=pos, database=database)
        
        for player in players_list:
            # Filter by preferred foot if specified
            if params.foot and params.foot != "both":
                player_foot = player.get('foot', '').lower()
                if player_foot and player_foot != params.foot.lower():
                    continue  # Skip if foot doesn't match
            
            # Filter by contract expiration if specified
            if params.contract_expiration:
                # Try different paths for contract expiration
                contract_until = None
                if player.get("contractUntil"):
                    contract_until = player.get("contractUntil")
                elif player.get("contract") and isinstance(player.get("contract"), dict) and player.get("contract").get("contractExpiration"):
                    contract_until = player.get("contract").get("contractExpiration")
                
                # Skip if contract doesn't expire soon enough
                if not contract_until or contract_until > params.contract_expiration:
                    continue
            
            # Calculate score for this player in this position
            score = get_score(player, params, pos, weights, average_stats)
            
            # Store the player's score
            player_id = player.get('wyId', player.get('id', player.get('name')))
            if player_id not in players_score or score > players_score[player_id]['score']:
                # Keep the player's highest score across all positions
                players_score[player_id] = {
                    'player': player,
                    'score': score,
                    'position': pos
                }
    
    # Sort players by score and take the top N
    sorted_scores = sorted(players_score.items(), key=lambda x: x[1]['score'], reverse=True)[:limit]
    
    # Format the player data for the response
    selected_players = []
    for player_id, data in sorted_scores:
        # Ensure player_id is string to prevent issues
        player_id_str = str(player_id) if not isinstance(player_id, str) else player_id
        
        # Use the standalone function for consistent player info retrieval
        # No need to import as it's in the same file
        player_info = get_player_info(
            player_id=player_id_str, 
            database=database, 
            database_id=database_id, 
            params=params,
            weights=weights,
            average_stats=average_stats
        )
        
        # Check if player_info is not None and doesn't contain an error
        if player_info and not player_info.get('error'):
            player_info['score'] = round(data['score'], 2)  # Round score to 2 decimal places
            selected_players.append(player_info)
        else:
            print(f"Warning: Could not retrieve info for player ID: {player_id_str}. Error: {player_info.get('error') if player_info else 'Player info is None'}")
    
    # Log search results
    print(f"\n=== SEARCH RESULTS ===")
    print(f"Found {len(selected_players)} players matching the search criteria")
    
    # Log top 5 results with scores
    if selected_players:
        print("Top players found:")
        for i, player in enumerate(selected_players[:5], 1):
            print(f"{i}. {player.get('name', 'Unknown')} - Score: {player.get('score', 0)}")
    else:
        print("No players found with non-zero scores")
    print(f"======================\n")
        
    return selected_players


def get_players_with_position(position_code: str, database: Dict[str, Any] = None) -> List[dict]:
    """
    Get all players that can play in the specified position
    
    Args:
        position_code: The position code to search for
        database: The player database
        
    Returns:
        List of players that can play in the specified position
    """
    # Load database if not provided
    if database is None:
        from services.data_service import get_player_database
        database = get_player_database()
    
    # Validate inputs to prevent type errors
    if not isinstance(database, dict):
        print(f"ERROR: database is not a dictionary but {type(database)}")
        return []
    
    # Get players with the specified position
    players_list = []
    for player_name, player_data in database.items():
        if any(pos["position"]["code"] == position_code for pos in player_data.get("positions", [])):
            # Add the player name to the data for easier access
            player_data["name"] = unidecode.unidecode(player_name)
            players_list.append(player_data)
    return players_list


def get_score(player, params: SearchParameters, pos, weights, average_stats):
    """
    Calculate a weighted score for how well a player matches the search parameters
    
    Args:
        player: The player data
        params: The search parameters
        pos: The position to evaluate for
        weights: Dictionary of weights for different positions and attributes
        average_stats: Dictionary of average statistics by position
        
    Returns:
        A numerical score representing how well the player matches the criteria
    """
    # Minimal debug - just print the name of the player we're scoring
    player_name = player.get('name', 'Unknown Player')
    
    score = 0.0
    # Get position-specific weights based on key description words
    position_weights = {}
    
    # Get average statistics for this position
    if pos in average_stats:
        avg = average_stats[pos]
    else:
        # If position not found, use a reasonable default
        avg = average_stats.get('cmf', {})  # Default to central midfielder if available
    
    # Extract weights for this position and description word
    for key in params.key_description_word:
        if pos in weights and key in weights[pos]:
            # Add these weights to our mapping
            position_weights.update(weights[pos][key])
    
    # Get parameters with actual values
    true_params = params.get_true_parameters()
    
    # Calculate score component for each relevant parameter
    for param in true_params:
        # Skip non-metric parameters
        if param in ["key_description_word", "position_codes"]:
            continue
            
        # Default weight if not specified
        weight_multiplier = 1.0
        
        # Extract category and metric from parameter name
        parts = param.split('_', 1)
        if len(parts) != 2:
            continue
            
        category, metric = parts
        param_score = 0.0
        
        try:
            # Handle different parameter types
            if category == "total" and "total" in player:
                # Get player's value for this metric
                player_value = player["total"].get(metric, 0)
                # Get average value for comparison
                avg_value = avg.get("total", {}).get(metric, 1)  # Default to 1 to avoid division by zero
                # Get weight for this metric
                weight_key = f"min_{metric}"
                weight_multiplier = position_weights.get(weight_key, 1.0)
                
                # Calculate normalized score: (player value / average value) * weight
                if avg_value > 0:
                    param_score = (player_value / avg_value) * weight_multiplier
                
            elif category == "average" and "average" in player:
                player_value = player["average"].get(metric, 0)
                avg_value = avg.get("average", {}).get(metric, 1)
                weight_key = f"min_{metric}"
                weight_multiplier = position_weights.get(weight_key, 1.0)
                
                if avg_value > 0:
                    param_score = (player_value / avg_value) * weight_multiplier
                
            elif category == "percent" and "percent" in player:
                player_value = player["percent"].get(metric, 0)
                avg_value = avg.get("percent", {}).get(metric, 1)
                weight_key = f"min_{metric}_percent"
                weight_multiplier = position_weights.get(weight_key, 1.0)
                
                if avg_value > 0:
                    param_score = (player_value / avg_value) * weight_multiplier
            
            # Handle special cases like max parameters (lower is better)
            if param.startswith("max_") and param_score > 0:
                # For max parameters, invert the score (lower values are better)
                param_score = 2.0 - param_score if param_score <= 2.0 else 0.0
            
            # Add parameter score to total
            score += param_score
            
            # Log high-scoring parameters for debugging (only significant contributions)
            if param_score > 1.0:
                print(f"High score for {player_name}: {param}={param_score:.2f}")
            
        except Exception as e:
            print(f"Error calculating score for {param}: {str(e)}")
            continue
    
    # Log players with non-zero scores for debugging
    if score > 0:
        print(f"Player {player_name} in position {pos} scored: {score:.2f}")
            
    return score


def get_player_info(player_id: str, database: dict, database_id: dict, params: Optional[SearchParameters] = None, weights: Optional[dict] = None, average_stats: Optional[dict] = None) -> dict:
    """
    Get detailed player information formatted for display
    
    Args:
        player_id: The player ID to retrieve
        database: Player database dictionary
        database_id: Player database by ID dictionary
        params: Optional search parameters to determine which metrics to include
        weights: Optional weights dictionary for scoring
        average_stats: Optional average statistics by position
        
    Returns:
        A dictionary with the player's details and relevant metrics
    """
    try:
        # Safety check for parameters
        if not database or not database_id:
            return {"error": "Missing database or database_id parameter"}
        
        if not player_id:
            return {"error": "Missing player_id parameter"}
        
        # Ensure player_id is a string
        player_id_str = str(player_id) if not isinstance(player_id, str) else player_id
        
        player = None
        
        # First check if player is in database_id
        if player_id_str in database_id:
            player = database_id[player_id_str]
        else:
            # Try to find by name if ID not found
            for name, p_data in database.items():
                # Convert wyId to string for comparison if it exists
                wy_id = str(p_data.get('wyId')) if p_data.get('wyId') is not None else None
                
                if wy_id == player_id_str or unidecode.unidecode(name).lower() == player_id_str.lower():
                    player = p_data
                    break
            
            # If still not found, return error
            if not player:
                return {"error": f"Player not found with ID: {player_id_str}"}
            
    except Exception as e:
        return {"error": f"Error finding player: {str(e)}"}
    
    # Get the positions the player plays in
    positions = [pos["position"]["code"] for pos in player.get("positions", [])]
    
    # Format basic player info
    # We already have player_id_str from earlier
    
    try:
        # Get club and contract info - handle multiple possible formats
        club_name = "Unknown"
        contract_until = "Unknown"
        
        # Try different paths for club name
        # First, check if club is directly available as an object
        club_obj = player.get("club")
        if isinstance(club_obj, dict) and 'name' in club_obj:
            club_name = club_obj.get('name', 'Unknown')
        else:
            # If no direct club object or it has no name, try to look up by team ID
            team_id = player.get("currentTeamId")
            
            # Use a hardcoded mapping for common team IDs
            # Try multiple file paths to find team.json
            team_names = {}
            team_json_paths = [
                'team.json',  # Current directory
                os.path.join(os.path.dirname(__file__), 'team.json'),  # Same directory as this file
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'team.json'),  # Parent directory
            ]
            
            for path in team_json_paths:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        team_names = json.load(f)
                        break  # Found and loaded the file, exit the loop
                except (FileNotFoundError, IOError):
                    continue
            
            # Convert team_id to string for comparison
            if team_id:
                team_id_str = str(team_id)
                if team_id_str in team_names:
                    club_name = team_names[team_id_str].get('name', 'Unknown')
        
        # Try different paths for contract expiration
        if player.get("contractUntil"):
            contract_until = player.get("contractUntil")
        elif player.get("contract") and isinstance(player.get("contract"), dict) and player.get("contract").get("contractExpiration"):
            contract_until = player.get("contract").get("contractExpiration")
        
        # Get nationality info - try different possible field names
        nationality = None
        for field in ["passportArea", "birthArea", "nationality", "country", "countryOfBirth"]:
            if player.get(field):
                nationality = player.get(field)
                # If nationality is a string, use it directly
                # If it's an object, extract the name property
                if isinstance(nationality, dict):
                    # Use 'name' as first priority, then alpha3code or alpha2code
                    if 'name' in nationality:
                        nationality = nationality['name']
                    elif 'alpha3code' in nationality:
                        nationality = nationality['alpha3code']
                    elif 'alpha2code' in nationality:
                        nationality = nationality['alpha2code']
                break
        
        # Get preferred foot
        foot = player.get("foot", "")  # Default to empty string if not available
        
        # Extract player ID fields with proper fallbacks
        player_wy_id = player.get("wyId")
        
        # Debug output to see what we're working with
        print(f"Player data WyID: {player_wy_id}, type: {type(player_wy_id)}")
        
        player_info = {
            "wyId": player_wy_id,  # Include wyId in the player info
            "name": player.get("name", unidecode.unidecode(player_id_str)),
            "age": player.get("age"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "positions": positions,
            "club": club_name,
            "contractUntil": contract_until,
            "nationality": nationality,
            "foot": foot
        }
        
        # Initialize stats dict
        stats = {}
        
        # Get relevant stats based on search parameters
        if params:
            true_params = params.get_true_parameters()
            # Simplified debug - just count the stats we're going to use
            stats_count = len([p for p in true_params if p not in ["key_description_word", "position_codes", "age", "height", "weight"]])
            
            # Extract only relevant statistics from player data - no extras
            for param in true_params:
                # Skip non-statistical parameters
                if param in ["key_description_word", "position_codes", "age", "height", "weight"]:
                    continue
                
                # Split the parameter name to get the category and metric
                parts = param.split('_', 1)
                if len(parts) != 2:
                    continue
                    
                category, metric = parts
                
                # Extract the value from the appropriate category in player data
                if category == "total" and "total" in player:
                    stats[metric] = player["total"].get(metric)
                elif category == "average" and "average" in player:
                    stats[metric] = player["average"].get(metric)
                elif category == "percent" and "percent" in player:
                    stats[f"{metric}_percent"] = player["percent"].get(metric)
        
        player_info["stats"] = stats
        
        # Calculate player score for each position if params, weights, and average_stats are provided
        if params and weights is not None and average_stats is not None:
            position_scores = {}
            for pos in positions:
                if pos in params.position_codes:
                    position_scores[pos] = get_score(player, params, pos, weights, average_stats)
            
            player_info["position_scores"] = position_scores
        
        # Add a complete_profile with ALL metrics for the player,
        # so the frontend can display them without requiring another API call
        complete_stats = {}
        
        # Extract all available statistics from player data
        for category in ["total", "average", "percent"]:
            if category in player and isinstance(player[category], dict):
                for metric, value in player[category].items():
                    # For percent category, add '_percent' suffix to avoid key collisions
                    if category == "percent":
                        stat_key = f"{metric}_percent"
                    else:
                        stat_key = metric
                    
                    # Don't overwrite existing stats with None values
                    if value is not None or stat_key not in complete_stats:
                        complete_stats[stat_key] = value
        
        # Add position averages for main position (if available)
        position_averages = {}
        primary_position = positions[0] if positions else None
        
        if primary_position and average_stats and primary_position in average_stats:
            for metric, value in average_stats[primary_position].items():
                position_averages[metric] = value
        
        # Add complete profile to player info
        player_info["complete_profile"] = {
            "stats": complete_stats,
            "position_averages": position_averages
        }
        
        return player_info
        
    except Exception as e:
        print(f"Error processing player info: {str(e)}")
        return {"error": f"Error processing player info: {str(e)}"}
    



