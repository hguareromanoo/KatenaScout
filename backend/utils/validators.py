"""
Validation utilities for KatenaScout request inputs
"""

from typing import Dict, Any, Tuple, Optional, List
from config import SUPPORTED_LANGUAGES

def validate_search_request(data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """
    Validate search request data
    
    Args:
        data: Request JSON data
        
    Returns:
        Tuple of (is_valid, error_message, validated_data)
    """
    # Check if required fields are present
    if not data:
        return False, "Request body is missing", {}
    
    if "query" not in data:
        return False, "Query parameter is required", {}
    
    # Initialize validated data with defaults
    validated = {
        "session_id": data.get("session_id", "default"),
        "query": data.get("query", ""),
        "is_follow_up": data.get("is_follow_up", False),
        "satisfaction": data.get("satisfaction"),
        "language": data.get("language", "english")
    }
    
    # Validate query
    if not validated["query"].strip():
        return False, "Query cannot be empty", validated
    
    # Validate language
    if validated["language"] not in SUPPORTED_LANGUAGES:
        validated["language"] = "english"
    
    # Validate satisfaction (must be None, True, or False)
    if validated["satisfaction"] is not None and not isinstance(validated["satisfaction"], bool):
        return False, "Satisfaction must be boolean or null", validated
    
    # Validate is_follow_up
    if not isinstance(validated["is_follow_up"], bool):
        validated["is_follow_up"] = False
    
    return True, None, validated

def validate_comparison_request(data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """
    Validate player comparison request data
    
    Args:
        data: Request JSON data
        
    Returns:
        Tuple of (is_valid, error_message, validated_data)
    """
    # Check if required fields are present
    if not data:
        return False, "Request body is missing", {}
    
    if "player_ids" not in data:
        return False, "player_ids parameter is required", {}
    
    # Initialize validated data with defaults
    validated = {
        "session_id": data.get("session_id", "default"),
        "player_ids": data.get("player_ids", []),
        "language": data.get("language", "english"),
        "include_ai_analysis": data.get("include_ai_analysis", False)
    }
    
    # Validate player_ids
    if not isinstance(validated["player_ids"], list):
        return False, "player_ids must be an array", validated
    
    if len(validated["player_ids"]) < 2:
        return False, "At least two player IDs are required for comparison", validated
    
    # Validate language
    if validated["language"] not in SUPPORTED_LANGUAGES:
        validated["language"] = "english"
    
    # Validate include_ai_analysis
    if not isinstance(validated["include_ai_analysis"], bool):
        validated["include_ai_analysis"] = False
    
    return True, None, validated

def validate_tactical_analysis_request(data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """
    Validate tactical analysis request data
    
    Args:
        data: Request JSON data
        
    Returns:
        Tuple of (is_valid, error_message, validated_data)
    """
    # Check if required fields are present
    if not data:
        return False, "Request body is missing", {}
    
    if "player_ids" not in data:
        return False, "player_ids parameter is required", {}
    
    if "playing_style" not in data:
        return False, "playing_style parameter is required", {}
    
    if "formation" not in data:
        return False, "formation parameter is required", {}
    
    # Initialize validated data with defaults
    validated = {
        "session_id": data.get("session_id", "default"),
        "player_ids": data.get("player_ids", []),
        "players": data.get("players", []),  # Include complete player objects if provided
        "playing_style": data.get("playing_style", "balanced_approach"),
        "formation": data.get("formation", "4-3-3"),
        "original_query": data.get("original_query", "Compare players for tactical fit"),
        "language": data.get("language", "english")
    }
    
    # Validate player_ids
    if not isinstance(validated["player_ids"], list):
        return False, "player_ids must be an array", validated
    
    if len(validated["player_ids"]) != 2:
        return False, "Exactly two player IDs are required for tactical analysis", validated
    
    # Validate language
    if validated["language"] not in SUPPORTED_LANGUAGES:
        validated["language"] = "english"
    
    return True, None, validated

def sanitize_player_id(player_id: str) -> str:
    """
    Sanitize player ID to prevent path traversal and other issues
    
    Args:
        player_id: Raw player ID from request
        
    Returns:
        Sanitized player ID
    """
    # Remove any path separators and parent directory references
    return str(player_id).replace("/", "").replace("\\", "").replace("..", "").replace("%", "")