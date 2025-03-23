"""
Parameter models for KatenaScout

This module contains all parameter-related models for the application,
ensuring a single source of truth for parameter definitions.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal

# Constants - will be moved to config.py later
KEY_DESCRIPTION_WORDS = [
    "scoring", "playmaking", "passing", "dribbling", "offensive", "defensive", 
    "aerial", "pressing", "creation", "defensive_actions", "distribution", 
    "positioning", "stamina", "transition", "sweeping"
]

class PositionCorrection(BaseModel):
    """Model for correcting invalid position codes"""
    corrected_postion: List[str] = Field(..., description="Corrected position codes")

class SearchParameters(BaseModel):
    """
    Comprehensive model for player search parameters
    
    This is the single source of truth for all search parameters in the application.
    All parameter extraction should produce an instance of this model.
    """
    # Player Info
    key_description_word: List[str] = Field(default=["passing"], 
        description="List of key description words that better define the player",
        enum=KEY_DESCRIPTION_WORDS)
    
    # Basic Parameters
    age: Optional[int] = Field(None, description="Maximum age")
    height: Optional[int] = Field(None, description="Minimum height in cm")
    weight: Optional[int] = Field(None, description="Minimum weight in kg")
    position_codes: List[str] = Field(default=["cmf"], description="List of position codes")
    foot: Literal["left", "right", "both"] = Field("both", description="Preferred foot")
    contract_expiration: Optional[str] = Field(None, description="Maximum contract expiration date (YYYY-MM-DD)")
    
    # Name search parameters - used for finding specific players
    player_name: Optional[str] = Field(None, description="Player name to search for")
    is_name_search: Optional[bool] = Field(False, description="Whether this is a search by player name")
    
    # Basic Stats
    total_goals: Optional[bool] = Field(None, description="Total goals scored")
    total_assists: Optional[bool] = Field(None, description="Total assists provided")
    average_shots: Optional[bool] = Field(None, description="Average shots per 90 min")
    average_shotsOnTarget: Optional[bool] = Field(None, description="Average shots on target per 90 min")
    total_xgShot: Optional[bool] = Field(None, description="Total expected goals per shot")
    total_xgAssist: Optional[bool] = Field(None, description="Total expected goals assist")
    percent_goalConversion: Optional[bool] = Field(None, description="Goal conversion rate (percentage)")
    percent_shotsOnTarget: Optional[bool] = Field(None, description="Shots on target percentage")

    # Passing
    average_passes: Optional[bool] = Field(None, description="Average passes per 90 min")
    percent_successfulPasses: Optional[bool] = Field(None, description="Pass accuracy percentage")
    average_forwardPasses: Optional[bool] = Field(None, description="Average forward passes per 90 min")
    average_backPasses: Optional[bool] = Field(None, description="Average backward passes per 90 min")
    average_lateralPasses: Optional[bool] = Field(None, description="Average lateral passes per 90 min")
    average_longPasses: Optional[bool] = Field(None, description="Average long passes per 90 min")
    percent_successfulLongPasses: Optional[bool] = Field(None, description="Long pass accuracy percentage")
    average_progressivePasses: Optional[bool] = Field(None, description="Average progressive passes per 90 min")
    average_passesToFinalThird: Optional[bool] = Field(None, description="Average passes to final third per 90 min")
    average_smartPasses: Optional[bool] = Field(None, description="Average smart passes per 90 min")
    average_throughPasses: Optional[bool] = Field(None, description="Average through passes per 90 min")
    average_keyPasses: Optional[bool] = Field(None, description="Average key passes per 90 min")
    average_crosses: Optional[bool] = Field(None, description="Average crosses per 90 min")
    percent_successfulCrosses: Optional[bool] = Field(None, description="Cross accuracy percentage")

    # Defensive Actions
    average_defensiveDuels: Optional[bool] = Field(None, description="Average defensive duels per 90 min")
    percent_defensiveDuelsWon: Optional[bool] = Field(None, description="Defensive duels win percentage")
    average_defensiveDuelsWon: Optional[bool] = Field(None, description="Average defensive duels won per 90 min")
    average_interceptions: Optional[bool] = Field(None, description="Average interceptions per 90 min")
    average_slidingTackles: Optional[bool] = Field(None, description="Average sliding tackles per 90 min")
    percent_successfulSlidingTackles: Optional[bool] = Field(None, description="Sliding tackles success percentage")
    total_clearances: Optional[bool] = Field(None, description="Total clearances")
    average_ballRecoveries: Optional[bool] = Field(None, description="Average ball recoveries per 90 min")
    average_dangerousOpponentHalfRecoveries: Optional[bool] = Field(None, description="Dangerous opponent half recoveries per 90 min")
    average_counterpressingRecoveries: Optional[bool] = Field(None, description="Counterpressing recoveries per 90 min")
    average_goalkeeperExitsPerformed: Optional[bool] = Field(None, description="Goalkeeper exits performed per 90 min")
    percent_gkSuccessfulExits: Optional[bool] = Field(None, description="Goalkeeper successful exits percentage")
    
    # Possession & Dribbling
    average_successfulDribbles: Optional[bool] = Field(None, description="Successful dribbles per 90 min")
    percent_successfulDribbles: Optional[bool] = Field(None, description="Dribble success percentage")
    average_progressiveRun: Optional[bool] = Field(None, description="Progressive runs per 90 min")
    average_offensiveDuelsWon: Optional[bool] = Field(None, description="Offensive duels won per 90 min")
    percent_offensiveDuelsWon: Optional[bool] = Field(None, description="Offensive duels win percentage")
    average_ballLosses: Optional[bool] = Field(None, description="Ball losses per 90 min")
    average_dangerousOwnHalfLosses: Optional[bool] = Field(None, description="Dangerous own half losses per 90 min")
    
    # Physical
    average_accelerations: Optional[bool] = Field(None, description="Accelerations per 90 min")
    average_aerialDuelsWon: Optional[bool] = Field(None, description="Aerial duels won per 90 min")
    percent_aerialDuelsWon: Optional[bool] = Field(None, description="Aerial duels win percentage")
    average_duelsWon: Optional[bool] = Field(None, description="Total duels won per 90 min")
    percent_duelsWon: Optional[bool] = Field(None, description="Total duels win percentage")
    
    # Goalkeeper
    percent_gkSaves: Optional[bool] = Field(None, description="Goalkeeper save percentage")
    average_gkSaves: Optional[bool] = Field(None, description="Goalkeeper saves per 90 min")
    percent_successfulGoalKicks: Optional[bool] = Field(None, description="Successful goal kicks percentage")

    def get_true_parameters(self) -> List[str]:
        """Get a list of parameters that have non-False, non-None, non-empty values"""
        true_params = []
        for param, value in self.model_dump().items():
            if value not in (False, None, []):
                true_params.append(param)
        return true_params
    
    @classmethod
    def create_default(cls) -> 'SearchParameters':
        """Create a default SearchParameters instance with sensible defaults"""
        return cls(
            key_description_word=["passing"],
            position_codes=["cmf"],
        )

class SearchRequest(BaseModel):
    """
    Model for search request payload
    
    This standardizes the input for search requests across the application.
    """
    session_id: str = Field(..., description="Unique session identifier")
    query: str = Field(..., description="Natural language search query")
    is_follow_up: bool = Field(False, description="Whether this is a follow-up to a previous query")
    satisfaction: Optional[bool] = Field(None, description="User satisfaction with previous results (null if not provided)")
    language: str = Field("english", description="Language for the response")

class ComparisonRequest(BaseModel):
    """
    Model for player comparison request payload
    
    This standardizes the input for comparison requests across the application.
    """
    session_id: str = Field(..., description="Unique session identifier")
    player_ids: List[str] = Field(..., min_items=2, description="List of player IDs to compare")
    language: str = Field("english", description="Language for the response")