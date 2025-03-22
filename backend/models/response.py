"""
Response models for KatenaScout API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from models.player import PlayerSummary

class SearchResponse(BaseModel):
    """Response model for player search endpoint"""
    success: bool = Field(True, description="Whether the request was successful")
    response: str = Field(..., description="Natural language response with player recommendations")
    satisfaction_question: str = Field(..., description="Question asking if user is satisfied with results")
    players: List[PlayerSummary] = Field(default_factory=list, description="Array of player objects with scores")
    language: str = Field("english", description="Language of the response")
    follow_up_suggestions: Optional[List[str]] = Field(None, description="Suggested follow-up queries")

class ComparisonResponse(BaseModel):
    """Response model for player comparison endpoint"""
    success: bool = Field(True, description="Whether the request was successful")
    comparison: Optional[str] = Field(None, description="Natural language comparison of the players")
    comparison_aspects: List[str] = Field(default_factory=list, description="Aspects compared (e.g., 'Passing', 'Shooting')")
    players: List[PlayerSummary] = Field(default_factory=list, description="Array of player objects")
    language: str = Field("english", description="Language of the response")
    metric_winners: Dict[str, str] = Field(default_factory=dict, description="Winner for each metric ('player1', 'player2', or 'tie')")
    overall_winner: Dict[str, Any] = Field(default_factory=dict, description="Overall winner information")
    categorized_metrics: Dict[str, List[str]] = Field(default_factory=dict, description="Metrics organized by category")
    category_winners: Dict[str, str] = Field(default_factory=dict, description="Winner for each category")
    negative_metrics: List[str] = Field(default_factory=list, description="Metrics where lower values are better")

class PlayerTacticalAnalysis(BaseModel):
    """Analysis of a player's tactical fit"""
    name: str = Field(..., description="Player name")
    description: str = Field(..., description="Description of player's strengths and weaknesses in the tactical system")
    fit_score: float = Field(..., description="Tactical fit score (0-100)")
    key_strengths: List[str] = Field(default_factory=list, description="Key strengths in this tactical system")
    key_weaknesses: List[str] = Field(default_factory=list, description="Key weaknesses in this tactical system")

class TacticalAnalysisResponse(BaseModel):
    """Response model for tactical analysis"""
    success: bool = Field(True, description="Whether the request was successful")
    tactical_description: str = Field(..., description="Explanation of the tactical system and requirements for the players' positions")
    players: List[PlayerTacticalAnalysis] = Field(..., description="Analysis of each player")
    winner: str = Field(..., description="Name of the player who best fits the tactical system")
    language: str = Field("english", description="Language of the response")
    playing_style: str = Field(..., description="The playing style analyzed")
    formation: str = Field(..., description="The formation analyzed")
    comparison_text: str = Field(..., description="Full tactical comparison text from the AI")

class ErrorResponse(BaseModel):
    """Response model for error responses"""
    success: bool = Field(False, description="Request was not successful")
    error: str = Field(..., description="Error code or brief description")
    message: str = Field(..., description="Human-readable error message")
    language: str = Field("english", description="Language of the error message")

class LanguagesResponse(BaseModel):
    """Response model for languages endpoint"""
    success: bool = Field(True, description="Whether the request was successful")
    languages: Dict[str, Dict[str, str]] = Field(..., description="Available languages and their metadata")
    default: str = Field("english", description="Default language")