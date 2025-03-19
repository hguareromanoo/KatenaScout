"""
Compatibility module for backward compatibility

This module exists solely to maintain compatibility with older code
that may try to import from 'enhanced_chat'. It forwards all imports
to the appropriate new modules.
"""

# Forward imports from their new locations
from models.parameters import SearchParameters
from core.player_search import search_players
from core.session import UnifiedSession
from core.handlers import handle_player_search, handle_player_comparison, handle_stats_explanation

# Add any other imports that might be needed for compatibility