"""
Formatting utilities for KatenaScout responses
"""

import json
import os
from typing import List, Dict, Any, Optional, Tuple
from models.response import SearchResponse, ComparisonResponse, ErrorResponse

# Import constants related to player images
from config import PLAYER_IMAGES_DIR

# Helper function to add player image information
def add_player_image_info(player_data):
    """Add image URL and availability information to player data"""
    if 'wyId' in player_data and player_data['wyId']:
        # Convert wyId to string if it's not already
        player_id = str(player_data['wyId'])
        # Set the image URL to the player-image endpoint
        player_data['image_url'] = f"/player-image/{player_id}"
        # Check if image exists locally
        player_data['has_image'] = os.path.exists(os.path.join(PLAYER_IMAGES_DIR, f"{player_id}.png"))
    return player_data

# Satisfaction questions by language
SATISFACTION_QUESTIONS = {
    "english": "Are you satisfied with these players or would you like to refine your search?",
    "portuguese": "Você está satisfeito com esses jogadores ou gostaria de refinar sua busca?",
    "spanish": "¿Estás satisfecho con estos jugadores o te gustaría refinar tu búsqueda?",
    "bulgarian": "Доволни ли сте от тези играчи или бихте искали да прецизирате търсенето си?"
}

def get_satisfaction_question(language: str) -> str:
    """Get language-specific satisfaction question"""
    return SATISFACTION_QUESTIONS.get(language, SATISFACTION_QUESTIONS["english"])

def split_response_and_satisfaction(text: str, language: str) -> tuple:
    """Split response into main content and satisfaction question"""
    # Look for satisfaction question markers in the text
    markers = {
        "english": ["satisfied", "would you like", "refine your search"],
        "portuguese": ["satisfeito", "gostaria de refinar", "refinar sua busca"],
        "spanish": ["satisfecho", "te gustaría", "refinar tu búsqueda"],
        "bulgarian": ["доволни", "прецизирате", "търсенето си"]
    }
    
    selected_markers = markers.get(language, markers["english"])
    
    # Try to find the satisfaction question by looking for markers
    sentences = text.split("\n")
    question_index = -1
    
    for i in range(len(sentences) - 1, -1, -1):
        sentence = sentences[i].lower()
        if any(marker in sentence for marker in selected_markers):
            question_index = i
            break
    
    if question_index >= 0:
        # Split the text
        main_response = "\n".join(sentences[:question_index])
        satisfaction_question = sentences[question_index]
        return main_response, satisfaction_question
    else:
        # If no split found, use the whole text as main response and a default question
        return text, get_satisfaction_question(language)

def process_player_data(player):
    """Process and sanitize player data"""
    if isinstance(player, dict):
        # Simple sanitization without model conversion
        player_copy = player.copy()
        
        # Ensure 'stats' exists and sanitize None values
        if 'stats' not in player_copy or player_copy['stats'] is None:
            player_copy['stats'] = {}
        else:
            # Replace None values with 0.0 in stats
            for stat_key, stat_value in player_copy['stats'].items():
                if stat_value is None:
                    player_copy['stats'][stat_key] = 0.0
        
        # Add image URL and availability information
        player_copy = add_player_image_info(player_copy)
        
        return player_copy
    else:
        # If it's already a model instance, get its dict representation
        try:
            player_dict = player.model_dump()
            return add_player_image_info(player_dict)
        except:
            # Fallback for non-pydantic objects
            fallback = {
                'name': getattr(player, 'name', 'Unknown Player'),
                'stats': getattr(player, 'stats', {})
            }
            return fallback

def format_search_response(
    players: List[Dict[str, Any]], 
    text_response: str, 
    language: str = "english",
    follow_up_suggestions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Format a standardized search response"""
    # Split the response into main content and satisfaction question
    main_response, satisfaction_question = split_response_and_satisfaction(text_response, language)
    
    # Process all players - sanitize data and add image information
    raw_players = [process_player_data(player) for player in players]

    # Store raw players in the response for direct use
    response_data = {
        'success': True,
        'response': main_response,
        'satisfaction_question': satisfaction_question,
        'players': raw_players,  # Use raw players directly
        'language': language
    }
    
    # Add follow-up suggestions if provided
    if follow_up_suggestions:
        response_data['follow_up_suggestions'] = follow_up_suggestions
        
    return response_data

def format_comparison_response(
    players: List[Dict[str, Any]], 
    comparison_text: Optional[str] = None,
    comparison_aspects: Optional[List[str]] = None,
    language: str = "english",
    metric_winners: Optional[Dict[str, str]] = None,
    overall_winner: Optional[Dict[str, Any]] = None,
    categorized_metrics: Optional[Dict[str, List[str]]] = None,
    category_winners: Optional[Dict[str, str]] = None,
    negative_metrics: Optional[List[str]] = None,
    in_chat_comparison: Optional[bool] = False
) -> Dict[str, Any]:
    # Debug information
    print(f"DEBUG - Formatting comparison response with in_chat_comparison={in_chat_comparison}")
    """Format a standardized comparison response"""
    # Process all players - sanitize data and add image information
    raw_players = [process_player_data(player) for player in players]
    
    # Set defaults for missing parameters
    if metric_winners is None:
        metric_winners = {}
    if overall_winner is None:
        overall_winner = {"winner": "tie", "player1_score": 0, "player2_score": 0}
    if categorized_metrics is None:
        categorized_metrics = {}
    if category_winners is None:
        category_winners = {}
    if negative_metrics is None:
        negative_metrics = []
    
    # Store raw players in the response for direct use
    response_data = {
        'success': True,
        'comparison': comparison_text,
        'comparison_aspects': comparison_aspects or [],
        'players': raw_players,  # Use raw players directly
        'language': language,
        'metric_winners': metric_winners,
        'overall_winner': overall_winner,
        'categorized_metrics': categorized_metrics,
        'category_winners': category_winners,
        'negative_metrics': negative_metrics,
        'in_chat_comparison': in_chat_comparison  # Add the in_chat_comparison flag
    }
    
    return response_data

def format_error_response(
    error: str, 
    message: str, 
    language: str = "english"
) -> Dict[str, Any]:
    """Format a standardized error response"""
    response = ErrorResponse(
        success=False,
        error=error,
        message=message,
        language=language
    )
    
    # Convert to dict for jsonify
    return response.model_dump()