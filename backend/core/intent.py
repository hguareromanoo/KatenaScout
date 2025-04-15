"""
Intent recognition for KatenaScout

This module handles the identification of user intents and extraction of entities.
"""

from typing import List, Dict, Any, Optional, Callable
from pydantic import BaseModel, Field
import json

class Intent(BaseModel):
    """Model representing a user intent with confidence score"""
    name: str = Field(..., description="Intent name")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")

class SessionMemory:
    """Type for function signatures that reference session memory"""
    # Define attributes expected in memory for type hinting if possible
    messages: List[Dict[str, Any]] = []
    selected_players: List[Dict[str, Any]] = []
    context_window: int = 5 # Add default if not always present
    # Add other relevant attributes if known
    pass

def identify_intent(memory: SessionMemory, message: str, claude_api_call, context_messages: Optional[List[Dict[str, Any]]] = None) -> Intent:
    """
    Identify the user's intent from their message using Claude API
    
    Args:
        memory: The conversation memory
        message: The user message
        claude_api_call: Function to call Claude API
        context_messages: Optional context messages for better intent recognition
        
    Returns:
        Intent object with name and confidence
    """
    # Define available intents with examples
    intents = {
        "player_search": [
            "Find a center back with good passing",
            "I need a striker who scores a lot of goals",
            "Show me goalkeepers with good distribution",
            "Which right backs have good crossing ability?",
            "Who are the best young midfielders?"
        ],
        "player_comparison": [
            "Compare Ronaldo and Messi",
            "How does Player A compare to Player B?",
            "Show me a comparison of these players",
            "Which of these players is better?",
            "Compare the top 2 players from my search"
        ],
        "explain_stats": [
            "What does xG mean?",
            "Explain progressive passes",
            "What are defensive duels?",
            "I don't understand what pressing means",
            "What is PPDA in football?"
        ],
        "casual_conversation": [
            "Hello",
            "How are you?",
            "What can you do?",
            "Tell me about this service",
            "Thanks for your help"
        ]
    }
    
    # Get conversation context if not provided
    if context_messages is None:
        if hasattr(memory, "messages") and len(memory.messages) > 0:
            # Ensure context_window attribute exists or use a default
            context_window = getattr(memory, 'context_window', 5) 
            window_size = min(context_window * 2, len(memory.messages)) # Use pairs
            context_messages = memory.messages[-window_size:]
        else:
            context_messages = []
    
    # Add the current message if it's not already there
    current_message_content = message.strip()
    if not context_messages or not (context_messages[-1].get("role") == "user" and context_messages[-1].get("content") == current_message_content):
         context_messages.append({"role": "user", "content": current_message_content})

    
    # Create system prompt for intent recognition
    system_prompt = """
    You are an intent recognition system for a football scouting AI.
    Your task is to determine which of the defined intents best matches the user's message, considering the conversation context.
    
    You must identify one of the following intents:
    - player_search: User wants to find players with specific characteristics. IMPORTANT: THE QUERY MUST BE SPECIFIC. IT MUST INCLUDE A DESCRIPTION OF A PLAYER'S ATRIBUTES, NOT ONLY "I WANT TO FIND THE PERFECT PLAYER"
    - player_comparison: User wants to compare two or more players
    - explain_stats: User wants an explanation of football statistics or metrics
    - casual_conversation: User is engaging in small talk or asking about the system itself
    
    IMPORTANT: FOR PLAYER SEARCH, THE QUERY MUST BE SPECIFIC. IT MUST INCLUDE A DESCRIPTION OF A PLAYER'S ATRIBUTES, NOT ONLY "I WANT TO FIND THE PERFECT PLAYER". DO NOT SEND TO PLAYER SEARCH INTENT IF THE QUERY IS TOO VAGUE. JUST SEND TO CASUAL CONVERSATION.
    ## Examples:
    <example1>
    - "Find a center back with good passing"
    - Response: "intent": "player_search", "confidence": 0.95
    - Reason: The user is explicitly looking for a player with specific attributes
    </example1>
    <example2>
    - "I want to find the best player"
    - Response: "intent": "casual_conversation", "confidence": 0.85
    - Reason: The query is too vague and does not match any specific intent
    </example2>
    <example3>
    - "What is xG?"
    - Response: "intent": "explain_stats", "confidence": 0.90
    - Reason: The user is asking for an explanation of a football statistic
    </example3>
    <example4>
    - "Compare Ronaldo and Messi"
    - Response: "intent": "player_comparison", "confidence": 0.80
    - Reason: The user wants to compare two players
    </example4>
    

    Return only the most likely intent and a confidence score (0-1) where 1 is complete certainty.
    """
    
    # Provide conversation context and available intents
    user_prompt = f"""
    Here is the conversation context:
    {json.dumps(context_messages)}
    
    
    Based on the conversation context, determine the intent of the last user message.
    """
    
    try:
        # Call Claude API with tool for structured output
        response = claude_api_call(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            tools=[{
                "name": "classify_intent",
                "description": "Classify the intent of the user message",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "intent": {
                            "type": "string",
                            "enum": ["player_search", "player_comparison", "explain_stats", "casual_conversation"],
                            "description": "The identified intent"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "description": "Confidence score (0-1). It describes how certain the system is about the intent"
                        }
                    },
                    "required": ["intent", "confidence"]
                }
            }],
            tool_choice={"type": "tool", "name": "classify_intent"}
        )
        
        # Extract intent and confidence from response
        args = response.content[0].input
        intent = Intent(name=args["intent"], confidence=args["confidence"])
        # If confidence is low for specific intents, default to casual conversation
        if intent.name != "casual_conversation" and intent.confidence < 0.7:
            print(f"Low confidence ({intent.confidence}) for intent '{intent.name}', defaulting to casual_conversation.")
            return Intent(name='casual_conversation', confidence=1.0)
            
        return intent
    
    except Exception as e:
        print(f"Error in intent recognition: {str(e)}")
        # Default to most common intent with low confidence
        return Intent(name="casual_conversation", confidence=0.6)

def extract_entities(memory: SessionMemory, message: str, intent: Intent, claude_api_call, context_messages: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Extract entities from a user message based on the identified intent
    
    Args:
        memory: The conversation memory
        message: The user message
        intent: The identified intent
        claude_api_call: Function to call Claude API
        context_messages: Optional context messages for better entity extraction
        
    Returns:
        Dictionary of extracted entities
    """
    # Get conversation context if not provided
    if context_messages is None:
        if hasattr(memory, "messages") and len(memory.messages) > 0:
            # Ensure context_window attribute exists or use a default
            context_window = getattr(memory, 'context_window', 5)
            window_size = min(context_window * 2, len(memory.messages)) # Use pairs
            context_messages = memory.messages[-window_size:]
        else:
            context_messages = []
    
    # Add the current message if it's not already there
    current_message_content = message.strip()
    if not context_messages or not (context_messages[-1].get("role") == "user" and context_messages[-1].get("content") == current_message_content):
         context_messages.append({"role": "user", "content": current_message_content})

    
    # Intent-specific entity extraction
    if intent.name == "player_search":
        # Parameter extraction for search is handled by get_parameters in session.py
        return {} 
    elif intent.name == "player_comparison":
        return extract_comparison_entities(memory, message, claude_api_call, context_messages)
    elif intent.name == "explain_stats":
        return extract_stat_entities(memory, message, claude_api_call, context_messages)
    else:
        # For casual conversation, no specific entities to extract
        return {}

def extract_search_entities(memory: SessionMemory, message: str, claude_api_call, context_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract entities for player search intent (DEPRECATED - handled by get_parameters)"""
    print("WARNING: extract_search_entities called, but parameter extraction should be handled by get_parameters.")
    return {}

def extract_comparison_entities(memory: SessionMemory, message: str, claude_api_call, context_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract entities for player comparison intent, handling indirect references."""
    # Construct the database string safely, handling potential None or missing 'selected_players'
    selected_players_json = "[]"
    player_names_for_prompt = []
    if hasattr(memory, 'selected_players') and memory.selected_players:
        try:
            # Ensure selected_players is a list of dicts before dumping
            if isinstance(memory.selected_players, list) and all(isinstance(p, dict) for p in memory.selected_players):
                 # Extract only names for the prompt to keep it concise
                 player_names_for_prompt = [p.get("name", "Unknown") for p in memory.selected_players]
                 # Limit the number of names in the prompt to avoid excessive length
                 selected_players_json = json.dumps(player_names_for_prompt[:10]) # Limit to 10 names
            else:
                 print("DEBUG: memory.selected_players is not a list of dicts, using empty list for prompt.")
        except Exception as json_err:
            print(f"DEBUG: Error serializing memory.selected_players names: {json_err}")

    system_prompt = f"""
    ## Your task:
    Extract the names of football players mentioned for comparison in the context of this conversation.
    You must fetch player's complete names from partial mentions or nicknames using the provided database context. Identify which players the user is referring to.

    ## Context:
    - The `database` field below contains the list of player names most recently shown or discussed ({selected_players_json}). These are the primary candidates if the user makes an indirect reference.
    - The `conversation context` provides the history of user messages and assistant responses.

    ## Instructions:
    1.  **Identify Explicit Names:** If the user explicitly mentions player names (full or partial), extract their exact full names by matching them against the names in the provided `database`. Prioritize names from the database if there's ambiguity.
    2.  **Identify Indirect References:** If the user uses phrases like "compare them", "compare these two", "os dois", "compare the previous ones", etc., AND does not mention specific new names, understand that they likely refer to the players in the `database`. In this case, extract the names of the first two players listed in the `database`.
    3.  **Identify "Top N":** If the user asks to compare the "top N" players (e.g., "compare the top 2"), set `compare_top_n` to `true` and extract the number `N` into the `top_n` field. Do *not* extract player names in this case.
    4.  **Return Exact Names:** Always return the player names exactly as they appear in the `database`.
    5.  **Original Query:** Include the user's original message in the `original_query` field.

    ## Examples:
    <ex_1>
    User Query: "Compare Ronaldo and Messi"
    Database: ["Cristiano Ronaldo", "Lionel Messi"]
    Good Response: {{ "player_names": ["Cristiano Ronaldo", "Lionel Messi"], "compare_top_n": false, "original_query": "Compare Ronaldo and Messi" }}
    Bad Response: {{ "player_names": ["Ronaldo", "Messi"], ... }} (Reason: Names not exact match from database)
    </ex_1>
    <ex_2>
    User Query: "Compare Lukaku and Lautaro on the brazilian playing style"
    Database: ["Lautaro Javier Martínez", "Romelu Menama Lukaku Bolingoli", "Gabriel Barbosa"]
    Good Response: {{ "player_names": ["Romelu Menama Lukaku Bolingoli", "Lautaro Javier Martínez"], "compare_top_n": false, "original_query": "Compare Lukaku and Lautaro on the brazilian playing style" }}
    Bad Response: {{ "player_names": ["Lukaku", "Lautaro"], ... }} (Reason: Names not exact match from database)
    </ex_2>
    <ex_3>
    User Query: "Compare the top 2 players from my search"
    Database: ["Cristiano Ronaldo", "Lionel Messi", "Neymar Jr.", "Kylian Mbappé"]
    Good Response: {{ "player_names": [], "compare_top_n": true, "top_n": 2, "original_query": "Compare the top 2 players from my search" }}
    Bad Response: {{ "player_names": ["Cristiano Ronaldo", "Lionel Messi"], "compare_top_n": false, ... }} (Reason: Should set compare_top_n=true, player_names=[])
    </ex_3>
    <ex_4>
    User Query: "Compare Martinelly and Gabriel Barbosa playing as a reference"
    Database: ["Gabriel Barbosa", "Gabriel Martinelli", "Gabriel Jesus"]
    Good Response: {{ "player_names": ["Gabriel Martinelli", "Gabriel Barbosa"], "compare_top_n": false, "original_query": "Compare Martinelly and Gabriel Barbosa playing as a reference" }}
    Bad Response: {{ "player_names": ["Martinelly", "Gabriel Barbosa"], ... }} (Reason: Names not exact match from database)
    </ex_4>
    <ex_5>
    User Query: "compare them"
    Database: ["Cristiano Ronaldo", "Lionel Messi", "Neymar Jr."]
    Good Response: {{ "player_names": ["Cristiano Ronaldo", "Lionel Messi"], "compare_top_n": false, "original_query": "compare them" }}
    Reason: User referred indirectly to the players in the database context.
    </ex_5>
    <ex_6>
    User Query: "compare os dois"
    Database: ["Gabriel Martinelli", "Gabriel Barbosa"]
    Good Response: {{ "player_names": ["Gabriel Martinelli", "Gabriel Barbosa"], "compare_top_n": false, "original_query": "compare os dois" }}
    Reason: User referred indirectly ("os dois") to the players in the database context.
    </ex_6>
    """
    
    # Prepare the user prompt for the API call, including the selected players database
    user_prompt = f"""
    Conversation Context:
    {json.dumps(context_messages)}

    Database (Recently Shown Players): 
    {selected_players_json}

    User Query: "{message}"

    Extract the comparison entities based on the instructions and examples provided in the system prompt.
    """
    
    try:
        # Call Claude API with tool for structured output
        response = claude_api_call(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            tools=[{
                "name": "extract_comparison_players",
                "description": "Extract player names for comparison based on conversation context and database.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "player_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of player names to compare EXACTLY how they appear in the database context."
                        },
                        "compare_top_n": {
                            "type": "boolean",
                            "default": False,
                            "description": "Whether the user wants to compare top N players without naming them"
                        },
                        "top_n": {
                            "type": "integer",
                            "description": "Number of top players to compare (if compare_top_n is true)"
                        },
                        "original_query": {
                            "type": "string",
                            "description": "The original query from the user, for context"
                        }
                    },
                    "required": ["player_names", "compare_top_n", "original_query"] # Made original_query required
                }
            }],
            tool_choice={"type": "tool", "name": "extract_comparison_players"}
        )
        
        # Extract entity data from response
        args = response.content[0].input
        
        # --- Fallback Logic for Indirect References ---
        extracted_names = args.get("player_names", [])
        is_top_n_request = args.get("compare_top_n", False)
        
        # Simple check for indirect phrases (can be expanded)
        indirect_phrases = ["compare them", "compare these", "os dois", "compare the two"]
        # Check if the message *only* contains an indirect phrase (or very little else)
        is_indirect_message = any(phrase == message.lower().strip() for phrase in indirect_phrases) or \
                              any(message.lower().startswith(phrase) and len(message) < len(phrase) + 5 for phrase in indirect_phrases)


        if not extracted_names and not is_top_n_request and is_indirect_message and hasattr(memory, 'selected_players') and isinstance(memory.selected_players, list) and len(memory.selected_players) >= 2:
            print("DEBUG: LLM didn't extract names for indirect comparison, using fallback logic.")
            # Use the names from the session context (using the full player objects now)
            context_players_data = memory.selected_players[:2]
            context_player_names = [p.get("name") for p in context_players_data if isinstance(p, dict) and "name" in p]
            
            if len(context_player_names) == 2:
                 args["player_names"] = context_player_names
                 print(f"DEBUG: Using fallback players from context: {context_player_names}")


        entities = {
            "players_to_compare": args.get("player_names", []), # Use potentially updated names
            "compare_top_n": args.get("compare_top_n", False),
            "original_query": args.get("original_query", message) # Use extracted query if available
        }
        
        if entities["compare_top_n"] and "top_n" in args:
            entities["top_n"] = args["top_n"]
        
        # Log the final extracted/fallback entities for debugging
        print(f"Final players to compare: {entities['players_to_compare']}")
        print(f"Original query for comparison context: {entities['original_query']}")
        
        return entities
    
    except Exception as e:
        print(f"Error in comparison entity extraction: {str(e)}")
        # Attempt fallback even on error if possible
        if hasattr(memory, 'selected_players') and isinstance(memory.selected_players, list) and len(memory.selected_players) >= 2:
             context_players_data = memory.selected_players[:2]
             context_player_names = [p.get("name") for p in context_players_data if isinstance(p, dict) and "name" in p]
             if len(context_player_names) == 2:
                  print(f"DEBUG: Using fallback players due to exception: {context_player_names}")
                  return {"players_to_compare": context_player_names, "compare_top_n": False, "original_query": message}
        # If fallback not possible, return empty
        return {"players_to_compare": [], "compare_top_n": False, "original_query": message}

def extract_stat_entities(memory: SessionMemory, message: str, claude_api_call, context_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract entities for stats explanation intent"""
    system_prompt = """
    You are an entity extraction system for a football scouting AI.
    Your task is to extract football statistics or metrics mentioned in a message about explaining stats.
    
    Extract ONLY football statistics or metrics that the user wants explained.
    """
    
    user_prompt = f"""
    Here is the conversation context:
    {json.dumps(context_messages)}
    
    Extract the names of football statistics or metrics that the user wants explained.
    Common football stats include: xG, progressive passes, through passes, pressing, PPDA, defensive duels, etc.
    """
    
    try:
        # Call Claude API with tool for structured output
        response = claude_api_call(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            tools=[{
                "name": "extract_stats_to_explain",
                "description": "Extract football statistics to explain",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "stats": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of football statistics or metrics to explain"
                        }
                    },
                    "required": ["stats"]
                }
            }],
            tool_choice={"type": "tool", "name": "extract_stats_to_explain"}
        )
        
        # Extract entity data from response
        args = response.content[0].input
        return {"stats_to_explain": args["stats"]}
    
    except Exception as e:
        print(f"Error in stats entity extraction: {str(e)}")
        return {"stats_to_explain": []}

def generate_follow_up_suggestions(memory: SessionMemory, players: Any) -> List[str]:
    """
    Generate follow-up suggestions based on the conversation context and found players
    
    Args:
        memory: The conversation memory
        players: The players found in the search (should be a list of dicts but might be something else)
        
    Returns:
        List of follow-up suggestion strings
    """
    # DEBUG: Print players and their type for troubleshooting
    print(f"DEBUG - generate_follow_up_suggestions received players of type: {type(players)}")
    # print(f"DEBUG - players value: {players}") # Avoid printing potentially large player data
    print(f"DEBUG - memory type: {type(memory)}")
    try:
        import json
        # Print only name and ID of first player if exists
        if isinstance(players, list) and len(players) > 0 and isinstance(players[0], dict):
             first_player_info = {k: players[0][k] for k in ['name', 'id', 'wyId'] if k in players[0]}
             print(f"DEBUG - first player info: {json.dumps(first_player_info)}")
        else:
             print("DEBUG - first player: None or not a dict")
    except Exception as e:
        print(f"DEBUG - Error accessing first player info: {str(e)}")
    
    # Handle various error cases
    if not players:
        return [
            "Try searching for a different position",
            "Look for players with different skills",
            "Broaden your search criteria"
        ]
    
    # Handle case where players is not a list
    if not isinstance(players, list):
        print(f"Warning: players is not a list but {type(players)}")
        return [
            "Try searching for a different position",
            "Look for players with different skills",
            "Try using more specific search terms"
        ]
    
    # Get player positions and attributes for context
    positions = set()
    for player in players:
        if isinstance(player, dict) and "positions" in player and player["positions"]:
            # Handle different position formats
            if isinstance(player["positions"], list):
                positions.update(player["positions"])
            elif isinstance(player["positions"], str):
                positions.add(player["positions"])
    
    # Generate generic follow-up suggestions
    suggestions = []
    if len(players) >= 2: # Only suggest comparison if there are at least 2 players
        suggestions.append("Compare these players")
    
    # Only add player name suggestion if we have valid player data
    if players and isinstance(players[0], dict) and "name" in players[0]:
        suggestions.append(f"Find more players like {players[0]['name']}")
    else:
        suggestions.append("Find similar players")
    
    # Add position-specific suggestions
    if "cf" in positions or "lw" in positions or "rw" in positions:
        suggestions.append("Find attackers with better finishing")
    
    if "cb" in positions or "lb" in positions or "rb" in positions:
        suggestions.append("Find defenders with better passing")
    
    if "cmf" in positions or "dmf" in positions or "amf" in positions:
        suggestions.append("Find midfielders with more creativity")
    
    if "gk" in positions:
        suggestions.append("Find goalkeepers with better distribution")
    
    # Add general suggestions
    suggestions.extend([
        "Show me younger players with similar skills",
        "Find players with better physical attributes"
    ])
    
    # Return a curated list (not too many)
    return suggestions[:4]
