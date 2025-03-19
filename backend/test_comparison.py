"""
Test script for player comparison functionality
"""

import json
import os
import sys

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary modules with absolute imports
from models.parameters import SearchParameters
from services.data_service import get_player_database, get_player_database_by_id
from core.player_search import get_player_info
from core.comparison import compare_players, find_players_for_comparison

# Mock session manager for testing
class MockSessionManager:
    def __init__(self):
        self.database = get_player_database()
        self.database_id = get_player_database_by_id()
    
    def call_claude_api(self, **kwargs):
        # Mock Claude API response
        class MockContent:
            def __init__(self, text):
                self.text = text
        
        class MockResponse:
            def __init__(self, content):
                self.content = content
        
        # Create mock content with comparison text
        comparison_text = """
        # Comparison of Players
        
        ## Player 1
        Player 1 is a talented midfielder with excellent passing ability. Their key strengths are:
        - Great vision
        - Technical skills
        - Tactical awareness
        
        ## Player 2
        Player 2 is a strong defender with solid positioning. Their key strengths are:
        - Physical presence
        - Aerial ability
        - Tackling
        
        ## Overall Comparison
        Player 1 is better in possession while Player 2 excels defensively.
        """
        
        mock_content = [MockContent(comparison_text)]
        return MockResponse(mock_content)

def test_player_comparison():
    """Test the player comparison functionality"""
    print("Testing player comparison functionality...\n")
    
    # Initialize mock session manager
    session_manager = MockSessionManager()
    
    # Find two players to compare (can be hardcoded IDs from your database)
    # Example: searching by position to find players
    db = get_player_database()
    player_ids = []
    
    # Print the number of players in the database
    print(f"Total players in database: {len(db)}")
    
    # Find any two players with wyId
    counter = 0
    for player_name, player_data in db.items():
        if 'wyId' in player_data:
            player_ids.append(str(player_data['wyId']))
            print(f"Found player {counter+1}: {player_name} (ID: {player_data['wyId']})")
            counter += 1
            if counter >= 2:
                break
    
    if len(player_ids) < 2:
        print("Could not find enough players to compare")
        return
    
    # Create a simple search parameters object
    params = SearchParameters(
        key_description_word=["passing"],
        position_codes=["cmf", "cb"]
    )
    
    # Get full player information
    players = []
    for player_id in player_ids:
        # Get database information for testing
        database = get_player_database()
        database_id = get_player_database_by_id()
        
        # Call with proper parameters
        player_info = get_player_info(
            player_id=player_id,
            database=database,
            database_id=database_id,
            params=params
        )
        if 'error' not in player_info:
            players.append(player_info)
    
    print(f"\nFound {len(players)} players for comparison")
    
    # Run comparison
    comparison_result = compare_players(
        players=players,
        session_manager=session_manager,
        language="english"
    )
    
    print("\nComparison result:")
    print(f"Comparison text length: {len(comparison_result['comparison'])} characters")
    print(f"Comparison aspects: {', '.join(comparison_result['comparison_aspects'])}")
    
    # Print snippet of comparison text
    text_preview = comparison_result['comparison'][:200] + "..." if len(comparison_result['comparison']) > 200 else comparison_result['comparison']
    print(f"\nComparison text preview:\n{text_preview}")
    
    print("\nPlayer comparison test completed successfully!")

if __name__ == "__main__":
    test_player_comparison()