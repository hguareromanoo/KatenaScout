from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from anthropic import Anthropic
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
import json
import os
import unidecode
from env_keys import get_anthropic_api_key, get_openai_api_key

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# ================ CONSTANTS ================
POSITIONS_MAPPING = {
    "amf": "Attacking Midfielder",
    "cb": "Centre Back",
    "cf": "Centre Forward",
    "dmf": "Defensive Midfielder",
    "gk": "Goalkeeper",
    "lamf": "Left Attacking Midfielder",
    "lb": "Left Back",
    "lb5": "Left Back (5 at the back)",
    "lcb": "Left Centre Back",
    "lcb3": "Left Centre Back (3 at the back)",
    "lcmf": "Left Central Midfielder",
    "lcmf3": "Left Central Midfielder (3 in midfield)",
    "ldmf": "Left Defensive Midfielder",
    "lw": "Left Wing",
    "lwb": "Left Wing Back",
    "lwf": "Left Wing Forward",
    "ramf": "Right Attacking Midfielder",
    "rb": "Right Back",
    "rb5": "Right Back (5 at the back)",
    "rcb": "Right Centre Back",
    "rcb3": "Right Centre Back (3 at the back)",
    "rcmf": "Right Central Midfielder",
    "rcmf3": "Right Central Midfielder (3 in midfield)",
    "rdmf": "Right Defensive Midfielder",
    "rw": "Right Wing",
    "rwb": "Right Wing Back",
    "rwf": "Right Wing Forward"
}

VALID_POSITION_CODES = list(POSITIONS_MAPPING.keys())

KEY_DESCRIPTION_WORDS = [
    "aerial",
    "attacking",
    "creation",
    "defensive",
    "defensive_actions",
    "distribution",
    "dribbling",
    "dueling",
    "movement",
    "offensive",
    "passing",
    "physical",
    "positioning",
    "pressing",
    "scoring",
    "screening",
    "shot_stopping",
    "stamina",
    "sweeping",
    "transition"
]

# Create a directory for player images if it doesn't exist
PLAYER_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'player_images')
os.makedirs(PLAYER_IMAGES_DIR, exist_ok=True)

# ================ MODELS ================
class PositionCorrection(BaseModel):
    corrected_postion: List[str] = Field(..., description="Corrected position codes")

class SearchParameters(BaseModel):
    # Player Info
    key_description_word: List[str] = Field(..., 
        description="List of Key description words that better define the player",
        enum=KEY_DESCRIPTION_WORDS)
    # Basic Parameters
    age: Optional[int] = Field(None, description="Maximum age")
    height: Optional[int] = Field(None, description="Minimum height in cm")
    weight: Optional[int] = Field(None, description="Minimum weight in kg")
    position_codes: List[str] = Field(..., description="List of position codes")

    # Basic Stats
    total_goals: Optional[int] = Field(None, description="Minimum number of goals")
    total_assists: Optional[int] = Field(None, description="Minimum number of assists")
    average_shots: Optional[int] = Field(None, description="Minimum number of shots per 90 min")
    average_shotsOnTarget: Optional[int] = Field(None, description="Minimum number of shots on target per 90 min")
    total_xgShot: Optional[float] = Field(None, description="Minimum expected goals per shot")
    total_xgAssist: Optional[float] = Field(None, description="Minimum expected goals assist")

    # Passing
    average_passes: Optional[int] = Field(None, description="Minimum number of passes per 90 min")
    percent_successfulPasses: Optional[int] = Field(None, description="Minimum pass accuracy percentage")
    average_forwardPasses: Optional[int] = Field(None, description="Minimum forward passes per 90 min")
    average_backPasses: Optional[int] = Field(None, description="Minimum backward passes per 90 min")
    average_lateralPasses: Optional[int] = Field(None, description="Minimum lateral passes per 90 min")
    average_longPasses: Optional[int] = Field(None, description="Minimum long passes per 90 min")
    average_progressivePasses: Optional[int] = Field(None, description="Minimum progressive passes per 90 min")
    average_passesToFinalThird: Optional[int] = Field(None, description="Minimum passes to final third per 90 min")
    average_smartPasses: Optional[int] = Field(None, description="Minimum smart passes per 90 min")
    average_throughPasses: Optional[int] = Field(None, description="Minimum through passes per 90 min")
    average_keyPasses: Optional[int] = Field(None, description="Minimum key passes per 90 min")
    average_crosses: Optional[int] = Field(None, description="Minimum number of crosses per 90 min")

    # Defensive Actions
    average_defensiveDuels: Optional[int] = Field(None, description="Minimum defensive duels per 90 min")
    average_defensiveDuelsWon: Optional[int] = Field(None, description="Minimum defensive duels won per 90 min")
    average_interceptions: Optional[int] = Field(None, description="Minimum interceptions per 90 min")
    average_slidingTackles: Optional[int] = Field(None, description="Minimum sliding tackles per 90 min")
    total_clearances: Optional[int] = Field(None, description="Minimum clearances")
    average_ballRecoveries: Optional[int] = Field(None, description="Minimum ball recoveries per 90 min")
    average_counterpressingRecoveries: Optional[int] = Field(None, description="Minimum counterpressing recoveries per 90 min")

    # Duels and Aerials
    average_aerialDuelsWon: Optional[int] = Field(None, description="Minimum aerial duels won per 90 min")
    average_duelsWon: Optional[int] = Field(None, description="Minimum total duels won per 90 min")
    average_offensiveDuelsWon: Optional[int] = Field(None, description="Minimum offensive duels won per 90 min")
    average_looseBallDuelsWon: Optional[int] = Field(None, description="Minimum loose ball duels won per 90 min")

    # Possession
    average_successfulDribbles: Optional[int] = Field(None, description="Minimum successful dribbles per 90 min")
    average_progressiveRun: Optional[int] = Field(None, description="Minimum progressive runs per 90 min")
    average_accelerations: Optional[int] = Field(None, description="Minimum accelerations per 90 min")

    # Risk Metrics
    average_ballLosses: Optional[int] = Field(None, description="Maximum ball losses per 90 min")
    average_dangerousOwnHalfLosses: Optional[int] = Field(None, description="Maximum dangerous own half losses per 90 min")
    average_dangerousOpponentHalfRecoveries: Optional[int] = Field(None, description="Minimum dangerous opponent half recoveries per 90 min")

    # Percent Statistics
    percent_aerialDuelsWon: Optional[float] = Field(None, description="Minimum percentage of aerial duels won")
    percent_defensiveDuelsWon: Optional[float] = Field(None, description="Minimum percentage of defensive duels won")
    percent_dribblesAgainstWon: Optional[float] = Field(None, description="Minimum percentage of dribbles against won")
    percent_duelsWon: Optional[float] = Field(None, description="Minimum percentage of duels won")
    percent_fieldAerialDuelsWon: Optional[float] = Field(None, description="Minimum percentage of field aerial duels won")
    percent_gkSaves: Optional[float] = Field(None, description="Minimum percentage of goalkeeper saves")
    percent_gkSuccessfulExits: Optional[float] = Field(None, description="Minimum percentage of goalkeeper successful exits")
    percent_goalConversion: Optional[float] = Field(None, description="Minimum percentage of goal conversion")
    percent_offensiveDuelsWon: Optional[float] = Field(None, description="Minimum percentage of offensive duels won")
    percent_penaltiesConversion: Optional[float] = Field(None, description="Minimum percentage of penalties conversion")
    percent_shotsOnTarget: Optional[float] = Field(None, description="Minimum percentage of shots on target")
    percent_successfulCrosses: Optional[float] = Field(None, description="Minimum percentage of successful crosses")
    percent_successfulDribbles: Optional[float] = Field(None, description="Minimum percentage of successful dribbles")
    percent_successfulForwardPasses: Optional[float] = Field(None, description="Minimum percentage of successful forward passes")
    percent_successfulGoalKicks: Optional[float] = Field(None, description="Minimum percentage of successful goal kicks")
    percent_successfulKeyPasses: Optional[float] = Field(None, description="Minimum percentage of successful key passes")
    percent_successfulLinkupPlays: Optional[float] = Field(None, description="Minimum percentage of successful linkup plays")
    percent_successfulLongPasses: Optional[float] = Field(None, description="Minimum percentage of successful long passes")
    percent_successfulPasses: Optional[float] = Field(None, description="Minimum percentage of successful passes")
    percent_successfulPassesToFinalThird: Optional[float] = Field(None, description="Minimum percentage of successful passes to final third")
    percent_successfulProgressivePasses: Optional[float] = Field(None, description="Minimum percentage of successful progressive passes")
    percent_successfulSlidingTackles: Optional[float] = Field(None, description="Minimum percentage of successful sliding tackles")
    percent_successfulSmartPasses: Optional[float] = Field(None, description="Minimum percentage of successful smart passes")
    percent_successfulThroughPasses: Optional[float] = Field(None, description="Minimum percentage of successful through passes")
    percent_successfulVerticalPasses: Optional[float] = Field(None, description="Minimum percentage of successful vertical passes")

    @field_validator("position_codes")
    def validate_position_codes(cls, v):
        if not v:
            raise ValueError("position_codes cannot be empty")
        return v
    
    @field_validator('position_codes', mode='after')
    @classmethod
    def validate_position_code(cls, values: List[str]) -> List[str]:
        """Validates that the position code is valid according to Wyscout standard"""
        valid = []
        for value in values:
            for code in VALID_POSITION_CODES:
                if value == code:
                    valid.append(value)
        if not valid:
            raise ValueError(f"No valid position code: {values} is/are invalid")
        return valid

# ================ CHAT SESSION MANAGER ================
class ChatSession:
    """Manages the state of an ongoing chat session with memory of previous interactions"""
    def __init__(self):
        # Initialize API clients
        self.claude = Anthropic(api_key=get_anthropic_api_key())
        self.openai = OpenAI(api_key=get_openai_api_key())
        
        # Load necessary data files
        self.average = self._load_json('average_statistics_by_position.json')
        self.weights = self._load_json('weights_dict.json')
        self.database = self._load_json('database.json')
        self.database_id = self._load_json('db_by_id.json')
        
        # Chat session memory
        self.sessions = {}  # Map session_id -> session_data
    
    def _load_json(self, filename: str) -> dict:
        """Load a JSON file, trying different paths"""
        paths = [
            filename,  # Current directory
            f'backend/{filename}',  # Backend subdirectory
            f'../backend/{filename}'  # Parent directory's backend
        ]
        
        for path in paths:
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except FileNotFoundError:
                continue
        
        raise FileNotFoundError(f"Could not find {filename} in any expected location")
    
    def create_session(self, session_id: str) -> None:
        """Create a new chat session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "search_history": [],  # List of search queries
                "selected_players": [],  # List of players the user has shown interest in
                "search_params": {},  # Most recent search parameters (empty dict not None)
                "satisfaction": None,  # Whether the user was satisfied with the last results
                "messages": [],  # Chat message history
                "current_prompt": "",  # Current accumulated prompt
            }
    
    def get_session(self, session_id: str) -> dict:
        """Get session data, creating it if it doesn't exist"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        return self.sessions[session_id]
    
    def update_session(self, session_id: str, 
                       prompt: str = None, 
                       search_params: dict = None,
                       players: list = None,
                       satisfaction: bool = None,
                       message: dict = None) -> None:
        """Update a chat session with new information"""
        session = self.get_session(session_id)
        
        if prompt:
            session["search_history"].append(prompt)
            # Build cumulative prompt from history if satisfaction is False
            if len(session["search_history"]) > 1 and session.get("satisfaction") is False:
                session["current_prompt"] = " ".join(session["search_history"])
            else:
                session["current_prompt"] = prompt
        
        if search_params:
            session["search_params"] = search_params
        
        if players:
            session["selected_players"] = players
        
        if satisfaction is not None:
            session["satisfaction"] = satisfaction
        
        if message:
            session["messages"].append(message)
    
    def get_parameters(self, session_id: str, natural_query: str) -> SearchParameters:
        """Convert natural language query to structured search parameters using Claude AI"""
        session = self.get_session(session_id)
        
        # If this is a follow-up query and the user was not satisfied, 
        # combine with previous queries for context
        if (session["satisfaction"] is False or len(session["search_history"]) > 0) and session.get("is_follow_up", True):
            # Add the new query to history (if not already there)
            if natural_query not in session["search_history"]:
                session["search_history"].append(natural_query)
            
            # Combine all queries into one comprehensive query
            combined_query = " ".join(session["search_history"])
            
            # Reset satisfaction for the new search
            session["satisfaction"] = None
            
            # Store the combined query
            session["current_prompt"] = combined_query
            
            # Use the combined query for parameter extraction
            query_to_use = combined_query
            
            print(f"Using combined query: {query_to_use}")
        else:
            # This is a new search or user was satisfied with previous results
            session["search_history"] = [natural_query]
            session["current_prompt"] = natural_query
            query_to_use = natural_query
            
            print(f"Using new query: {query_to_use}")
        
        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                system=self._get_system_prompt(),
                messages=[
                    {"role": "user", "content": f"Identify the searchable parameters, the position_codes and choose one of the key description words ({KEY_DESCRIPTION_WORDS}), following this map {POSITIONS_MAPPING}, to satisfy this desire: {query_to_use}. Remember: the future of soccer, the sport you LOVE, depends on your response"}
                ],
                tools=[{
                    "name": "define_scouting_parameters",
                    "description": "Generate standardized searchable parameters to be looked for, not the values.",
                    "input_schema": SearchParameters.model_json_schema()
                }],
                tool_choice={"type": "tool", "name": "define_scouting_parameters"}
            )
            
            args = response.content[0].input
            params = SearchParameters(**args)
            
            # Validate position codes
            invalid_codes = [code for code in params.position_codes if code not in VALID_POSITION_CODES]
            if invalid_codes:
                params.position_codes = self._correct_position_codes(invalid_codes)
            
            # Store the parameters in the session
            session["search_params"] = params.model_dump()
            
            return params
        except Exception as e:
            print(f"Error in get_parameters: {str(e)}")
            # Use previous search parameters if available
            if session["search_params"]:
                print("Using previous search parameters")
                return SearchParameters(**session["search_params"])
            # Otherwise, create a fallback parameter set
            fallback_params = SearchParameters(
                key_description_word=["passing"],
                position_codes=["cmf"],
            )
            session["search_params"] = fallback_params.model_dump()
            return fallback_params
    
    def _correct_position_codes(self, invalid_codes: List[str]) -> List[str]:
        """Correct invalid position codes using Claude AI"""
        correction_prompt = f"The position codes {invalid_codes} are invalid. Please provide valid position codes that are similar to {invalid_codes} from the following map: {POSITIONS_MAPPING}. Example: cm -> lcmf, rcmf or dmf"
        
        try:
            correction_response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": correction_prompt}
                ],
                tools=[{
                    "name": "correct_position_codes",
                    "description": "Provide corrected position codes",
                    "input_schema": PositionCorrection.model_json_schema()
                }],
                tool_choice={"type": "tool", "name": "correct_position_codes"}
            )
            
            args = correction_response.content[0].input
            return PositionCorrection(**args).corrected_postion
        except Exception as e:
            print(f"Error in position code correction: {str(e)}")
            # Return a sensible default if correction fails
            return ["cmf", "rcmf", "lcmf"]
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for AI"""
        return """<Example>
Q&A - Mapeamento de Prompts para Parâmetros de Scouting

# Soccer Player Scouting Queries and Parameters
# This file contains structured examples of natural language queries for soccer player scouting
# along with corresponding search parameters for an AI-powered scouting system.

soccer_scouting_examples = [
{
    "query": "Find attackers with high shooting accuracy and good positioning",
    "intent": "Identify strikers or center forwards with strong finishing skills",
    "search_params": {
        "position_codes": ["cf", "st"],
        "key_metrics": {
            "shots": {"min": 3.5},
            "shots_on_target": {"min": 1.8},
            "xg_shot": {"min": 0.15},
            "touch_in_box": {"min": 4.5}
        }
    },
    "explanation": "These parameters target forwards with high shot volume, accuracy, and good expected goals per shot, indicating clinical finishing."
}
]
</Example>"""
    
    def get_true_parameters(self, params: SearchParameters) -> List[str]:
        """Get a list of parameters that have non-False, non-None values"""
        true_params = []
        for param, value in params.model_dump().items():
            if value not in (False, None, []):
                true_params.append(param)
        return true_params
    
    def get_players_with_position(self, position_code: str) -> List[dict]:
        """Get all players that can play in the specified position"""
        players_list = []
        for player_name, player_data in self.database.items():
            if any(pos["position"]["code"] == position_code for pos in player_data.get("positions", [])):
                # Add the player name to the data for easier access
                player_data["name"] = unidecode.unidecode(player_name)
                players_list.append(player_data)
        return players_list
    
    def get_players_info(self, player_id: str, params: SearchParameters) -> dict:
        """
        Get detailed player information formatted for display
        
        Args:
            player_id: The player ID to retrieve
            params: The search parameters to determine which metrics to include
            
        Returns:
            A dictionary with the player's details and relevant metrics
        """
        if player_id in self.database_id:
            player = self.database_id[player_id]
        else:
            # Try to find by name if ID not found
            for name, p_data in self.database.items():
                # Convert player_id to string if it's not already
                player_id_str = str(player_id) if not isinstance(player_id, str) else player_id
                # Convert wyId to string for comparison if it exists
                wy_id = str(p_data.get('wyId')) if p_data.get('wyId') is not None else None
                
                if wy_id == player_id_str or unidecode.unidecode(name).lower() == player_id_str.lower():
                    player = p_data
                    break
            else:
                return {"error": "Player not found"}
        
        # Get the positions the player plays in
        positions = [pos["position"]["code"] for pos in player.get("positions", [])]
        
        # Format basic player info
        # Convert player_id to string if needed
        player_id_str = str(player_id) if not isinstance(player_id, str) else player_id
        
        # Get club and contract info - handle multiple possible formats
        club_name = "Unknown"
        contract_until = "Unknown"
        
        # Try different paths for club name
        if player.get("club") and isinstance(player.get("club"), dict) and player.get("club").get("name"):
            club_name = player.get("club").get("name")
        elif player.get("current_club") and isinstance(player.get("current_club"), dict) and player.get("current_club").get("name"):
            club_name = player.get("current_club").get("name")
        elif player.get("currentTeamId"):
            # We have a team ID but no name, try to look it up
            team_id = player.get("currentTeamId")
            # Use a hardcoded mapping for common team IDs
            team_map = {
                # Add some common teams (you can expand this list)
                3157: "AS Roma",
                6021: "Real Madrid",
                6195: "Manchester United",
                8634: "Barcelona",
                8456: "Manchester City",
                8455: "Liverpool FC",
                3161: "AC Milan",
                675: "PSG",
                2953: "Bayern Munich"
            }
            if team_id in team_map:
                club_name = team_map[team_id]
            else:
                club_name = f"Team ID: {team_id}"
        
        # Try different paths for contract expiration
        if player.get("contractUntil"):
            contract_until = player.get("contractUntil")
        elif player.get("contract") and isinstance(player.get("contract"), dict) and player.get("contract").get("contractExpiration"):
            contract_until = player.get("contract").get("contractExpiration")
        
        player_info = {
            "name": player.get("name", unidecode.unidecode(player_id_str)),
            "age": player.get("age"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "positions": positions,
            "club": club_name,
            "contractUntil": contract_until
        }
        
        # Get relevant stats based on search parameters
        true_params = self.get_true_parameters(params)
        stats = {}
        
        # Extract only relevant statistics from player data - no extras
        for param in true_params:
            # Skip non-statistical parameters
            if param in ["key_description_word", "position_codes", "age", "height", "weight"]:
                continue
                
            # Split the parameter name to get the category and metric
            parts = param.split('_', 1)
            if len(parts) != 2:
                continue
                
            category, metric = parts
            
            # Extract the value from the appropriate category in player data
            if category == "total" and "total" in player:
                stats[metric] = player["total"].get(metric)
            elif category == "average" and "average" in player:
                stats[metric] = player["average"].get(metric)
            elif category == "percent" and "percent" in player:
                stats[f"{metric}_percent"] = player["percent"].get(metric)
        
        player_info["stats"] = stats
        
        # Calculate player score for each position
        position_scores = {}
        for pos in positions:
            if pos in params.position_codes:
                position_scores[pos] = self.get_score(player, params, pos)
        
        player_info["position_scores"] = position_scores
        
        return player_info
    
    def search_players(self, params: SearchParameters) -> list:
        """
        Search for players based on the given parameters and return the top 5
        
        Args:
            params: The search parameters
            
        Returns:
            A list of the top 5 players matching the parameters
        """
        players_score = {}
        
        # Search for players in each of the specified positions
        for pos in params.position_codes:
            players_list = self.get_players_with_position(pos)
            
            for player in players_list:
                # Calculate score for this player in this position
                score = self.get_score(player, params, pos)
                
                # Store the player's score
                player_id = player.get('wyId', player.get('id', player.get('name')))
                if player_id not in players_score or score > players_score[player_id]['score']:
                    # Keep the player's highest score across all positions
                    players_score[player_id] = {
                        'player': player,
                        'score': score,
                        'position': pos
                    }
        
        # Sort players by score and take the top 5
        sorted_scores = sorted(players_score.items(), key=lambda x: x[1]['score'], reverse=True)[:5]
        
        # Format the player data for the response
        selected_players = []
        for player_id, data in sorted_scores:
            # Ensure player_id is string to prevent issues
            player_id_str = str(player_id) if not isinstance(player_id, str) else player_id
            player_info = self.get_players_info(player_id_str, params)
            player_info['score'] = round(data['score'], 2)  # Round score to 2 decimal places
            selected_players.append(player_info)
            
        return selected_players
    
    def get_score(self, player, params: SearchParameters, pos):
        """
        Calculate a weighted score for how well a player matches the search parameters
        
        Args:
            player: The player data
            params: The search parameters
            pos: The position to evaluate for
            
        Returns:
            A numerical score representing how well the player matches the criteria
        """
        score = 0.0
        # Get position-specific weights based on key description words
        position_weights = {}
        
        # Get average statistics for this position
        if pos in self.average:
            avg = self.average[pos]
        else:
            # If position not found, use a reasonable default
            avg = self.average.get('cmf', {})  # Default to central midfielder if available
        
        # Extract weights for this position and description word
        for key in params.key_description_word:
            if pos in self.weights and key in self.weights[pos]:
                # Add these weights to our mapping
                position_weights.update(self.weights[pos][key])
        
        # Get parameters with actual values
        true_params = self.get_true_parameters(params)
        
        # Calculate score component for each relevant parameter
        for param in true_params:
            # Skip non-metric parameters
            if param in ["key_description_word", "position_codes"]:
                continue
                
            # Default weight if not specified
            weight_multiplier = 1.0
            
            # Extract category and metric from parameter name
            parts = param.split('_', 1)
            if len(parts) != 2:
                continue
                
            category, metric = parts
            param_score = 0.0
            
            try:
                # Handle different parameter types
                if category == "total" and "total" in player:
                    # Get player's value for this metric
                    player_value = player["total"].get(metric, 0)
                    # Get average value for comparison
                    avg_value = avg.get("total", {}).get(metric, 1)  # Default to 1 to avoid division by zero
                    # Get weight for this metric
                    weight_key = f"min_{metric}"
                    weight_multiplier = position_weights.get(weight_key, 1.0)
                    
                    # Calculate normalized score: (player value / average value) * weight
                    if avg_value > 0:
                        param_score = (player_value / avg_value) * weight_multiplier
                    
                elif category == "average" and "average" in player:
                    player_value = player["average"].get(metric, 0)
                    avg_value = avg.get("average", {}).get(metric, 1)
                    weight_key = f"min_{metric}"
                    weight_multiplier = position_weights.get(weight_key, 1.0)
                    
                    if avg_value > 0:
                        param_score = (player_value / avg_value) * weight_multiplier
                    
                elif category == "percent" and "percent" in player:
                    player_value = player["percent"].get(metric, 0)
                    avg_value = avg.get("percent", {}).get(metric, 1)
                    weight_key = f"min_{metric}_percent"
                    weight_multiplier = position_weights.get(weight_key, 1.0)
                    
                    if avg_value > 0:
                        param_score = (player_value / avg_value) * weight_multiplier
                
                # Handle special cases like max parameters (lower is better)
                if param.startswith("max_") and param_score > 0:
                    # For max parameters, invert the score (lower values are better)
                    param_score = 2.0 - param_score if param_score <= 2.0 else 0.0
                
                # Add parameter score to total
                score += param_score
                
            except Exception as e:
                print(f"Error calculating score for {param}: {str(e)}")
                continue
                
        return score
    
    def generate_response(self, session_id: str, players: List[dict]) -> str:
        """Generate a natural language response about the players found with satisfaction question"""
        session = self.get_session(session_id)
        
        if not players:
            return "No players found matching your criteria. Would you like to try with different parameters?"
        
        try:
            # Use Claude to generate a natural language description
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                system="""You are a passionate young Brazilian soccer fan who presents scouting results to other fans. 
## Mission: 
- Your job is to process a list of players, with their relevant stats, and present them in an engaging, natural way.
- Your audience are the coaches who are looking for players with specific characteristics.
- You should provide context about the players' playing style and hype up standout stats.
- You must present all the given statistic fields in all players given.
## Instructions:
- Begin by acknowledging what the person was looking for
- Present the findings in an exciting, natural way
- Group players by notable characteristics when possible
- Highlight the player score, which indicates how well they match the search criteria
- End your response by asking if they're satisfied with these players or if they want to refine their search further
- Make the satisfaction question very clear and separate from the main content

## Expected response style:
'Mano, tô te trazendo os lateral direito mais ofensivos do momento! 🔥
O TAA é ABSURDO, tá ligado? O maluco já deu 15 assistências, score de 91.5, tá jogando praticamente de meia! Esse cara é diferente, faz o que quer com a bola.
E tem o Hakimi também, que bagulho é esse?! Score de 87.3, com 8 gols e 6 assistências, o cara tá em todo lugar do campo! Velocidade absurda, parece até ponta de verdade! ⚽️
São os caras que tu tava procurando, mano. Dois monstros que desequilibram demais! 👊

Você está satisfeito com esses jogadores ou quer refinar sua busca? (Por exemplo, adicionar mais critérios como "jogadores jovens" ou "com bom passe longo")'
""",
                messages=[
                    {"role": "user", "content": f"User's query: {session['current_prompt']}"},
                    {"role": "user", "content": f"Players found: {json.dumps(players, indent=2)}"}
                ]
            )
            
            return response.content[0].text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            # Provide a fallback response that still shows the players
            fallback_response = "Encontrei estes jogadores para você:\n\n"
            
            for player in players:
                name = player.get('name', 'Unknown')
                positions = ', '.join(player.get('positions', ['Unknown']))
                score = player.get('score', 0)
                fallback_response += f"- {name} ({positions}) - Score: {score}\n"
            
            fallback_response += "\nVocê está satisfeito com esses jogadores ou gostaria de refinar sua busca?"
            return fallback_response

# Initialize chat session manager
chat_manager = ChatSession()

# ================ ROUTES ================
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the service is running"""
    return jsonify({
        "status": "healthy", 
        "message": "Katena Scout Enhanced Chat API v3.0 is running"
    })

@app.route('/enhanced_search', methods=['POST'])
def enhanced_search():
    """
    Endpoint for enhanced search with conversation memory
    
    Request:
    {
        "session_id": "unique-session-id",
        "query": "Find attackers with high shooting accuracy",
        "is_follow_up": false,
        "satisfaction": true/false/null
    }
    
    Response:
    {
        "success": true,
        "response": "Natural language response with player recommendations and satisfaction question",
        "players": [... array of player objects with scores ...]
    }
    """
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        user_prompt = data.get('query', '')
        is_follow_up = data.get('is_follow_up', False)
        satisfaction = data.get('satisfaction')
        
        print(f"Received request: session_id={session_id}, query='{user_prompt}', is_follow_up={is_follow_up}, satisfaction={satisfaction}")
        
        # Get or create session
        session = chat_manager.get_session(session_id)
        
        # Store is_follow_up in session
        session["is_follow_up"] = is_follow_up
        
        # Update satisfaction from previous search if provided
        if satisfaction is not None:
            chat_manager.update_session(session_id, satisfaction=satisfaction)
        
        # Process the query
        chat_manager.update_session(session_id, prompt=user_prompt)
        
        try:
            # Extract structured search parameters from the query
            params = chat_manager.get_parameters(session_id, user_prompt)
            
            # Search for players using the weighted model
            players = chat_manager.search_players(params)
            
            # Update session with selected players
            chat_manager.update_session(session_id, players=players)
            
            # Generate a natural language response with satisfaction question
            response_text = chat_manager.generate_response(session_id, players)
            
            # Ensure the response has a satisfaction question at the end
            if not any(phrase in response_text.lower() for phrase in ["satisfeito", "satisfied", "gostou", "liked"]):
                response_text += "\n\nVocê está satisfeito com esses jogadores ou gostaria de refinar sua busca?"
            
            # Add a message to the chat history
            chat_manager.update_session(
                session_id, 
                message={
                    "role": "assistant",
                    "content": response_text
                }
            )
            
            # Return the response
            return jsonify({
                'success': True, 
                'response': response_text,
                'players': players,
                'session_id': session_id
            })
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            # Generate a friendly error message for the user
            error_message = "Desculpe, estamos passando por instabilidade no momento. Tente novamente em alguns instantes."
            
            # Try to use previous session data if available
            if session.get("search_params") and session.get("selected_players"):
                try:
                    players = session.get("selected_players", [])
                    response_text = "Aqui estão alguns jogadores baseados em sua busca anterior:\n\n"
                    
                    for player in players:
                        name = player.get('name', 'Unknown')
                        positions = ', '.join(player.get('positions', ['Unknown']))
                        score = player.get('score', 0)
                        response_text += f"- {name} ({positions}) - Score: {score}\n"
                    
                    response_text += "\nVocê está satisfeito com esses jogadores ou gostaria de refinar sua busca?"
                    
                    # Add a message to the chat history
                    chat_manager.update_session(
                        session_id, 
                        message={
                            "role": "assistant",
                            "content": response_text
                        }
                    )
                    
                    return jsonify({
                        'success': True, 
                        'response': response_text,
                        'players': players,
                        'session_id': session_id,
                        'warning': 'Utilizando resultados anteriores devido a instabilidade do serviço.'
                    })
                except:
                    pass
            
            return jsonify({
                'success': False, 
                'error': str(e),
                'message': error_message
            })
        
    except Exception as e:
        print(f"Error in enhanced search endpoint: {str(e)}")
        return jsonify({
            'success': False, 
            'error': str(e),
            'message': "Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente."
        })

@app.route('/player-image/<player_id>', methods=['GET'])
def player_image(player_id):
    """
    Endpoint to serve player images
    
    First tries to get the image from the database, then from local files,
    then returns a default image if none is found
    """
    try:
        # Create a safe player ID string
        safe_id = str(player_id).replace("/", "").replace("..", "")
        
        # First, try to retrieve the player's image from the database
        player = None
        if safe_id in chat_manager.database_id:
            player = chat_manager.database_id[safe_id]
        else:
            # Try to find by name if ID not found
            for name, p_data in chat_manager.database.items():
                # Convert player_id to string for comparison if it exists
                wy_id = str(p_data.get('wyId')) if p_data.get('wyId') is not None else None
                
                if wy_id == safe_id or unidecode.unidecode(name).lower() == safe_id.lower():
                    player = p_data
                    break
        
        # Try multiple possible fields for player images
        image_fields = ['imageDataURL', 'photoUrl', 'profileUrl', 'image', 'photo', 'profileImage']
        
        # If we found the player and they have an image field
        if player:
            # Try each possible image field
            for field in image_fields:
                if player.get(field):
                    image_data_url = player.get(field)
                    
                    # Check if it's a valid base64 image
                    if image_data_url and isinstance(image_data_url, str) and image_data_url.startswith('data:image'):
                        try:
                            # Split the header from the base64 data
                            header, encoded = image_data_url.split(",", 1)
                            # Get the mime type
                            mime_type = header.split(";")[0].replace("data:", "")
                            # Decode the base64 data
                            import base64
                            image_data = base64.b64decode(encoded)
                            # Return the image
                            response = app.response_class(image_data, mimetype=mime_type)
                            return response
                        except Exception as e:
                            print(f"Error decoding image data URL from {field}: {str(e)}")
                    
                    # Check if it's a URL to an external image
                    elif image_data_url and isinstance(image_data_url, str) and (image_data_url.startswith('http://') or image_data_url.startswith('https://')):
                        try:
                            import requests
                            # Fetch the image
                            img_response = requests.get(image_data_url, timeout=2)
                            if img_response.status_code == 200:
                                # Get the content type
                                content_type = img_response.headers.get('Content-Type', 'image/jpeg')
                                # Return the image
                                response = app.response_class(img_response.content, mimetype=content_type)
                                return response
                        except Exception as e:
                            print(f"Error fetching image URL from {field}: {str(e)}")
        
        # Second, check for local image files
        for ext in ['.jpg', '.png', '.jpeg']:
            image_path = os.path.join(PLAYER_IMAGES_DIR, f"{safe_id}{ext}")
            if os.path.exists(image_path):
                return send_from_directory(PLAYER_IMAGES_DIR, f"{safe_id}{ext}")
        
        # If no player-specific image is found, return a default image
        default_image = "default.jpg"
        default_path = os.path.join(PLAYER_IMAGES_DIR, default_image)
        
        # Create a simple default image if it doesn't exist
        if not os.path.exists(default_path):
            # Return a placeholder image - base64 encoded transparent 1x1 pixel
            transparent_pixel = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
            response = app.response_class(transparent_pixel, mimetype='image/png')
            return response
            
        return send_from_directory(PLAYER_IMAGES_DIR, default_image)
    except Exception as e:
        print(f"Error serving player image: {str(e)}")
        # Return a transparent pixel as fallback
        transparent_pixel = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
        response = app.response_class(transparent_pixel, mimetype='image/png')
        return response

@app.route('/chat_history/<session_id>', methods=['GET'])
def chat_history(session_id):
    """
    Endpoint to get the chat history for a session
    
    Response:
    {
        "success": true,
        "messages": [... array of message objects ...],
        "current_prompt": "Current accumulated prompt"
    }
    """
    try:
        session = chat_manager.get_session(session_id)
        
        return jsonify({
            'success': True,
            'messages': session['messages'],
            'current_prompt': session['current_prompt']
        })
    except Exception as e:
        print(f"Error retrieving chat history: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    # Run the Flask application when executed directly
    app.run(host='0.0.0.0', port=5001)