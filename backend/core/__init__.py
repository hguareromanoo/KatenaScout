"""
Core module for KatenaScout backend
"""
# Import all core modules using absolute imports
from core.session import UnifiedSession
from core.intent import identify_intent, extract_entities, generate_follow_up_suggestions
from core.player_search import search_players, get_score, get_player_info
from core.comparison import compare_players, find_players_for_comparison
from core.handlers import (
    handle_player_search, 
    handle_player_comparison, 
    handle_stats_explanation, 
    handle_casual_chat, 
    handle_fallback
)