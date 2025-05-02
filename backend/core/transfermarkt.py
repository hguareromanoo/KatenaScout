# app/utils/player_data.py
from typing import List, Optional
import sys
import os



# Adiciona o diretório transfermarkt-api ao caminho de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'transfermarkt-api')))

# Agora as importações funcionarão
from transfermarktApi.main.schemas.players.injuries import Injury
# ...
from pydantic import BaseModel

# Import existing schemas
from transfermarktApi.main.schemas.players.injuries import Injury
from transfermarktApi.main.schemas.players.market_value import MarketValueHistory
from transfermarktApi.main.schemas.players.transfers import PlayerTransfer

# Import existing services
from transfermarktApi.main.services.players.search import TransfermarktPlayerSearch
from transfermarktApi.main.services.players.injuries import TransfermarktPlayerInjuries
from transfermarktApi.main.services.players.market_value import TransfermarktPlayerMarketValue
from transfermarktApi.main.services.players.transfers import TransfermarktPlayerTransfers


class PlayerData(BaseModel):
    """Combined player data including injuries, market value, and transfers."""
    player_id: str
    injuries: List[Injury]
    market_value_history: List[MarketValueHistory]
    transfers: List[PlayerTransfer]


def get_player_data(player_name: str) -> Optional[PlayerData]:
    """
    Fetches combined data (injuries, market value, transfers) for a given player name.

    Args:
        player_name: The name of the player to search for.

    Returns:
        A PlayerData object containing the combined data, or None if the player is not found
        or an error occurs during fetching.
    """
    try:
        # 1. Search for the player to get the ID
        search_service = TransfermarktPlayerSearch(query=player_name)
        search_results = search_service.search_players()

        # Check if the dictionary or the 'results' key is empty/missing
        if not search_results or not search_results.get('results'):
            print(f"Player '{player_name}' not found.")
            return None

        # Use the first result's ID (dictionary access)
        player_id = search_results['results'][0]['id']
        print(f"Found player ID for '{player_name}': {player_id}")

        # 2. Fetch Injuries
        injury_service = TransfermarktPlayerInjuries(player_id=player_id)
        injury_data = injury_service.get_player_injuries()
        print(f"Fetched injury data for player ID {player_id}")


        # 3. Fetch Market Value
        market_value_service = TransfermarktPlayerMarketValue(player_id=player_id)
        market_value_data = market_value_service.get_player_market_value()
        print(f"Fetched market value data for player ID {player_id}")


        # 4. Fetch Transfers
        transfer_service = TransfermarktPlayerTransfers(player_id=player_id)
        transfer_data = transfer_service.get_player_transfers()
        print(f"Fetched transfer data for player ID {player_id}")


        # 5. Combine data into the Pydantic model (using dictionary access)
        player_data = PlayerData(
            player_id=player_id,
            injuries=injury_data.get('injuries', []) if injury_data else [],
            market_value_history=market_value_data.get('marketValueHistory', []) if market_value_data else [],
            transfers=transfer_data.get('transfers', []) if transfer_data else [],
        )

        return player_data

    except Exception as e:
        print(f"An error occurred while fetching data for '{player_name}': {e}")
        return None

# Example Usage (can be removed or kept for testing)


# player_visualization.py

import os
import json
from datetime import datetime, date
import re

class PlayerVisualizationModule:
    """Module for generating visualizations of player data"""
    
    def __init__(self):
        """Initialize the visualization module"""
        self.output_base_dir = "player_reports"
    
    def generate_visualizations(self, player_data, output_dir=None):
        """
        Generate visualizations for a player and return paths to the outputs
        
        Args:
            player_data: PlayerData object containing player information
            output_dir: Optional custom output directory
            
        Returns:
            Dictionary with paths to generated files and processed data
        """
        # Set output directory
        if output_dir is None:
            player_name = getattr(player_data, 'name', player_data.player_id)
            output_dir = os.path.join(self.output_base_dir, str(player_name).replace(" ", "_"))
        
        # Create the output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Process the player data into a standardized format
        processed_data = self._process_player_data(player_data)
        
        # Save the processed data as JSON
        json_path = os.path.join(output_dir, "player_visualization_data.json")
        with open(json_path, 'w') as f:
            json.dump(processed_data, f)
        
        # Generate the visualization HTML
       
        
        # Return the paths for integration with other modules
        return {
            "processed_data": processed_data,
            "json_path": json_path,
            "output_dir": output_dir
        }
    
    def _process_player_data(self, player_data):
        """
        Process player data into a standardized format for visualization
        
        Args:
            player_data: PlayerData object
            
        Returns:
            Dictionary with processed data
        """
        # Initialize data structure
        processed_data = {
            "player_id": player_data.player_id,
            "injuries": self._process_injuries(player_data.injuries),
            "market_values": self._process_market_values(player_data.market_value_history),
            "transfers": self._process_transfers(player_data.transfers),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "data_types": ["injuries", "market_values", "transfers"]
            }
        }
        
        return processed_data
    
    def _process_injuries(self, injuries):
        """Process injury data"""
        processed_injuries = []
        
        for injury in injuries:
            # Handle date formatting
            if injury.from_date:
                from_date = self._format_date(injury.from_date)
            else:
                from_date = "Unknown"
                
            if injury.until_date:
                until_date = self._format_date(injury.until_date)
            else:
                until_date = "Unknown"
            
            # Calculate duration if possible
            duration = self._calculate_duration(injury.from_date, injury.until_date)
            
            processed_injuries.append({
                "type": injury.injury,
                "from_date": from_date,
                "until_date": until_date,
                "duration": duration,
                "days_missed": getattr(injury, "days_missed", duration)
            })
        
        return processed_injuries
    
    def _process_market_values(self, market_values):
        """Process market value data"""
        processed_values = []
        
        for mv in market_values:
            date_str = self._format_date(getattr(mv, "date", None))
            value_str = getattr(mv, "market_value", "Unknown")
            
            # Parse value to numeric for charts
            value_numeric = self._parse_currency_value(value_str)
                
            processed_values.append({
                "date": date_str,
                "value_display": value_str,
                "value_numeric": value_numeric,
                "club": getattr(mv, "club_name", "Unknown")
            })
        
        # Sort by date
        processed_values = self._sort_by_date(processed_values)
        
        return processed_values
    
    def _process_transfers(self, transfers):
        """Process transfer data"""
        processed_transfers = []
        
        for transfer in transfers:
            date_str = self._format_date(getattr(transfer, "date", None))
                
            from_club = "Unknown"
            if hasattr(transfer, "club_from"):
                club_from = transfer.club_from
                from_club = getattr(club_from, "name", "Unknown")
                
            to_club = "Unknown"
            if hasattr(transfer, "club_to"):
                club_to = transfer.club_to
                to_club = getattr(club_to, "name", "Unknown")
            
            fee_str = getattr(transfer, "fee", "Unknown")
            fee_numeric = self._parse_currency_value(fee_str)
            is_loan = isinstance(fee_str, str) and "loan" in fee_str.lower()
            
            processed_transfers.append({
                "date": date_str,
                "from_club": from_club,
                "to_club": to_club,
                "fee_display": fee_str,
                "fee_numeric": fee_numeric,
                "is_loan": is_loan
            })
        
        # Sort by date
        processed_transfers = self._sort_by_date(processed_transfers)
        
        return processed_transfers
    
    def _format_date(self, date_obj):
        """Format date objects to strings consistently"""
        if date_obj is None:
            return "Unknown"
            
        if hasattr(date_obj, "strftime"):
            return date_obj.strftime("%Y-%m-%d")
        
        return str(date_obj)
    
    def _calculate_duration(self, start_date, end_date):
        """Calculate duration between two dates in days"""
        if not start_date or not end_date:
            return "Unknown"
            
        try:
            if hasattr(start_date, "toordinal") and hasattr(end_date, "toordinal"):
                return (end_date - start_date).days
                
            # Try parsing strings
            start_str = self._format_date(start_date)
            end_str = self._format_date(end_date)
            
            if start_str != "Unknown" and end_str != "Unknown":
                start = datetime.strptime(start_str, "%Y-%m-%d")
                end = datetime.strptime(end_str, "%Y-%m-%d")
                return (end - start).days
        except Exception as e:
            print(f"Error calculating duration: {e}")
            
        return "Unknown"
    
    def _parse_currency_value(self, value_str):
        """Parse currency string to numeric value in millions"""
        if not isinstance(value_str, str):
            return 0
            
        # Handle special cases
        if "free transfer" in value_str.lower() or "loan" in value_str.lower():
            return 0
        
        # Extract numeric value with regex
        match = re.search(r'[€$£]?([0-9,.]+)([mk])?', value_str.lower())
        if match:
            value_str = match.group(1).replace(',', '.')
            try:
                value = float(value_str)
                
                # Apply unit multiplier
                unit = match.group(2)
                if unit == 'm':
                    return value
                elif unit == 'k':
                    return value / 1000
                else:
                    return value / 1000000
            except ValueError:
                return 0
        
        return 0
    
    def _sort_by_date(self, items):
        """Sort a list of dictionaries by date field"""
        try:
            return sorted(
                items, 
                key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d') if x['date'] != "Unknown" else datetime.min
            )
        except Exception as e:
            print(f"Warning: Could not sort by date - {e}")
            return items
    
    

