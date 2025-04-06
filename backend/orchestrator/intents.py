"""
Intent recognition and handling for the KatenaScout conversation orchestrator
"""

from typing import Dict, List, Any
import json
from .models import ConversationMemory, Intent


def identify_intent(memory: ConversationMemory, message: str, call_claude_api, context_messages=None) -> Intent:
    """
    Identify the user's intent from a message using Claude API and conversation context
    
    Args:
        memory: The conversation memory
        message: The user message
        call_claude_api: Function to call Claude API
        context_messages: Optional list of context messages
        
    Returns:
        Intent object with name and confidence
    """
    # Use provided context messages or create from memory
    if context_messages is None:
        context_messages = memory.messages[-memory.context_window*2:] if memory.messages else []
    
    system_prompt = """
    Identify the user's intent from their message in the context of this conversation.
    The user is interacting with a football scouting application.
    
    Available intents:
    - player_search: User wants to find players matching specific criteria. The SPECIFIC is the main part (e.g., "Find attackers with high shooting accuracy")
    - player_comparison: User wants to compare multiple players (e.g., "Compare these two strikers")
    - explain_stats: User wants explanation of statistics or metrics (e.g., "What is xG?")
    - casual_conversation: General chat not related to specific player search (e.g., "Hello", "Thank you")
    - other: None of the above
    ## Examples:
    ## 1. User: "Who are the best defenders?"
    ##    Intent: player_search
    ## 2. User: "Compare these two"
    ##    Intent: player_comparison
    ## 3. User: "What is xG?"
    ##    Intent: explain_stats
    ## 4. User: "Hello, I need some help finding the best players"
    ##    Intent: casual_conversation
    
    
    Pay special attention to follow-up messages that reference previous players or queries.
    For example, if the user says "Compare them" after search results, this is player_comparison intent.
    If they say "Which ones are better at defending?", this is still player_search but with context.
    
    Analyze the full conversation context and determine the most likely intent.
    """
    
    try:
        response = call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=context_messages,  # Use the structured conversation history
            tools=[{
                "name": "classify_intent",
                "description": "Classify the user's intent",
                "input_schema": Intent.model_json_schema()
            }],
            tool_choice={"type": "tool", "name": "classify_intent"}
        )
        
        return Intent(**response.content[0].input)
    except Exception as e:
        print(f"Error identifying intent: {str(e)}")
        # Fallback to a default intent if API call fails
        return Intent(name="player_search", confidence=0.5)


def extract_entities(memory: ConversationMemory, message: str, intent: Intent, call_claude_api, context_messages=None) -> Dict[str, Any]:
    """
    Extract relevant entities from a user message based on intent using conversation context
    
    Args:
        memory: The conversation memory
        message: The user message
        intent: The identified intent
        call_claude_api: Function to call Claude API
        context_messages: Optional list of context messages
        
    Returns:
        Dictionary of extracted entities
    """
    # Use provided context messages or create from memory
    if context_messages is None:
        context_messages = memory.messages[-memory.context_window*2:] if memory.messages else []
    
    # Different entity extraction based on intent type
    try:
        if intent.name == "player_search":
            # Now handled here for better context
            return extract_search_entities(memory, message, call_claude_api, context_messages)
        elif intent.name == "player_comparison":
            return extract_player_entities(memory, message, call_claude_api, context_messages)
        elif intent.name == "explain_stats":
            return extract_stat_entities(memory, message, call_claude_api, context_messages)
        else:
            return {}  # No specific entities for casual conversation or other
    except Exception as e:
        print(f"Error extracting entities: {str(e)}")
        return {}


def extract_search_entities(memory: ConversationMemory, message: str, call_claude_api, context_messages=None) -> Dict[str, Any]:
    """
    Extract search-related entities from user message with context awareness
    
    Args:
        memory: The conversation memory
        message: The user message
        call_claude_api: Function to call Claude API
        context_messages: Optional list of context messages
        
    Returns:
        Dictionary of search entities
    """
    if context_messages is None:
        context_messages = memory.messages[-memory.context_window*2:] if memory.messages else []
    
    system_prompt = """
    Extract search parameters from the user's message in the context of the entire conversation.
    Pay special attention to follow-up messages that reference previous searches or results.
    
    For example:
    - If user says "Find me younger ones" after a search for midfielders, they want younger midfielders
    - If user says "What about defenders?" after searching for fast players, they want fast defenders
    
    Extract both explicit parameters and those implied by the conversation context.
    """
    
    # Define tool schema for search extraction
    schema = {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "description": "Position types the user is looking for",
                "items": {"type": "string"}
            },
            "skills": {
                "type": "array",
                "description": "Skills or attributes mentioned (e.g., 'passing', 'defending')",
                "items": {"type": "string"}
            },
            "age_range": {
                "type": "object",
                "description": "Age constraints mentioned",
                "properties": {
                    "min": {"type": "integer", "nullable": True},
                    "max": {"type": "integer", "nullable": True}
                }
            },
            "is_relative_to_previous": {
                "type": "boolean",
                "description": "Whether this query is relative to previous results"
            }
        }
    }
    
    try:
        response = call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=context_messages,
            tools=[{
                "name": "extract_search_parameters",
                "description": "Extract search parameters from the conversation",
                "input_schema": schema
            }],
            tool_choice={"type": "tool", "name": "extract_search_parameters"}
        )
        
        extracted = response.content[0].input
        
        # Store the extracted entities in memory for later use
        memory.detected_entities.append({
            "type": "search_parameters",
            "value": extracted
        })
        
        return {"search_parameters": extracted}
    except Exception as e:
        print(f"Error extracting search entities: {str(e)}")
        return {}


def extract_player_entities(memory: ConversationMemory, message: str, call_claude_api, context_messages=None) -> Dict[str, Any]:
    """
    Extract player names for comparison with context awareness
    
    Args:
        memory: The conversation memory
        message: The user message
        call_claude_api: Function to call Claude API
        context_messages: Optional list of context messages
        
    Returns:
        Dictionary with player names to compare
    """
    if context_messages is None:
        context_messages = memory.messages[-memory.context_window*2:] if memory.messages else []
    
    system_prompt = """
   ## Your task:
    Extract the names of football players mentioned for comparison in the context of this conversation.
    You must fetch player's complete names from partial mentions or nicknames. Identify which players the user is referring to.
    These are the players you must fetch the players from: json.dumps(memory.)
    
    # Define tool schema for player extraction
    schema = {
        "type": "object",
        "properties": {
            "players": {
                "type": "array",
                "description": "List of player names mentioned or referenced",
                "items": {"type": "string"}
            },
            "using_previous_results": {
                "type": "boolean",
                "description": "Whether the user is referring to previously mentioned players"
            }
        },
        "required": ["players"]
    }
    
    try:
        response = call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=context_messages,
            tools=[{
                "name": "extract_players",
                "description": "Extract player names for comparison",
                "input_schema": schema
            }],
            tool_choice={"type": "tool", "name": "extract_players"}
        )
        
        extracted = response.content[0].input
        
        # Store the extracted players in memory
        memory.detected_entities.append({
            "type": "players_to_compare",
            "value": extracted.get("players", [])
        })
        
        return {"players_to_compare": extracted.get("players", [])}
    except Exception as e:
        print(f"Error extracting player entities: {str(e)}")
        # If we have previous players in memory, use those
        if "recent_players" in memory.entities and memory.entities["recent_players"]:
            return {"players_to_compare": memory.entities["recent_players"][:2]}
        return {"players_to_compare": []}


def extract_stat_entities(memory: ConversationMemory, message: str, call_claude_api, context_messages=None) -> Dict[str, Any]:
    """
    Extract statistics or metrics mentioned for explanation with context awareness
    
    Args:
        memory: The conversation memory
        message: The user message
        call_claude_api: Function to call Claude API
        context_messages: Optional list of context messages
        
    Returns:
        Dictionary with stats to explain
    """
    if context_messages is None:
        context_messages = memory.messages[-memory.context_window*2:] if memory.messages else []
    
    system_prompt = """
    Extract the football statistics or metrics mentioned in the conversation that the user wants explained.
    Pay attention to both direct questions and follow-up questions about statistics.
    
    Common football metrics include:
    - xG (expected goals)
    - Passing accuracy
    - Progressive passes
    - Defensive duels
    - Ball recoveries
    - Shot conversion rate
    - And many others
    
    If the user is referring to stats mentioned earlier in the conversation or shown in player data,
    identify those stats as well.
    """
    
    # Define tool schema for stat extraction
    schema = {
        "type": "object",
        "properties": {
            "stats": {
                "type": "array",
                "description": "List of statistics or metrics to explain",
                "items": {"type": "string"}
            },
            "is_referencing_previous": {
                "type": "boolean",
                "description": "Whether the user is referring to previously mentioned stats"
            }
        },
        "required": ["stats"]
    }
    
    try:
        response = call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=context_messages,
            tools=[{
                "name": "extract_stats",
                "description": "Extract statistics or metrics for explanation",
                "input_schema": schema
            }],
            tool_choice={"type": "tool", "name": "extract_stats"}
        )
        
        extracted = response.content[0].input
        
        # Store the extracted stats in memory
        memory.detected_entities.append({
            "type": "stats_to_explain",
            "value": extracted.get("stats", [])
        })
        
        return {"stats_to_explain": extracted.get("stats", [])}
    except Exception as e:
        print(f"Error extracting stat entities: {str(e)}")
        return {"stats_to_explain": []}


# This function has been replaced by get_context_messages in orchestrator.py


def generate_follow_up_suggestions(memory: ConversationMemory, players: List[Dict]) -> List[str]:
    """Generate follow-up suggestions based on search results"""
    if not players:
        return ["Try a different position", "Look for players with different skills"]
    
    suggestions = []
    
    # Add player-specific suggestions
    if len(players) >= 1:
        suggestions.append(f"Tell me more about {players[0]['name']}")
    
    if len(players) >= 2:
        suggestions.append(f"Compare {players[0]['name']} and {players[1]['name']}")
    
    # Add refinement suggestions based on intent
    if memory.current_intent == "player_search":
        suggestions.append("Show me younger players")
        suggestions.append("Find players with better passing")
    
    return suggestions[:3]  # Limit to 3 suggestions