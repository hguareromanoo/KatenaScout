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
    try:
        # Extract search parameters using existing function
        params = chat_manager.get_parameters(memory.session_id, message)
        
        # Store parameters in memory
        memory.search_params = params.model_dump() if params else {}
        
        # Search for players with existing function
        players = chat_manager.search_players(params)
        
        # Update memory with players found
        if players:
            memory.entities["recent_players"] = [p.get("name", "") for p in players]
            memory.selected_players = players
        
        from .intents import generate_follow_up_suggestions
        
        suggestions = generate_follow_up_suggestions(memory, players)
        
        # Print debug information
        print(f"Found {len(players)} players in search")
        print(f"Generated {len(suggestions)} follow-up suggestions")
        
        return {
            "type": "search_results",
            "players": players,
            "params": params.model_dump() if params else {},
            "follow_up_suggestions": suggestions
        }
    except Exception as e:
        print(f"Error in handle_player_search: {str(e)}")
        # Fallback to empty results
        return {
            "type": "search_results",
            "players": [],
            "params": {},
            "follow_up_suggestions": ["Try a different search query", "Look for players in another position"]
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
    # Basic Stats
    "total_goals": "Total number of goals scored by a player across all competitions, indicating finishing ability and offensive contribution.",
    "total_assists": "Total number of assists provided by a player across all competitions, showing creative contribution to goal-scoring opportunities.",
    "average_shots": "Average number of shot attempts per 90 minutes, indicating a player's involvement in attacking opportunities.",
    "average_shotsOnTarget": "Average number of shots on target per 90 minutes, showing accuracy and quality of shooting attempts.",
    "total_xgShot": "Expected Goals per shot, measuring the quality of shooting opportunities a player takes based on position, angle, and defensive pressure.",
    "total_xgAssist": "Expected Goals from assists, quantifying the quality of chances a player creates for teammates.",
    
    # Passing
    "average_passes": "Average number of passes attempted per 90 minutes, indicating involvement in build-up play and possession.",
    "percent_successfulPasses": "Percentage of passes that successfully reach a teammate, measuring passing accuracy and reliability.",
    "average_forwardPasses": "Average number of forward passes per 90 minutes, showing progressive intent in possession.",
    "average_backPasses": "Average number of backward passes per 90 minutes, often indicating recycling possession or maintaining control.",
    "average_lateralPasses": "Average number of sideways passes per 90 minutes, showing horizontal ball circulation.",
    "average_longPasses": "Average number of long passes (typically >30 meters) per 90 minutes, indicating range of passing and ability to switch play.",
    "average_progressivePasses": "Average number of progressive passes per 90 minutes that move the ball at least 10 meters closer to the opponent's goal, showing attacking intent.",
    "average_passesToFinalThird": "Average number of passes into the final third of the pitch per 90 minutes, demonstrating ability to advance play into dangerous areas.",
    "average_smartPasses": "Average number of creative, high-risk passes that attempt to break defensive lines per 90 minutes.",
    "average_throughPasses": "Average number of passes played between defensive lines that eliminate defenders from the play per 90 minutes.",
    "average_keyPasses": "Average number of passes that directly lead to a shot per 90 minutes, indicating chance creation.",
    "average_crosses": "Average number of crosses delivered from wide areas per 90 minutes, showing wide attacking contribution.",
    
    # Defensive Actions
    "average_defensiveDuels": "Average number of one-on-one defensive challenges per 90 minutes, showing defensive engagement.",
    "average_defensiveDuelsWon": "Average number of successful defensive duels per 90 minutes, indicating effectiveness in defensive challenges.",
    "average_interceptions": "Average number of times a player intercepts opposition passes per 90 minutes, showing anticipation and reading of the game.",
    "average_slidingTackles": "Average number of sliding tackles attempted per 90 minutes, indicating commitment in defensive actions.",
    "total_clearances": "Total number of times a player clears the ball away from danger zones, showing defensive intervention ability.",
    "average_ballRecoveries": "Average number of loose ball recoveries per 90 minutes, demonstrating anticipation and positioning.",
    "average_counterpressingRecoveries": "Average number of ball recoveries within 5 seconds of losing possession per 90 minutes, showing immediate pressure after losing the ball.",
    
    # Duels and Aerials
    "average_aerialDuelsWon": "Average number of successful aerial challenges per 90 minutes, indicating dominance in the air.",
    "average_duelsWon": "Average number of total successful duels (ground and aerial) per 90 minutes, showing overall physical effectiveness.",
    "average_offensiveDuelsWon": "Average number of successful offensive one-on-one situations per 90 minutes, demonstrating ability to beat defenders.",
    "average_looseBallDuelsWon": "Average number of successful challenges for loose balls per 90 minutes, indicating reaction speed and anticipation.",
    
    # Possession
    "average_successfulDribbles": "Average number of successful dribbles past opponents per 90 minutes, showing ball-carrying ability.",
    "average_progressiveRun": "Average number of runs with the ball that advance play at least 10 meters closer to the opponent's goal per 90 minutes.",
    "average_accelerations": "Average number of rapid increases in speed while in possession per 90 minutes, indicating explosive movement with the ball.",
    
    # Risk Metrics
    "average_ballLosses": "Average number of times a player loses possession per 90 minutes, indicating risk in their play.",
    "average_dangerousOwnHalfLosses": "Average number of possessions lost in dangerous areas of their own half per 90 minutes, measuring defensive risk.",
    "average_dangerousOpponentHalfRecoveries": "Average number of ball recoveries in dangerous areas of the opponent's half per 90 minutes, showing high pressing effectiveness.",
    
    # Percent Statistics
    "percent_aerialDuelsWon": "Percentage of aerial duels won, measuring effectiveness in aerial challenges.",
    "percent_defensiveDuelsWon": "Percentage of defensive duels won, indicating defensive one-on-one effectiveness.",
    "percent_dribblesAgainstWon": "Percentage of times a player successfully stops an opponent's dribbling attempt, showing defensive ability against dribblers.",
    "percent_duelsWon": "Percentage of total duels won (ground and aerial), indicating overall physical effectiveness in challenges.",
    "percent_fieldAerialDuelsWon": "Percentage of aerial duels won in open play (excluding set pieces), showing aerial dominance in open play situations.",
    "percent_gkSaves": "Percentage of shots on target that a goalkeeper saves, measuring shot-stopping ability.",
    "percent_gkSuccessfulExits": "Percentage of successful goalkeeper actions outside the penalty area, showing sweeper-keeper effectiveness.",
    "percent_goalConversion": "Percentage of shots that result in goals, indicating finishing efficiency.",
    "percent_offensiveDuelsWon": "Percentage of offensive one-on-one situations won, showing ability to beat defenders consistently.",
    "percent_penaltiesConversion": "Percentage of penalties successfully converted, measuring penalty-taking reliability.",
    "percent_shotsOnTarget": "Percentage of shots that hit the target, indicating shooting accuracy.",
    "percent_successfulCrosses": "Percentage of crosses that successfully reach a teammate, showing quality of delivery from wide areas.",
    "percent_successfulDribbles": "Percentage of dribbling attempts that successfully beat an opponent, measuring dribbling efficiency.",
    "percent_successfulForwardPasses": "Percentage of forward passes that successfully reach a teammate, indicating progressive passing accuracy.",
    "percent_successfulGoalKicks": "Percentage of goal kicks that successfully reach a teammate, showing distribution quality from goal kicks.",
    "percent_successfulKeyPasses": "Percentage of key passes that are successful, measuring the quality of chance creation.",
    "percent_successfulLinkupPlays": "Percentage of successful short combination plays with teammates, indicating ability in tight spaces.",
    "percent_successfulLongPasses": "Percentage of long passes that successfully reach a teammate, showing accuracy in long-range distribution.",
    "percent_successfulPasses": "Percentage of total passes that successfully reach a teammate, measuring overall passing accuracy.",
    "percent_successfulPassesToFinalThird": "Percentage of passes into the final third that successfully reach a teammate, showing quality of attacking distribution.",
    "percent_successfulProgressivePasses": "Percentage of progressive passes that successfully reach a teammate, indicating quality of forward ball progression.",
    "percent_successfulSlidingTackles": "Percentage of sliding tackles that successfully win the ball, measuring tackle effectiveness.",
    "percent_successfulSmartPasses": "Percentage of creative, line-breaking passes that successfully reach a teammate, showing creative passing effectiveness.",
    "percent_successfulThroughPasses": "Percentage of through passes that successfully reach a teammate, measuring effectiveness in penetrating defenses.",
    "percent_successfulVerticalPasses": "Percentage of vertical passes that successfully reach a teammate, showing ability to progress play directly forward."
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