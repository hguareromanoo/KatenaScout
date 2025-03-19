"""
Response generation utilities for the KatenaScout conversation orchestrator
"""

from typing import Dict, List, Any, Tuple
import json
from .models import ConversationMemory


def format_natural_language_response(memory: ConversationMemory, 
                                    response_data: Dict[str, Any], 
                                    call_claude_api) -> Tuple[str, str]:
    """
    Format the response data into natural language
    
    Args:
        memory: The conversation memory
        response_data: The response data
        call_claude_api: Function to call Claude API
        
    Returns:
        Tuple of (main_response, satisfaction_question)
    """
    response_type = response_data.get("type", "text")
    
    if response_type == "text":
        # Simple text response, no formatting needed
        return response_data.get("text", ""), ""
    
    elif response_type == "search_results":
        return format_search_results(memory, response_data, call_claude_api)
    
    elif response_type == "player_comparison":
        return format_player_comparison(memory, response_data, call_claude_api)
    
    elif response_type == "stats_explanation":
        return format_stats_explanation(memory, response_data), ""
    
    else:
        # Default format for unknown types
        return str(response_data), ""


def format_search_results(memory: ConversationMemory, 
                         response_data: Dict[str, Any], 
                         call_claude_api) -> Tuple[str, str]:
    """Format search results into natural language"""
    language = memory.language
    players = response_data.get("players", [])
    
    if not players:
        # No players found
        no_players_messages = {
            "english": "No players found matching your criteria.",
            "portuguese": "Nenhum jogador encontrado com esses critérios.",
            "spanish": "No se encontraron jugadores que coincidan con tus criterios.",
            "bulgarian": "Не са намерени играчи, отговарящи на вашите критерии."
        }
        
        satisfaction_questions = {
            "english": "Would you like to try with different parameters?",
            "portuguese": "Gostaria de tentar com parâmetros diferentes?",
            "spanish": "¿Te gustaría probar con parámetros diferentes?",
            "bulgarian": "Бихте ли искали да опитате с различни параметри?"
        }
        
        return (
            no_players_messages.get(language, no_players_messages["english"]),
            satisfaction_questions.get(language, satisfaction_questions["english"])
        )
    
    # Use Claude to generate natural language response
    system_prompt = get_language_specific_prompt(language)
    
    try:
        # Create conversational response
        claude_response = call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"User's intent: {memory.current_intent}"},
                {"role": "user", "content": f"Recent conversation: {json.dumps(memory.messages[-5:])}"},
                {"role": "user", "content": f"Data to respond with: {json.dumps(response_data)}"}
            ]
        )
        
        text_response = claude_response.content[0].text
        
        # Split into main response and satisfaction question
        main_response, satisfaction_question = split_response_and_satisfaction(text_response, language)
        
        return main_response, satisfaction_question
        
    except Exception as e:
        # Fallback response
        fallback_intros = {
            "english": "Here are the players I found for you:",
            "portuguese": "Encontrei estes jogadores para você:",
            "spanish": "He encontrado estos jugadores para ti:",
            "bulgarian": "Намерих тези играчи за вас:"
        }
        
        satisfaction_questions = {
            "english": "Are you satisfied with these players or would you like to refine your search?",
            "portuguese": "Você está satisfeito com esses jogadores ou gostaria de refinar sua busca?",
            "spanish": "¿Estás satisfecho con estos jugadores o te gustaría refinar tu búsqueda?",
            "bulgarian": "Доволни ли сте от тези играчи или бихте искали да прецизирате търсенето си?"
        }
        
        # Provide a fallback response that still shows the players
        fallback_intro = fallback_intros.get(language, fallback_intros["english"])
        satisfaction_question = satisfaction_questions.get(language, satisfaction_questions["english"])
        
        fallback_response = f"{fallback_intro}\n\n"
        
        for player in players:
            name = player.get('name', 'Unknown')
            positions = ', '.join(player.get('positions', ['Unknown']))
            score = player.get('score', 0)
            fallback_response += f"- {name} ({positions}) - Score: {score}\n"
        
        return fallback_response, satisfaction_question


def format_player_comparison(memory: ConversationMemory, 
                            response_data: Dict[str, Any], 
                            call_claude_api) -> Tuple[str, str]:
    """Format player comparison into natural language"""
    language = memory.language
    players = response_data.get("players", [])
    
    if len(players) < 2:
        # Not enough players to compare
        not_enough_players = {
            "english": "I need at least two players to make a comparison.",
            "portuguese": "Preciso de pelo menos dois jogadores para fazer uma comparação.",
            "spanish": "Necesito al menos dos jugadores para hacer una comparación.",
            "bulgarian": "Нужни са ми поне двама играчи, за да направя сравнение."
        }
        
        return not_enough_players.get(language, not_enough_players["english"]), ""
    
    # Use Claude to generate comparison
    system_prompt = """You are a football analyst comparing players. 
    Provide a detailed, fact-based comparison highlighting strengths and weaknesses of each player."""
    
    try:
        claude_response = call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"Compare these players: {json.dumps(players)}"}
            ]
        )
        
        comparison_text = claude_response.content[0].text
        return comparison_text, ""
        
    except Exception as e:
        # Fallback comparison
        player_names = [p.get('name', 'Player') for p in players]
        fallback_comparison = f"Comparison between {' and '.join(player_names)}:\n\n"
        
        # Compare basic stats
        for player in players:
            fallback_comparison += f"- {player.get('name', 'Player')}:\n"
            fallback_comparison += f"  Age: {player.get('age', 'Unknown')}\n"
            fallback_comparison += f"  Position: {', '.join(player.get('positions', ['Unknown']))}\n"
            fallback_comparison += f"  Score: {player.get('score', 'Unknown')}\n\n"
        
        return fallback_comparison, ""


def format_stats_explanation(memory: ConversationMemory, 
                            response_data: Dict[str, Any]) -> str:
    """Format stats explanation into natural language"""
    explanations = response_data.get("explanations", {})
    
    # Format explanations into text
    explanation_text = ""
    for stat, explanation in explanations.items():
        explanation_text += f"{stat}: {explanation}\n\n"
    
    return explanation_text


def get_language_specific_prompt(language: str) -> str:
    """Get language-specific system prompt for response generation"""
    prompts = {
        "english": """You are a knowledgeable football scout assistant who presents scouting results in English.
        Process the list of players with their stats and present them in an engaging, professional way.
        Your audience are coaches looking for players with specific characteristics.
        Provide context about players' playing style and highlight standout stats.
        Present all given statistic fields for all players.
        Begin by acknowledging what the person was looking for.
        Present findings in an exciting, natural way.
        End your response by asking if they're satisfied with these players or if they want to refine their search.""",
        
        "portuguese": """Você é um assistente apaixonado de scout de futebol que apresenta resultados de pesquisa em Português.
        Processar a lista de jogadores com suas estatísticas e apresentá-los de forma envolvente e natural.
        Seu público são técnicos que buscam jogadores com características específicas.
        Fornecer contexto sobre o estilo de jogo dos jogadores e destacar estatísticas impressionantes.
        Apresentar todos os campos estatísticos fornecidos para todos os jogadores.
        Comece reconhecendo o que a pessoa estava procurando.
        Apresente os resultados de forma empolgante e natural.
        Termine perguntando se estão satisfeitos com esses jogadores ou se querem refinar a busca.""",
        
        "spanish": """Eres un apasionado asistente de scout de fútbol que presenta resultados de búsqueda en Español.
        Procesar la lista de jugadores con sus estadísticas y presentarlos de manera atractiva y natural.
        Tu audiencia son entrenadores que buscan jugadores con características específicas.
        Proporcionar contexto sobre el estilo de juego de los jugadores y destacar estadísticas sobresalientes.
        Presentar todos los campos estadísticos proporcionados para todos los jugadores.
        Comienza reconociendo lo que la persona estaba buscando.
        Presenta los resultados de manera emocionante y natural.
        Termina preguntando si están satisfechos con estos jugadores o si quieren refinar su búsqueda.""",
        
        "bulgarian": """Вие сте страстен футболен скаут асистент, който представя резултати от търсене на български.
        Обработете списъка с играчи с техните статистики и ги представете по ангажиращ и естествен начин.
        Вашата аудитория са треньори, които търсят играчи със специфични характеристики.
        Предоставяйте контекст за стила на игра на играчите и подчертавайте изключителни статистики.
        Представете всички предоставени статистически полета за всички играчи.
        Започнете с признаване на това, което човекът е търсил.
        Представете резултатите по вълнуващ и естествен начин.
        Завършете с въпрос дали са доволни от тези играчи или искат да прецизират търсенето си."""
    }
    
    return prompts.get(language, prompts["english"])


def split_response_and_satisfaction(text: str, language: str) -> Tuple[str, str]:
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
        satisfaction_questions = {
            "english": "Are you satisfied with these players or would you like to refine your search?",
            "portuguese": "Você está satisfeito com esses jogadores ou gostaria de refinar sua busca?",
            "spanish": "¿Estás satisfecho con estos jugadores o te gustaría refinar tu búsqueda?",
            "bulgarian": "Доволни ли сте от тези играчи или бихте искали да прецизирате търсенето си?"
        }
        return text, satisfaction_questions.get(language, satisfaction_questions["english"])