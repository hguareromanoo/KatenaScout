"""
Main orchestrator for the KatenaScout conversation system
"""

from typing import Dict, Any, List
import json
from .models import ConversationMemory, Intent
from .intents import identify_intent, extract_entities
from .handlers import (
    handle_player_search,
    handle_player_comparison,
    handle_stats_explanation,
    handle_casual_chat,
    handle_fallback
)


def get_context_messages(memory: ConversationMemory) -> List[Dict[str, str]]:
    """
    Get the relevant context messages from conversation history
    
    Args:
        memory: The conversation memory
        
    Returns:
        List of messages for context
    """
    # Use the last N message pairs for context
    window_size = min(memory.context_window * 2, len(memory.messages))
    return memory.messages[-window_size:]


def get_conversation_memory(session_id: str, language: str, chat_manager) -> ConversationMemory:
    """
    Get or create a conversation memory object for a session
    
    Args:
        session_id: The session ID
        language: The user's preferred language
        chat_manager: The chat session manager
        
    Returns:
        A ConversationMemory object
    """
    try:
        # Get session data from the chat manager
        if session_id not in chat_manager.sessions:
            chat_manager.create_session(session_id, language)
        
        session_data = chat_manager.get_session(session_id, language)
        
        # Check if we have stored a full memory structure
        if "_memory_data" in session_data and session_data["_memory_data"]:
            try:
                # Reconstruct from the stored memory data
                memory = ConversationMemory(**session_data["_memory_data"])
                print(f"Restored full conversation memory for session {session_id}")
                return memory
            except Exception as restore_error:
                print(f"Error restoring full memory: {str(restore_error)}")
                # Fall through to standard reconstruction
        
        # Handle search parameters, ensuring they're properly formatted
        search_params = session_data.get("search_params", {})
        if isinstance(search_params, str):
            try:
                import json
                search_params = json.loads(search_params)
            except:
                search_params = {}
        
        # Get messages ensuring they have proper role/content structure
        messages = session_data.get("messages", [])
        structured_messages = []
        for msg in messages:
            # Ensure messages have proper structure
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                structured_messages.append(msg)
            elif isinstance(msg, dict) and "content" in msg:
                # Add missing role
                role = "assistant" if msg.get("is_satisfaction_question", False) else "user"
                structured_messages.append({"role": role, "content": msg["content"]})
            elif isinstance(msg, str):
                # Convert string messages to structured format
                structured_messages.append({"role": "user", "content": msg})
        
        # Create a ConversationMemory object from the session data
        memory = ConversationMemory(
            session_id=session_id,
            messages=structured_messages,
            current_intent=session_data.get("current_intent"),
            language=session_data.get("language", "english"),
            search_history=session_data.get("search_history", []),
            selected_players=session_data.get("selected_players", []),
            search_params=search_params,
            last_search_params=search_params,  # Initialize with existing params
            satisfaction=session_data.get("satisfaction"),
            current_prompt=session_data.get("current_prompt", ""),
            is_follow_up=session_data.get("is_follow_up", False),
            # Initialize with empty entities if not already present
            entities=session_data.get("entities", {}),
            detected_entities=session_data.get("detected_entities", [])
        )
        
        # Print debug info
        print(f"Created enhanced memory for session {session_id}")
        print(f"  Messages: {len(memory.messages)}")
        print(f"  Search history: {len(memory.search_history)}")
        print(f"  Selected players: {len(memory.selected_players)}")
        
        return memory
    except Exception as e:
        print(f"Error creating conversation memory: {str(e)}")
        # Create a default memory object
        return ConversationMemory(
            session_id=session_id,
            language=language
        )


def process_user_message(session_id: str, message: str, chat_manager, language: str = "english"):
    """
    Process a user message through the orchestrator with structured conversation history
    
    Args:
        session_id: The session ID
        message: The user message
        chat_manager: The chat session manager
        language: The user's preferred language
        
    Returns:
        Response data
    """
    # Get or create conversation memory with proper structure
    memory = get_conversation_memory(session_id, language, chat_manager)
    
    # Add user message to structured history
    memory.messages.append({"role": "user", "content": message})
    
    # Print debug information
    print(f"Processing message: '{message}'")
    print(f"Current conversation history has {len(memory.messages)} messages")
    
    # Determine if this is likely a follow-up query
    is_follow_up = False
    if len(memory.messages) > 2:  # If we have previous conversation
        # Look for follow-up patterns
        follow_up_phrases = ["what about", "which ones", "show me", "compare them", "these players"]
        if any(phrase in message.lower() for phrase in follow_up_phrases) or message.endswith("?"):
            is_follow_up = True
            print(f"Detected as follow-up query: {is_follow_up}")
    
    # For backward compatibility with the current_prompt approach
    if is_follow_up and memory.search_history:
        # Only store the last query for display purposes
        memory.search_history.append(message)
        # Don't combine queries - we're using structured history now
        memory.current_prompt = message
        # But log what the old system would have done
        print(f"Using structured conversation history instead of combined query")
    else:
        memory.search_history = [message]
        memory.current_prompt = message
    
    # Store the follow-up status
    memory.is_follow_up = is_follow_up
    
    # Process with orchestrator
    response_data = conversation_orchestrator(memory, message, chat_manager)
    
    # Update session in chat manager
    update_chat_session(memory, chat_manager)
    
    return response_data


def conversation_orchestrator(memory: ConversationMemory, message: str, chat_manager):
    """
    Main orchestrator function that decides what to do with a message
    using structured conversation history
    
    Args:
        memory: The conversation memory
        message: The user message
        chat_manager: The chat session manager
        
    Returns:
        Response data
    """
    # Get proper context for intent identification
    context_messages = get_context_messages(memory)
    
    # Identify user intent with Claude API using conversation context
    intent = identify_intent(memory, message, chat_manager.call_claude_api, context_messages)
    memory.current_intent = intent.name
    
    # Extract relevant entities based on intent
    entities = extract_entities(memory, message, intent, chat_manager.call_claude_api, context_messages)
    memory.entities.update(entities)
    
    # Dispatch to appropriate function based on intent
    if intent.name == "player_search":
        response = handle_player_search(memory, message, chat_manager)
    elif intent.name == "player_comparison":
        response = handle_player_comparison(memory, message, chat_manager)
    elif intent.name == "explain_stats":
        response = handle_stats_explanation(memory, message, chat_manager)
    elif intent.name == "casual_conversation":
        response = handle_casual_chat(memory, message, chat_manager)
    else:
        response = handle_fallback(memory, message, chat_manager)
    
    # Generate appropriate response with conversation context
    return format_response(memory, response, chat_manager)


def format_response(memory: ConversationMemory, response_data: Dict[str, Any], chat_manager) -> Dict[str, Any]:
    """
    Format the response data based on type
    
    Args:
        memory: The conversation memory
        response_data: The response data
        chat_manager: The chat session manager
        
    Returns:
        Formatted response data
    """
    response_type = response_data.get("type", "text")
    language = memory.language
    
    # Add the response data directly to the return value
    result = {
        "success": True,
        "type": response_type,
        "language": language
    }
    
    # Format response based on type
    if response_type == "search_results":
        players = response_data.get("players", [])
        
        # Use Claude to generate natural language response
        system_prompt = get_language_specific_prompt(language)
        
        try:
            # Create conversational response
            claude_response = chat_manager.call_claude_api(
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
            
            # Add response to memory
            memory.messages.append({"role": "assistant", "content": text_response})
            
            # Split into main response and satisfaction question
            main_response, satisfaction_question = split_response_and_satisfaction(text_response, language)
            
            result["response"] = main_response
            result["satisfaction_question"] = satisfaction_question
            result["players"] = players
            result["follow_up_suggestions"] = response_data.get("follow_up_suggestions", [])
            
        except Exception as e:
            # Fallback to simple response
            result["response"] = f"Found {len(players)} players matching your criteria."
            result["satisfaction_question"] = get_satisfaction_question(language)
            result["players"] = players
            result["error"] = str(e)
    
    elif response_type == "player_comparison":
        players = response_data.get("players", [])
        comparison_aspects = response_data.get("comparison_aspects", [])
        
        result["players"] = players
        result["comparison_aspects"] = comparison_aspects
        
        # Generate text comparison
        try:
            system_prompt = """You are a football analyst comparing players. 
            Provide a detailed, fact-based comparison highlighting strengths and weaknesses of each player."""
            
            claude_response = chat_manager.call_claude_api(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"Compare these players: {json.dumps(players)}"}
                ]
            )
            
            comparison_text = claude_response.content[0].text
            memory.messages.append({"role": "assistant", "content": comparison_text})
            
            result["response"] = comparison_text
            
        except Exception as e:
            # Fallback
            result["response"] = f"Here's a comparison of {', '.join([p.get('name', 'Player') for p in players])}."
            result["error"] = str(e)
    
    elif response_type == "stats_explanation":
        explanations = response_data.get("explanations", {})
        
        # Format explanations into text
        explanation_text = ""
        for stat, explanation in explanations.items():
            explanation_text += f"{stat}: {explanation}\n\n"
        
        memory.messages.append({"role": "assistant", "content": explanation_text})
        result["response"] = explanation_text
        result["explanations"] = explanations
    
    elif response_type == "text":
        text = response_data.get("text", "")
        memory.messages.append({"role": "assistant", "content": text})
        result["response"] = text
    
    elif response_type == "error":
        error_message = response_data.get("message", "An error occurred")
        memory.messages.append({"role": "assistant", "content": error_message})
        result["response"] = error_message
        result["success"] = False
    
    return result


def update_chat_session(memory: ConversationMemory, chat_manager):
    """
    Update the chat session with data from enhanced conversation memory
    
    Args:
        memory: The conversation memory
        chat_manager: The chat session manager
    """
    try:
        # Make sure the session exists
        if memory.session_id not in chat_manager.sessions:
            chat_manager.create_session(memory.session_id, memory.language)
        
        # Extract assistant responses from messages
        assistant_messages = []
        for i, msg in enumerate(memory.messages):
            if msg.get("role") == "assistant":
                # Only include assistant messages that come after a user message
                if i > 0 and memory.messages[i-1].get("role") == "user":
                    assistant_messages.append(msg)
        
        # Sync structured messages to chat manager
        for msg in assistant_messages:
            if not chat_manager.sessions[memory.session_id].get("messages") or msg not in chat_manager.sessions[memory.session_id].get("messages", []):
                chat_manager.update_session(memory.session_id, message=msg)
        
        # Sync other properties with chat manager's session
        if memory.selected_players:
            chat_manager.update_session(memory.session_id, players=memory.selected_players)
            
        # Store both last search params and full search params
        if memory.last_search_params:
            chat_manager.update_session(memory.session_id, search_params=memory.last_search_params)
        elif memory.search_params:
            chat_manager.update_session(memory.session_id, search_params=memory.search_params)
            
        # Sync satisfaction status
        if memory.satisfaction is not None:
            chat_manager.update_session(memory.session_id, satisfaction=memory.satisfaction)
            
        # Maintain backward compatibility with current_prompt
        if memory.current_prompt:
            chat_manager.update_session(memory.session_id, prompt=memory.current_prompt)
        
        # Store the full memory structure in a special key for later retrieval
        # This ensures we don't lose the rich conversation context when retrieving the memory
        full_memory_data = memory.model_dump()
        chat_manager.sessions[memory.session_id]["_memory_data"] = full_memory_data
        
        # Print debug info about sync status
        print(f"Synced conversation memory for session {memory.session_id}")
        print(f"  Messages synced: {len(assistant_messages)}")
        print(f"  Entities stored: {len(memory.entities)}")
        print(f"  Detected entities: {len(memory.detected_entities)}")
    
    except Exception as e:
        print(f"Error updating chat session: {str(e)}")


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


def get_satisfaction_question(language: str) -> str:
    """Get language-specific satisfaction question"""
    questions = {
        "english": "Are you satisfied with these players or would you like to refine your search?",
        "portuguese": "Você está satisfeito com esses jogadores ou gostaria de refinar sua busca?",
        "spanish": "¿Estás satisfecho con estos jugadores o te gustaría refinar tu búsqueda?",
        "bulgarian": "Доволни ли сте от тези играчи или бихте искали да прецизирате търсенето си?"
    }
    
    return questions.get(language, questions["english"])


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