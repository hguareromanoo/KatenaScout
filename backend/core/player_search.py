"""
Player search functionality for KatenaScout

This module provides the core functionality for searching players based on parameters.
All player search operations should use the functions in this module to ensure consistency.
"""

from typing import List, Dict, Any, Optional
import os
import json
from datetime import datetime
import unidecode
from models.parameters import SearchParameters
from config import MIN_SCORE_THRESHOLD, DEFAULT_SEARCH_LIMIT
from services.data_service import (
    # get_player_database, # Removed
    # get_player_database_by_id, # Removed
    get_weights_dictionary, # Kept for now, uses load_json
    get_average_statistics, # Now uses DB
    get_players_with_position as get_players_with_position_service, # Renamed to avoid conflict
    find_player_by_id as find_player_by_id_service, # Renamed
    find_player_by_name as find_player_by_name_service, # Renamed
    DB_TO_GRANULAR_FALLBACK_MAP, # Import for position display
    GRANULAR_TO_DB_POSITION_MAP # Import for querying by position
)
from backend.models.sql_models import Player as PlayerModel, Team as TeamModel, Country as CountryModel
from sqlalchemy.orm import Session

def get_date_months_from_now(months):
    """
    Calcula uma data X meses a partir de hoje, lidando com bordas de mês
    
    Args:
        months: Número de meses a adicionar
        
    Returns:
        Data formatada como string YYYY-MM-DD
    """
    today = datetime.now()
    # Adicionar os meses ajustando o ano se necessário
    month = today.month + months
    year = today.year
    
    # Ajustar ano se month > 12
    if month > 12:
        year += month // 12
        month = month % 12
        # Se month ficou 0, deve ser dezembro do ano anterior
        if month == 0:
            month = 12
            year -= 1
            
    # Lidar com dias inválidos (ex: 31 de janeiro + 6 meses seria 31 de julho, mas não existe)
    # Vamos pegar o último dia válido do mês resultante
    last_day_of_month = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 
                        31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Garantir que o dia não exceda o último dia do mês
    day = min(today.day, last_day_of_month[month-1])
    
    # Criar data e formatar
    target_date = datetime(year, month, day)
    return target_date.strftime("%Y-%m-%d")

def search_players(
    params: SearchParameters,
    limit: int = DEFAULT_SEARCH_LIMIT,
    db: Session, # Added db session
    limit: int = DEFAULT_SEARCH_LIMIT,
    # database, database_id removed as they are no longer sources of truth for player data
    weights_dict: Optional[Dict[str, Any]] = None, # Renamed for clarity
    avg_stats_by_pos: Optional[Dict[str, Any]] = None # Renamed for clarity
) -> List[Dict[str, Any]]: # Return type is List of Dicts (formatted player info)
    """
    Search for players based on the given parameters and return the top matches.
    Uses SQLAlchemy for database interaction.
    
    Args:
        db: SQLAlchemy Session object.
        params: The search parameters - primary input for search logic.
        limit: Maximum number of players to return.
        weights_dict: Optional weights dictionary for scoring.
        avg_stats_by_pos: Optional average statistics by position (DB position char keys).
            
    Returns:
        A list of the top N players matching the parameters, formatted as dictionaries.
    """
    if weights_dict is None:
        weights_dict = get_weights_dictionary() # Still loads from JSON for now
    
    if avg_stats_by_pos is None:
        avg_stats_by_pos = get_average_statistics(db=db) # Now from DB
    
    # Special case: Handle name-based search using find_player_by_name_service
    if params.is_name_search and params.player_name:
        print(f"\n=== NAME-BASED SEARCH (SQLAlchemy) ===")
        print(f"Looking for player by name: {params.player_name}")
        
        # find_player_by_name_service returns a single PlayerModel or None
        # This route was designed for multiple results. We need a list.
        # This implies a new service function like search_players_by_name_like might be better.
        # For now, use a direct query for multiple results.
        from sqlalchemy import func as sql_alchemy_func_search # Alias to avoid conflict
        name_query_lower = params.player_name.lower()
        player_results_db = db.query(PlayerModel).filter(
            sql_alchemy_func_search.lower(PlayerModel.name).contains(name_query_lower)
        ).limit(limit).all()

        results = []
        for player_obj in player_results_db:
            player_info = get_player_info(player_id_int=player_obj.id, db=db, params=None) # Pass int ID
            if player_info and not player_info.get('error'):
                results.append(player_info)
        
        print(f"Found {len(results)} players by name search.")
        return results # Already limited by query
    
    # Normal parameter-based search
    active_params = params.get_true_parameters()
    scoring_params = [p for p in active_params if p not in ["key_description_word", "position_codes", "age", "height", "weight", "player_name", "is_name_search", "foot", "contract_expiration"]]
    print(f"\n=== SEARCH PARAMETERS ===")
    print(f"Positions: {params.position_codes}")
    print(f"Description: {params.key_description_word}")
    if params.foot and params.foot != "both":
        print(f"Preferred foot: {params.foot}")
    
    six_months_from_now = None
    if params.contract_expiration:
        six_months_from_now = get_date_months_from_now(6)
        print(f"Contract expiration: {six_months_from_now}")
    print(f"Statistical params for scoring ({len(scoring_params)}): {scoring_params}")
    print(f"=========================\n")
    
    players_score: Dict[int, Dict[str, Any]] = {} # Keyed by player ID (int)
    
    # Search for players in each of the specified granular position_codes
    for granular_pos_code in params.position_codes:
        # get_players_with_position_service expects a granular code and db session
        # It uses GRANULAR_TO_DB_POSITION_MAP internally.
        player_obj_list = get_players_with_position_service(position_code=granular_pos_code, db=db)
        
        for player_obj in player_obj_list: # player_obj is now a PlayerModel instance
            # Filter by preferred foot
            if params.foot and params.foot != "both":
                if player_obj.preferred_foot and player_obj.preferred_foot.lower() != params.foot.lower():
                    continue
            
            # Filter by contract expiration (using player_obj.contract_until_timestamp (BIGINT))
            if params.contract_expiration and six_months_from_now:
                # Assuming contract_until_timestamp stores Unix timestamp.
                # And six_months_from_now is "YYYY-MM-DD". Convert for comparison.
                # This part needs careful handling of date formats and timestamps.
                # For simplicity, if player_obj.contract_until_timestamp is directly comparable or pre-converted, use it.
                # If contract_until_timestamp is significantly later than six_months_from_now, skip.
                # This is a placeholder for actual timestamp comparison logic.
                # Example: if player_obj.contract_until_timestamp > datetime.strptime(six_months_from_now, "%Y-%m-%d").timestamp(): continue
                pass # Placeholder for contract filtering logic

            # Calculate score for this player in this position
            # get_score needs to be adapted for PlayerModel instance and new avg_stats_by_pos structure
            score = get_score(player_obj, params, granular_pos_code, weights_dict, avg_stats_by_pos, db)
            
            if player_obj.id not in players_score or score > players_score[player_obj.id]['score']:
                players_score[player_obj.id] = {
                    'player_model': player_obj, # Store the model instance
                    'score': score,
                    'matched_granular_position': granular_pos_code 
                }
    
    sorted_scores = sorted(players_score.items(), key=lambda x: x[1]['score'], reverse=True)[:limit]
    
    selected_players = []
    for player_id_int, data in sorted_scores:
        player_info = get_player_info(
            player_id_int=player_id_int, 
            db=db, 
            params=params, # Pass params for focused stats if needed by get_player_info
            # weights_dict and avg_stats_by_pos are not directly used by get_player_info for formatting
            # but could be if get_player_info also calculates a score or relative metrics.
        )
        
        if player_info and not player_info.get('error'):
            player_info['score'] = round(data['score'], 2)
            player_info['matched_granular_position'] = data['matched_granular_position'] # Add matched position
            selected_players.append(player_info)
        else:
            print(f"Warning: Could not retrieve info for player ID: {player_id_int}. Error: {player_info.get('error') if player_info else 'Player info is None'}")
    
    print(f"Found {len(selected_players)} players matching the search criteria.")
    # ... (logging remains similar) ...
    return selected_players

# Removed local get_players_with_position as service one should be used.

def get_score(
    player_obj: PlayerModel, 
    params: SearchParameters, 
    granular_pos_code: str,  # Granular position code from params
    weights_dict: Dict[str, Any], 
    avg_stats_by_pos: Dict[str, Any], # DB position char keys
    db: Session # Added db session, though not directly used in this simplified scoring
) -> float:
    """
    Calculate a weighted score for how well a player matches the search parameters.
    This function needs significant adaptation to work with PlayerModel and new stats structure.
    Current version is a simplification focusing on structure change.
    
    Args:
        player_obj: SQLAlchemy PlayerModel instance.
        params: Search parameters.
        granular_pos_code: Granular position code (e.g., 'cmf', 'cb').
        weights_dict: Weights dictionary (keys are granular positions).
        avg_stats_by_pos: Average statistics (keys are DB general positions 'G','D','M','F').
        db: SQLAlchemy Session object.
        
    Returns:
        A numerical score.
    """
    score = 0.0
    player_name = player_obj.name
    
    # Determine DB general position for fetching average stats
    db_pos_char = GRANULAR_TO_DB_POSITION_MAP.get(granular_pos_code, None)
    if not db_pos_char: # Should not happen if granular_pos_code is validated before
        return 0.0 

    # Get average statistics for the player's general DB position
    # avg_stats_by_pos has keys 'G', 'D', 'M', 'F'
    # The values are dicts like {'rating': 7.0, 'goals': 0.2, ...}
    avg_for_gen_pos = avg_stats_by_pos.get(db_pos_char, {})

    # Get position-specific weights from weights_dict (still uses granular codes)
    # weights_dict structure: {'cmf': {'key_description': {'goals': 0.8, ...}}}
    position_weights = {}
    if granular_pos_code in weights_dict:
        # params.key_description_word is a list of strings
        for key_desc_word in params.key_description_word:
            if key_desc_word in weights_dict[granular_pos_code]:
                position_weights.update(weights_dict[granular_pos_code][key_desc_word])
    
    # This part is highly complex due to the old structure player["total"]["metric"]
    # PlayerModel does not have 'total', 'average', 'percent' dicts.
    # Player statistics are now in PlayerStatistic model, per match.
    # A full refactor of scoring would require querying PlayerStatistic for the player,
    # aggregating them (e.g., per 90 min values), then comparing to averages.
    # This is beyond simple attribute access change.
    # For now, let's assume a very simplified scoring based on available PlayerModel attributes
    # or make it a placeholder.

    # Placeholder: if 'goals' is a weighted parameter, and player_obj had direct 'goals_total'
    # if 'goals' in position_weights and hasattr(player_obj, 'goals_total_season'): # Fictional attribute
    #     player_value = player_obj.goals_total_season
    #     avg_value = avg_for_gen_pos.get('goals', 1) # Default to 1 to avoid div by zero
    #     if avg_value > 0:
    #         score += (player_value / avg_value) * position_weights['goals']

    # Example: Age scoring (if age is in params)
    if params.age_min is not None and player_obj.date_of_birth_timestamp:
        # Simplified age calculation (example, not accurate)
        # Convert timestamp to age, then compare.
        # For now, just add a small score if it's a parameter.
        if 'age' in position_weights: # Assuming 'age' could be a key in weights
             score += 0.5 * position_weights.get('age', 1.0)


    # This function needs a complete rewrite based on how PlayerStatistics will be aggregated
    # and compared. For now, returning a dummy score if any relevant params exist.
    if position_weights: # If any relevant weights were found for the position/description
        score += 1.0 # Dummy score contribution

    if score > 0:
        print(f"Player {player_name} in position {granular_pos_code} scored: {score:.2f} (Simplified)")
            
    return score


def get_player_info(
    player_id_int: int, # Changed to int
    db: Session, 
    params: Optional[SearchParameters] = None,
    # database, database_id, weights, average_stats removed from direct args
    # weights and average_stats might be needed if scoring is part of get_player_info
) -> Dict[str, Any]:
    """
    Get detailed player information formatted for display using SQLAlchemy.
    
    Args:
        player_id_int: The integer player ID to retrieve.
        db: SQLAlchemy Session object.
        params: Optional search parameters (currently not used for stat filtering here).
        
    Returns:
        A dictionary with the player's details.
    """
    player_obj = find_player_by_id_service(player_id=player_id_int, db=db)

    if not player_obj:
        return {"error": f"Player not found with ID: {player_id_int}"}

    # Get granular position for display
    display_position = DB_TO_GRANULAR_FALLBACK_MAP.get(player_obj.position, player_obj.position)

    # Club Name: Requires current team logic. PlayerTeam relationship.
    # Placeholder for current team logic:
    current_team_name = "Unknown Team"
    # Example: if player_obj.player_teams and player_obj.player_teams[0].team:
    #    current_team_name = player_obj.player_teams[0].team.name
    # This assumes player_teams is ordered by recency or has an is_current flag.

    # Contract Expiration: from player_obj.contract_until_timestamp (BIGINT)
    # Convert timestamp to human-readable date string if needed.
    contract_str = "Unknown"
    if player_obj.contract_until_timestamp:
        try:
            contract_str = datetime.fromtimestamp(player_obj.contract_until_timestamp).strftime('%Y-%m-%d')
        except Exception: # Handle potential errors with timestamp
            pass 

    # Nationality
    nationality_name = player_obj.country.name if player_obj.country else "Unknown"

    player_info_dict = {
        "id": player_obj.id, # Use the integer ID from DB
        "wyId": player_obj.id, # Assuming wyId is the same as DB id for now.
        "name": player_obj.name,
        "age": None, # Age needs calculation from date_of_birth_timestamp
        "height": player_obj.height,
        "weight": None, # Weight is not in Player model
        "positions": [display_position], # Simplified to a list with one primary position
        "club": current_team_name,
        "contractUntil": contract_str,
        "nationality": nationality_name,
        "foot": player_obj.preferred_foot,
        "stats": {}, # Placeholder: Detailed stats aggregation is complex
        "complete_profile": { # Placeholder
            "stats": {},
            "position_averages": {}
        }
    }
    
    # Age calculation from date_of_birth_timestamp
    if player_obj.date_of_birth_timestamp:
        try:
            birth_date = datetime.fromtimestamp(player_obj.date_of_birth_timestamp)
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            player_info_dict["age"] = age
        except Exception as e:
            print(f"Could not calculate age for player {player_obj.id}: {e}")


    # The 'stats' and 'complete_profile' part is complex.
    # The old code assumed player JSON objects had 'total', 'average', 'percent' sub-dictionaries.
    # With SQLAlchemy, stats are in PlayerStatistic (per match).
    # Aggregating these into a profile requires significant new logic:
    # 1. Query all PlayerStatistic for this player_id.
    # 2. Aggregate them (e.g., sum totals, calculate overall averages, per-90s).
    # 3. This might be a new function in data_service.py e.g., get_player_aggregated_stats(player_id, db).
    # For now, these will be empty or minimal.

    # If params are provided, old code filtered stats. This logic is deferred.
    # If scoring within get_player_info is needed, it would also go here,
    # using the main get_score function.

    return player_info_dict
    



