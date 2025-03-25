"""
Intent-specific handlers for KatenaScout

This module contains handlers for different user intents.
"""

from typing import Dict, List, Any, Optional
import json
from core.session import SessionData
from core.intent import generate_follow_up_suggestions
from core.comparison import compare_players, find_players_for_comparison
from config import SUPPORTED_LANGUAGES

# Language-specific prompts for response generation
def get_language_specific_prompt(language: str) -> str:
    """Get language-specific system prompt for response generation"""
    prompts = {
        "english": """You are a knowledgeable football scout assistant who presents scouting results in English.
            Process the list of players with their stats and present them in an engaging, professional way.
            Your audience are coaches looking for players with specific characteristics.
            Provide context about players' playing style and highlight standout stats.
            Present all given statistic fields for all players.
            Begin by acknowledging what the person was looking for and present findings in an exciting, natural way.""",
            
        "portuguese": """Você é um assistente apaixonado de scout de futebol que apresenta resultados de pesquisa em Português.
            Processar a lista de jogadores com suas estatísticas e apresentá-los de forma envolvente e natural.
            Seu público são técnicos que buscam jogadores com características específicas.
            Fornecer contexto sobre o estilo de jogo dos jogadores e destacar estatísticas impressionantes.
            Apresentar todos os campos estatísticos fornecidos para todos os jogadores.
            Comece reconhecendo o que a pessoa estava procurando e apresente os resultados de forma empolgante e natural.""",
            
        "spanish": """Eres un apasionado asistente de scout de fútbol que presenta resultados de búsqueda en Español.
            Procesar la lista de jugadores con sus estadísticas y presentarlos de manera atractiva y natural.
            Tu audiencia son entrenadores que buscan jugadores con características específicas.
            Proporcionar contexto sobre el estilo de juego de los jugadores y destacar estadísticas sobresalientes.
            Presentar todos los campos estadísticos proporcionados para todos los jugadores.
            Comienza reconociendo lo que la persona estaba buscando y presenta los resultados de manera emocionante y natural.""",
            
        "bulgarian": """Вие сте страстен футболен скаут асистент, който представя резултати от търсене на български.
            Обработете списъка с играчи с техните статистики и ги представете по ангажиращ и естествен начин.
            Вашата аудитория са треньори, които търсят играчи със специфични характеристики.
            Предоставяйте контекст за стила на игра на играчите и подчертавайте изключителни статистики.
            Представете всички предоставени статистически полета за всички играчи.
            Започнете с признаване на това, което човекът е търсил и представете резултатите по вълнуващ и естествен начин."""
    }
    
    return prompts.get(language, prompts["english"])

def clean_players_for_claude(players):
    """
    Remove complete_profile data from players before sending to Claude
    to avoid token overflow.
    
    Args:
        players: List of player objects
        
    Returns:
        Cleaned list of player objects
    """
    # Create a deep copy to avoid modifying the original data
    import copy
    cleaned_players = copy.deepcopy(players)
    
    for player in cleaned_players:
        # Remove complete_profile key if present
        if "complete_profile" in player:
            del player["complete_profile"]
            
    return cleaned_players

def handle_player_search(session: SessionData, message: str, session_manager) -> Dict[str, Any]:
    """
    Handle player search intent
    
    Args:
        session: The session data
        message: The user message
        session_manager: The session manager
        
    Returns:
        Response data
    """
    try:
        # Simple validation for extremely short messages that might be misclassified
        # Only redirect very short messages (1-2 words)
        if len(message.split()) < 3:
            print(f"Very short message '{message}' in player_search handler. Redirecting to casual_chat.")
            from core.handlers import handle_casual_chat
            return handle_casual_chat(session, message, session_manager)
        
        # For follow-up queries, ensure proper session state
        if session.is_follow_up:
            # If user wasn't satisfied with previous results, this helps with query refinement
            if session.satisfaction is False:
                print(f"User wasn't satisfied with previous results")
            
            print(f"Handling follow-up query")
        else:
            # New search - reset satisfaction
            session.satisfaction = None
            print(f"Handling new search query")
        
        # Extract search parameters (single source of truth)
        print(f"DEBUG - Attempting to extract parameters from: {message}")
        try:
            params = session_manager.get_parameters(session.session_id, message)
            print(f"DEBUG - Successfully extracted parameters: {params}")
        except ValueError as e:
            print(f"Error extracting parameters: {str(e)}")
            return {
                "type": "text",
                "text": "I couldn't understand your search request. Could you try describing the players you're looking for in more detail?"
            }
        
        # Store parameters in session
        session.search_params = params.model_dump()
        session.last_search_params = params.model_dump()
        
        # Search for players
        print(f"DEBUG - About to search with params: {params}")
        players = session_manager.search_players(params)
        print(f"DEBUG - Search returned players of type: {type(players)}")
        print(f"DEBUG - Players value: {players}")
        
        # Validate the players return value
        if not isinstance(players, list):
            raise TypeError(f"Expected list of players but got {type(players)}")
        
        # Update session with players found
        if players:
            print(f"DEBUG - Updating session.selected_players with players")
            session.selected_players = players
        
        # Generate follow-up suggestions
        print(f"DEBUG - About to call generate_follow_up_suggestions")
        suggestions = generate_follow_up_suggestions(session, players)
        
        # Generate natural language response
        system_prompt = get_language_specific_prompt(session.language)
        
        try:
            # Clean players data before sending to Claude to avoid token overflow
            # We remove the complete_profile from players for the LLM
            # but keep it in the response to the frontend
            cleaned_players = clean_players_for_claude(players)
            
            # Create conversational response
            claude_response = session_manager.call_claude_api(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"User's search query: {message}"},
                    {"role": "user", "content": f"Players found: {json.dumps(cleaned_players)}"}
                ]
            )
            
            text_response = claude_response.content[0].text
            
            # Add response to session history
            session.messages.append({"role": "assistant", "content": text_response})
            
            # Return the response data
            return {
                "type": "search_results",
                "players": players,
                "text": text_response,
                "follow_up_suggestions": suggestions
            }
        except Exception as e:
            print(f"Error generating natural language response: {str(e)}")
            
            # Fallback to simple response
            fallback_response = f"Found {len(players)} players matching your criteria.\n\n"
            
            for player in players:
                name = player.get('name', 'Unknown')
                positions = ', '.join(player.get('positions', ['Unknown']))
                score = player.get('score', 0)
                fallback_response += f"- {name} ({positions}) - Score: {score}\n"
            
            # Add response to session history
            session.messages.append({"role": "assistant", "content": fallback_response})
            
            return {
                "type": "search_results",
                "players": players,
                "text": fallback_response,
                "follow_up_suggestions": suggestions
            }
    except Exception as e:
        print(f"Error in handle_player_search: {str(e)}")
        # Return error response
        return {
            "type": "error",
            "message": f"Error searching for players: {str(e)}"
        }

def handle_player_comparison(session: SessionData, message: str, session_manager) -> Dict[str, Any]:
    """
    Handle player comparison intent
    
    Args:
        session: The session data
        message: The user message
        session_manager: The session manager
        
    Returns:
        Response data
    """
    try:
        # Get the players to compare from entities
        if hasattr(session, "entities") and "players_to_compare" in session.entities:
            player_names = session.entities["players_to_compare"]
            
            # If specific players were mentioned
            if player_names:
                # Find these players by their names
                players = find_players_for_comparison(
                    session_manager,
                    session.session_id,
                    player_names,  # pass player names as identifiers
                    session.language
                )
            # Otherwise, check if it's a "top N" comparison
            elif hasattr(session, "entities") and session.entities.get("compare_top_n", False):
                top_n = session.entities.get("top_n", 2)
                
                # Use the top N players from the last search
                if session.selected_players:
                    players = session.selected_players[:top_n]
                else:
                    return {
                        "type": "error",
                        "message": "No players available for comparison. Please search for players first."
                    }
            else:
                # If no specific players mentioned and not a "top N" request
                return {
                    "type": "error", 
                    "message": "Please specify which players you'd like to compare."
                }
        else:
            # No entities detected, use top 2 from recent search
            if session.selected_players and len(session.selected_players) >= 2:
                players = session.selected_players[:2]
            else:
                return {
                    "type": "error",
                    "message": "No players to compare. Please search for players first or specify which players to compare."
                }
        
        # Ensure we have at least 2 players to compare
        if len(players) < 2:
            return {
                "type": "error",
                "message": "At least two players are needed for comparison."
            }
        
        # Generate the comparison
        comparison_result = compare_players(
            players=players,
            session_manager=session_manager,
            language=session.language
        )
        
        # Add comparison to session history
        session.messages.append({
            "role": "assistant", 
            "content": comparison_result["comparison"]
        })
        
        # Return the comparison data
        return {
            "type": "player_comparison",
            "players": players,
            "text": comparison_result["comparison"],
            "comparison_aspects": comparison_result["comparison_aspects"]
        }
    except Exception as e:
        print(f"Error in handle_player_comparison: {str(e)}")
        return {
            "type": "error",
            "message": f"Error comparing players: {str(e)}"
        }

def handle_stats_explanation(session: SessionData, message: str, session_manager) -> Dict[str, Any]:
    """
    Handle stats explanation intent
    
    Args:
        session: The session data
        message: The user message
        session_manager: The session manager
        
    Returns:
        Response data
    """
    # Get the stats to explain from entities
    stats = []
    if hasattr(session, "entities") and "stats_to_explain" in session.entities:
        stats = session.entities["stats_to_explain"]
    
    if not stats:
        return {
            "type": "error",
            "message": "No statistics specified for explanation. Please mention which stat you'd like explained."
        }
    
    # Define system prompt for explanations
    system_prompt = f"""You are a football analytics expert explaining football statistics in {session.language}.
    Provide clear, concise explanations of football metrics that are informative but accessible.
    Include context about why each metric is important and how scouts use it to evaluate players."""
    
    try:
        # Generate explanations with Claude
        claude_response = session_manager.call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"Explain these football statistics: {', '.join(stats)}"}
            ]
        )
        
        explanation_text = claude_response.content[0].text
        
        # Create a structured explanations dictionary
        explanations = {}
        
        # Split the explanation by stat (simple approach - in reality would need more robust parsing)
        for stat in stats:
            # Find explanation for this stat in the text
            # This is a simplistic approach - in production would need better parsing
            if stat.lower() in explanation_text.lower():
                # Extract paragraphs containing the stat name
                stat_paragraphs = []
                for paragraph in explanation_text.split("\n\n"):
                    if stat.lower() in paragraph.lower():
                        stat_paragraphs.append(paragraph)
                
                if stat_paragraphs:
                    explanations[stat] = "\n\n".join(stat_paragraphs)
                else:
                    explanations[stat] = f"Explanation for {stat} not found."
            else:
                explanations[stat] = f"Explanation for {stat} not found."
        
        # Add explanation to session history
        session.messages.append({"role": "assistant", "content": explanation_text})
        
        return {
            "type": "stats_explanation",
            "text": explanation_text,
            "explanations": explanations
        }
    except Exception as e:
        print(f"Error in handle_stats_explanation: {str(e)}")
        
        # Fallback explanations
        fallback_explanations = {
            "xg": "Expected Goals (xG) measures the quality of a shot based on several variables and represents the probability that a shot will result in a goal.",
            "progressive passes": "Progressive passes are passes that move the ball significantly closer to the opponent's goal, typically at least 10 meters closer.",
            "defensive duels": "Defensive duels are one-on-one situations where a defender challenges an attacker for the ball.",
            "ball recoveries": "Ball recoveries are instances where a player regains possession of the ball after the opposing team had control."
        }
        
        explanations = {}
        for stat in stats:
            if stat.lower() in fallback_explanations:
                explanations[stat] = fallback_explanations[stat.lower()]
            else:
                explanations[stat] = f"Sorry, I don't have a detailed explanation for {stat} at the moment."
        
        explanation_text = "\n\n".join([f"{stat}: {explanation}" for stat, explanation in explanations.items()])
        
        session.messages.append({"role": "assistant", "content": explanation_text})
        
        return {
            "type": "stats_explanation",
            "text": explanation_text,
            "explanations": explanations
        }

def handle_casual_chat(session: SessionData, message: str, session_manager) -> Dict[str, Any]:
    """
    Handle casual conversation intent
    
    Args:
        session: The session data
        message: The user message
        session_manager: The session manager
        
    Returns:
        Response data
    """
    # Get conversation context
    context = session.messages[-5:] if len(session.messages) >= 5 else session.messages
    
    # Create system prompt based on language
    language = session.language
    
    system_prompt = f"""
    # Katena Scout - Chat Handler
    
    You are Scout, an assistant for Katena, an innovative AI platform for football. Your role is to direct users to Katena's player search system, encouraging them to describe the characteristics of the players they are looking for.
    
    You are the user's first point of contact with Katena and should present the service in a welcoming way, steering the conversation towards using the search system.
    
    ## Your Main Mission
    
    Quickly direct users to use the search system, briefly explaining how it works and encouraging them to describe the players they are looking for in natural language.
    
    ## Your Objectives
    
    1. Give a brief introduction to Katena and MVP Scout.
    2. Encourage users to describe the player profile they are looking for.
    3. Explain simply that the system translates natural descriptions into search parameters.
    4. Keep the conversation focused on using the search system.
    5. Clarify basic questions about how the system works.
    
    ## Behavior and Communication
    
    - **Tone**: Use a friendly and enthusiastic but objective tone.
    - **Style**: Keep messages short and direct.
    - **Proactivity**: Encourage the user to describe what they're looking for to start the search.
    - **Persistence**: Always direct the user to use the search system.
    
    ## Language Instruction
    IMPORTANT: You must respond in {language}. The user is expecting responses in {language}, so all your messages should be in {language}.
    """
    
    try:
        # Call Claude with the conversation context
        response = session_manager.call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=context
        )
        
        # Extract the response text
        response_text = response.content[0].text
        
        # Add the response to session history
        session.messages.append({"role": "assistant", "content": response_text})
        
        return {
            "type": "text",
            "text": response_text
        }
    except Exception as e:
        print(f"Error in handle_casual_chat: {str(e)}")
        
        # Fallback responses if the LLM call fails
        fallbacks = {
            "english": "I'm here to help you find football players. What type of player are you looking for today?",
            "portuguese": "Estou aqui para ajudá-lo a encontrar jogadores de futebol. Que tipo de jogador você está procurando hoje?",
            "spanish": "Estoy aquí para ayudarte a encontrar jugadores de fútbol. ¿Qué tipo de jugador estás buscando hoy?",
            "bulgarian": "Аз съм тук, за да ви помогна да намерите футболисти. Какъв тип играч търсите днес?"
        }
        
        fallback_text = fallbacks.get(language, fallbacks["english"])
        session.messages.append({"role": "assistant", "content": fallback_text})
        
        return {
            "type": "text",
            "text": fallback_text
        }

def handle_fallback(session: SessionData, message: str, session_manager) -> Dict[str, Any]:
    """
    Handle fallback for unrecognized intents
    
    Args:
        session: The session data
        message: The user message
        session_manager: The session manager
        
    Returns:
        Response data
    """
    language = session.language
    
    fallbacks = {
        "english": "I'm not sure I understand what you're looking for. Could you try rephrasing your request? You can ask me to find players with specific characteristics or compare players.",
        "portuguese": "Não tenho certeza se entendi o que você está procurando. Poderia tentar reformular seu pedido? Você pode me pedir para encontrar jogadores com características específicas ou comparar jogadores.",
        "spanish": "No estoy seguro de entender lo que estás buscando. ¿Podrías intentar reformular tu solicitud? Puedes pedirme que encuentre jugadores con características específicas o compare jugadores.",
        "bulgarian": "Не съм сигурен, че разбирам какво търсите. Бихте ли опитали да преформулирате заявката си? Можете да ме помолите да намеря играчи с конкретни характеристики или да сравня играчи."
    }
    
    fallback_text = fallbacks.get(language, fallbacks["english"])
    session.messages.append({"role": "assistant", "content": fallback_text})
    
    return {
        "type": "text",
        "text": fallback_text
    }