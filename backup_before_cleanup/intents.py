"""
Intent recognition and handling for the KatenaScout conversation orchestrator
"""

from typing import Dict, List, Any
import json
from .models import ConversationMemory, Intent


def identify_intent(memory: ConversationMemory, message: str, call_claude_api) -> Intent:
    """
    Identify the user's intent from a message using Claude API
    
    Args:
        memory: The conversation memory
        message: The user message
        call_claude_api: Function to call Claude API
        
    Returns:
        Intent object with name and confidence
    """
    messages = create_context_from_memory(memory)
    messages.append({"role": "user", "content": message})
    
    system_prompt = """
    Identify the user's intent from their message. The user is interacting with a football scouting application.
    
    Available intents:
    - player_search: User wants to find players matching specific criteria (e.g., "Find attackers with high shooting accuracy")
    - player_comparison: User wants to compare multiple players (e.g., "Compare these two strikers")
    - explain_stats: User wants explanation of statistics or metrics (e.g., "What is xG?")
    - casual_conversation: General chat not related to specific player search (e.g., "Hello", "Thank you")
    - other: None of the above
    
    Analyze the message context and determine the most likely intent.
    """
    
    response = call_claude_api(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
        tools=[{
            "name": "classify_intent",
            "description": "Classify the user's intent",
            "input_schema": Intent.model_json_schema()
        }],
        tool_choice={"type": "tool", "name": "classify_intent"}
    )
    
    return Intent(**response.content[0].input)


def extract_entities(memory: ConversationMemory, message: str, intent: Intent, call_claude_api) -> Dict[str, Any]:
    """
    Extract relevant entities from a user message based on intent
    
    Args:
        memory: The conversation memory
        message: The user message
        intent: The identified intent
        call_claude_api: Function to call Claude API
        
    Returns:
        Dictionary of extracted entities
    """
    # Different entity extraction based on intent type
    if intent.name == "player_search":
        return {}  # Handled by existing parameter extraction
    elif intent.name == "player_comparison":
        return extract_player_entities(memory, message, call_claude_api)
    elif intent.name == "explain_stats":
        return extract_stat_entities(memory, message, call_claude_api)
    else:
        return {}  # No specific entities for casual conversation or other


def extract_player_entities(memory: ConversationMemory, message: str, call_claude_api) -> Dict[str, Any]:
    """Extract player names for comparison"""
    system_prompt = """
    Extract the names of football players mentioned in the message for comparison.
    If specific players are not mentioned by name but referenced (e.g., "these two players"), 
    use the conversation context to determine which players are being discussed.
    """
    
    messages = create_context_from_memory(memory)
    messages.append({"role": "user", "content": message})
    
    # Define tool schema for player extraction
    schema = {
        "type": "object",
        "properties": {
            "players": {
                "type": "array",
                "description": "List of player names mentioned",
                "items": {"type": "string"}
            }
        },
        "required": ["players"]
    }
    
    response = call_claude_api(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
        tools=[{
            "name": "extract_players",
            "description": "Extract player names for comparison",
            "input_schema": schema
        }],
        tool_choice={"type": "tool", "name": "extract_players"}
    )
    
    extracted = response.content[0].input
    return {"players_to_compare": extracted.get("players", [])}


def extract_stat_entities(memory: ConversationMemory, message: str, call_claude_api) -> Dict[str, Any]:
    """Extract statistics or metrics mentioned for explanation"""
    system_prompt = """
    Extract the football statistics or metrics mentioned in the message that the user wants explained.
    Common football metrics include:
    - xG (expected goals)
    - Passing accuracy
    - Progressive passes
    - Defensive duels
    - Ball recoveries
    - And many others
    """
    
    messages = create_context_from_memory(memory)
    messages.append({"role": "user", "content": message})
    
    # Define tool schema for stat extraction
    schema = {
        "type": "object",
        "properties": {
            "stats": {
                "type": "array",
                "description": "List of statistics or metrics mentioned",
                "items": {"type": "string"}
            }
        },
        "required": ["stats"]
    }
    
    response = call_claude_api(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
        tools=[{
            "name": "extract_stats",
            "description": "Extract statistics or metrics for explanation",
            "input_schema": schema
        }],
        tool_choice={"type": "tool", "name": "extract_stats"}
    )
    
    extracted = response.content[0].input
    return {"stats_to_explain": extracted.get("stats", [])}


def create_context_from_memory(memory: ConversationMemory) -> List[Dict[str, str]]:
    """Create a context for Claude API from conversation memory"""
    # Include last 5 messages for context
    return memory.messages[-5:] if len(memory.messages) > 0 else []


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