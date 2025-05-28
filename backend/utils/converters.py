from datetime import datetime
from typing import Optional, List, Dict, Any

from backend.models import sql_models # SQLAlchemy models
from backend.models import player as pydantic_models # Pydantic models
from backend.services.data_service import DB_TO_GRANULAR_FALLBACK_MAP 
# For GRANULAR_TO_DB_POSITION_MAP, if needed for reverse mapping, or a more comprehensive position map.
# from backend.config import POSITIONS_MAPPING # If a map like {'cb': "Center Back"} is needed for PlayerPosition.name

from sqlalchemy.orm import Session # Keep for type hinting, even if not used directly in functions yet

def _calculate_age(birth_timestamp: Optional[int]) -> Optional[int]:
    if not birth_timestamp:
        return None
    try:
        birth_date = datetime.fromtimestamp(birth_timestamp)
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except Exception as e:
        print(f"Error calculating age: {e}") # It's good to log errors
        return None

def _format_timestamp_to_date_str(timestamp: Optional[int]) -> Optional[str]:
    if not timestamp:
        return None
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Error formatting timestamp: {e}") # Log errors
        return None

def convert_player_model_to_pydantic_detailed(
    player_sql: sql_models.Player,
    # db: Session # Uncomment if session is needed for lazy loading or complex queries
) -> pydantic_models.Player:
    """
    Converts a SQLAlchemy Player model instance to a Pydantic Player (detailed) model instance.
    Assumes player_sql object has necessary relationships (like country) eager-loaded if needed.
    """
    
    granular_position_code = DB_TO_GRANULAR_FALLBACK_MAP.get(player_sql.position, player_sql.position)
    # For PlayerPosition.name, a mapping from granular_code (e.g. 'cb') to full name (e.g. 'Center Back') would be ideal.
    # Using granular_position_code as name for now if a full map (like config.POSITIONS_MAPPING) isn't easily accessible here.
    # Example: position_display_name = POSITIONS_MAPPING.get(granular_position_code, granular_position_code)
    position_display_name = granular_position_code # Simplified: use code as name
    
    pydantic_positions_list = [
        pydantic_models.PlayerPosition(code=granular_position_code, name=position_display_name)
    ]

    # Club Name: Simplified to string. Assumes current team logic is handled before this converter,
    # or this converter focuses only on direct attributes.
    # If player_sql had a `current_team_name` attribute pre-populated by a service:
    # club_name_str = player_sql.current_team_name if hasattr(player_sql, 'current_team_name') else "Unknown Club"
    # For now, using a placeholder as Player model does not have direct current team.
    # This should ideally be resolved by the calling function or service layer providing this data.
    club_name_str = "Unknown Club" # Placeholder
    # If PlayerTeam relationship is loaded and processed:
    # if player_sql.player_teams: 
    #     current_team_rel = next((pt for pt in player_sql.player_teams if pt.is_current), None)
    #     if current_team_rel and current_team_rel.team:
    #         club_name_str = current_team_rel.team.name

    nationality_str = player_sql.country.name if player_sql.country else None

    # Stats are placeholder. Real aggregation is complex.
    player_stats_data = {} 

    return pydantic_models.Player(
        wyId=str(player_sql.id), # Convert int ID to string for Pydantic model
        name=player_sql.name,
        age=_calculate_age(player_sql.date_of_birth_timestamp),
        height=player_sql.height,
        weight=None, # Not available in sql_models.Player
        positions=pydantic_positions_list,
        club=club_name_str, # Pydantic model expects Optional[str]
        contractUntil=_format_timestamp_to_date_str(player_sql.contract_until_timestamp),
        nationality=nationality_str, # Pydantic model expects Optional[str]
        foot=player_sql.preferred_foot,
        stats=player_stats_data, 
    )

def convert_player_model_to_pydantic_summary(
    player_sql: sql_models.Player,
    # db: Session # Uncomment if session is needed
    score: Optional[float] = None,
) -> pydantic_models.PlayerSummary:
    """
    Converts a SQLAlchemy Player model instance to a Pydantic PlayerSummary model instance.
    """
    granular_position_code = DB_TO_GRANULAR_FALLBACK_MAP.get(player_sql.position, player_sql.position)
    
    club_name_str = "Unknown Club" # Placeholder for current club name logic
    # Example if current team logic was applied to player_sql object by caller:
    # if hasattr(player_sql, 'current_team_name'): club_name_str = player_sql.current_team_name
            
    nationality_str = player_sql.country.name if player_sql.country else None

    return pydantic_models.PlayerSummary(
        wyId=str(player_sql.id), 
        name=player_sql.name,
        age=_calculate_age(player_sql.date_of_birth_timestamp),
        height=player_sql.height,
        weight=None, # Not in sql_models.Player
        positions=[granular_position_code], # Pydantic PlayerSummary.positions is List[str]
        club=club_name_str,
        nationality=nationality_str,
        foot=player_sql.preferred_foot,
        stats={}, # Placeholder for key stats summary
        score=score,
        image_url=f"/player-image/{player_sql.id}", 
        detailed_stats=None # Placeholder
    )

# Add other converters if needed, e.g., for Team, Country, etc.
# def convert_team_model_to_pydantic(team_sql: sql_models.Team) -> pydantic_models.TeamPydantic: # Assuming TeamPydantic exists
#     return pydantic_models.TeamPydantic(id=str(team_sql.id), name=team_sql.name, ...)
