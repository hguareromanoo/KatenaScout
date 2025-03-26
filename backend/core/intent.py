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
            window_size = min(5, len(memory.messages))
            context_messages = memory.messages[-window_size:]
        else:
            context_messages = []
    
    # Add the current message if it's not already there
    current_message_content = message.strip()
    if not any(msg.get("content") == current_message_content for msg in context_messages if msg.get("role") == "user"):
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
        if intent.name != "casual_conversation" and intent.confidence< 0.7:
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
            window_size = min(5, len(memory.messages))
            context_messages = memory.messages[-window_size:]
        else:
            context_messages = []
    
    # Add the current message if it's not already there
    current_message_content = message.strip()
    if not any(msg.get("content") == current_message_content for msg in context_messages if msg.get("role") == "user"):
        context_messages.append({"role": "user", "content": current_message_content})
    
    # Intent-specific entity extraction
    if intent.name == "player_search":
        return extract_search_entities(memory, message, claude_api_call, context_messages)
    elif intent.name == "player_comparison":
        return extract_comparison_entities(memory, message, claude_api_call, context_messages)
    elif intent.name == "explain_stats":
        return extract_stat_entities(memory, message, claude_api_call, context_messages)
    else:
        # For casual conversation, no specific entities to extract
        return {}

def extract_search_entities(memory: SessionMemory, message: str, claude_api_call, context_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract entities for player search intent"""
    # For search intent, we don't need to extract entities here
    # The actual parameter extraction is handled by get_parameters
    return {}

def extract_comparison_entities(memory: SessionMemory, message: str, claude_api_call, context_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract entities for player comparison intent"""
    system_prompt = """
    You are an entity extraction system for a football scouting AI.
    Your task is to extract player names mentioned in a message about comparing players.
    
    Extract ONLY player names that are explicitly mentioned for comparison.
    Extract the EXACT name as mentioned by the user, without modification.
    If the user mentions comparing "top N players", do NOT extract any names.
    
    IMPORTANT: Do not try to complete or correct player names. Extract them EXACTLY as written by the user.
    For example, if the user writes "Compare Lautaro with Lukaku", extract ["Lautaro", "Lukaku"] exactly.
    """
    
    user_prompt = f"""
    Here is the conversation context:
    {json.dumps(context_messages)}
    
    Extract the names of players that the user wants to compare.
    Extract the names EXACTLY as they appear in the message, without trying to correct or complete them.
    If the user wants to compare "top 2" or similar without naming specific players, return an empty list.
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
                "description": "Extract player names for comparison",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "player_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of player names to compare EXACTLY as mentioned by the user"
                        },
                        "compare_top_n": {
                            "type": "boolean",
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
                    "required": ["player_names", "compare_top_n"]
                }
            }],
            tool_choice={"type": "tool", "name": "extract_comparison_players"}
        )
        
        # Extract entity data from response
        args = response.content[0].input
        entities = {
            "players_to_compare": args["player_names"],
            "compare_top_n": args["compare_top_n"],
            "original_query": message  # Add the original query for context
        }
        
        if args["compare_top_n"] and "top_n" in args:
            entities["top_n"] = args["top_n"]
        
        # Log the extracted entities for debugging
        print(f"Extracted players to compare: {entities['players_to_compare']}")
        print(f"Original query: {message}")
        
        return entities
    
    except Exception as e:
        print(f"Error in comparison entity extraction: {str(e)}")
        return {"players_to_compare": [], "original_query": message}

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
    print(f"DEBUG - players value: {players}")
    print(f"DEBUG - memory type: {type(memory)}")
    try:
        import json
        print(f"DEBUG - first player: {json.dumps(players[0]) if isinstance(players, list) and len(players) > 0 else 'None'}")
    except Exception as e:
        print(f"DEBUG - Error accessing players: {str(e)}")
    
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
    suggestions = [
        "Compare these players"
    ]
    
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