"""
Intent-specific handlers for the KatenaScout conversation orchestrator
"""

from typing import Dict, List, Any
import json
from .models import ConversationMemory


def handle_player_search(memory: ConversationMemory, message: str, chat_manager) -> Dict[str, Any]:
    """
    Handle player search intent
    
    Args:
        memory: The conversation memory
        message: The user message
        chat_manager: The chat session manager
        
    Returns:
        Response data
    """
    # Extract search parameters using existing function
    params = chat_manager.get_parameters(memory.session_id, message)
    
    # Search for players with existing function
    players = chat_manager.search_players(params)
    
    # Update memory with players found
    memory.entities["recent_players"] = [p["name"] for p in players]
    
    from .intents import generate_follow_up_suggestions
    
    return {
        "type": "search_results",
        "players": players,
        "params": params.model_dump(),
        "follow_up_suggestions": generate_follow_up_suggestions(memory, players)
    }


def handle_player_comparison(memory: ConversationMemory, message: str, chat_manager) -> Dict[str, Any]:
    """
    Handle player comparison intent
    
    Args:
        memory: The conversation memory
        message: The user message
        chat_manager: The chat session manager
        
    Returns:
        Response data
    """
    # Get the players to compare from entities
    player_names = memory.entities.get("players_to_compare", [])
    
    # If no players to compare, try to use recent players
    if not player_names and "recent_players" in memory.entities:
        player_names = memory.entities["recent_players"][:2]  # Compare up to 2 recent players
    
    # If still no players, return error
    if not player_names:
        return {
            "type": "error",
            "message": "No players to compare. Please specify which players you'd like to compare."
        }
    
    # Get player details
    players = []
    for name in player_names:
        # Use existing function to get player details
        # This is simplified and may need adaptation to your actual API
        for player_id, player_data in chat_manager.database_id.items():
            if player_data.get("name", "").lower() == name.lower():
                # Use last search parameters for context
                params = memory.search_params
                if params:
                    player_info = chat_manager.get_players_info(player_id, params)
                    players.append(player_info)
                break
    
    return {
        "type": "player_comparison",
        "players": players,
        "comparison_aspects": ["Passing", "Shooting", "Defense", "Physical"]
    }


def handle_stats_explanation(memory: ConversationMemory, message: str, chat_manager) -> Dict[str, Any]:
    """
    Handle stats explanation intent
    
    Args:
        memory: The conversation memory
        message: The user message
        chat_manager: The chat session manager
        
    Returns:
        Response data
    """
    # Get the stats to explain from entities
    stats = memory.entities.get("stats_to_explain", [])
    
    if not stats:
        return {
            "type": "error",
            "message": "No statistics specified for explanation. Please mention which stat you'd like explained."
        }
    
    # For now, we'll use a fixed set of explanations that could be expanded
    explanations = {
        "xg": "Expected Goals (xG) measures the quality of a shot based on several variables and represents the probability that a shot will result in a goal.",
        "progressive passes": "Progressive passes are passes that move the ball significantly closer to the opponent's goal, typically at least 10 meters closer.",
        "defensive duels": "Defensive duels are one-on-one situations where a defender challenges an attacker for the ball.",
        "ball recoveries": "Ball recoveries are instances where a player regains possession of the ball after the opposing team had control."
    }
    
    # Collect explanations for the requested stats
    stat_explanations = {}
    for stat in stats:
        stat_key = stat.lower().replace(" ", "_")
        if stat_key in explanations:
            stat_explanations[stat] = explanations[stat_key]
        else:
            # For unknown stats, we'll need to generate an explanation
            # This would ideally use a more sophisticated approach
            stat_explanations[stat] = f"Sorry, I don't have a detailed explanation for {stat} at the moment."
    
    return {
        "type": "stats_explanation",
        "explanations": stat_explanations
    }


def handle_casual_chat(memory: ConversationMemory, message: str, chat_manager) -> Dict[str, Any]:
    """
    Handle casual conversation intent
    
    Args:
        memory: The conversation memory
        message: The user message
        chat_manager: The chat session manager
        
    Returns:
        Response data
    """
    # Generate a casual response
    language = memory.language
    
    # Simple responses for common casual messages
    greetings = {
        "english": "Hello! I'm KatenaScout, your football scouting assistant. How can I help you today?",
        "portuguese": "Olá! Sou o KatenaScout, seu assistente de scout de futebol. Como posso ajudá-lo hoje?",
        "spanish": "¡Hola! Soy KatenaScout, tu asistente de scouting de fútbol. ¿Cómo puedo ayudarte hoy?",
        "bulgarian": "Здравейте! Аз съм KatenaScout, вашият футболен скаут асистент. Как мога да ви помогна днес?"
    }
    
    thanks = {
        "english": "You're welcome! Feel free to ask if you need anything else about football players.",
        "portuguese": "De nada! Sinta-se à vontade para perguntar se precisar de mais alguma coisa sobre jogadores de futebol.",
        "spanish": "¡De nada! No dudes en preguntar si necesitas algo más sobre jugadores de fútbol.",
        "bulgarian": "Моля! Не се колебайте да питате, ако имате нужда от друга информация за футболисти."
    }
    
    # Check for common patterns
    message_lower = message.lower()
    if any(word in message_lower for word in ["hello", "hi", "hey", "olá", "hola", "здравейте"]):
        response = greetings.get(language, greetings["english"])
    elif any(word in message_lower for word in ["thanks", "thank you", "obrigado", "gracias", "благодаря"]):
        response = thanks.get(language, thanks["english"])
    else:
        # General fallback
        fallbacks = {
            "english": "I'm here to help you find football players. You can ask me to search for specific types of players or get information about their statistics.",
            "portuguese": "Estou aqui para ajudá-lo a encontrar jogadores de futebol. Você pode me pedir para procurar tipos específicos de jogadores ou obter informações sobre suas estatísticas.",
            "spanish": "Estoy aquí para ayudarte a encontrar jugadores de fútbol. Puedes pedirme que busque tipos específicos de jugadores u obtenga información sobre sus estadísticas.",
            "bulgarian": "Тук съм, за да ви помогна да намерите футболисти. Можете да ме помолите да потърся конкретни типове играчи или да получа информация за техните статистики."
        }
        response = fallbacks.get(language, fallbacks["english"])
    
    return {
        "type": "text",
        "text": response
    }


def handle_fallback(memory: ConversationMemory, message: str, chat_manager) -> Dict[str, Any]:
    """
    Handle fallback for unrecognized intents
    
    Args:
        memory: The conversation memory
        message: The user message
        chat_manager: The chat session manager
        
    Returns:
        Response data
    """
    language = memory.language
    
    fallbacks = {
        "english": "I'm not sure I understand what you're looking for. Could you try rephrasing your request? You can ask me to find players with specific characteristics or compare players.",
        "portuguese": "Não tenho certeza se entendi o que você está procurando. Poderia tentar reformular seu pedido? Você pode me pedir para encontrar jogadores com características específicas ou comparar jogadores.",
        "spanish": "No estoy seguro de entender lo que estás buscando. ¿Podrías intentar reformular tu solicitud? Puedes pedirme que encuentre jugadores con características específicas o compare jugadores.",
        "bulgarian": "Не съм сигурен, че разбирам какво търсите. Бихте ли опитали да преформулирате заявката си? Можете да ме помолите да намеря играчи с конкретни характеристики или да сравня играчи."
    }
    
    return {
        "type": "text",
        "text": fallbacks.get(language, fallbacks["english"])
    }