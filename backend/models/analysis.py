from pydantic import BaseModel , Field
from typing import List, Dict, Any, Optional, Literal
from models.player import Player

##### Tactical FIt Analysis #####
class ProfileFitDetails(BaseModel):
    """Details for a single tactical profile fit"""
    score: int = Field(..., description="Fit score from 0-100")
    description: str = Field(..., description="Description of the tactical profile")
    category: str = Field(..., description="Qualitative category of fit (Excelente, Bom, etc)")
    position: str = Field(..., description="Position code (cf, lw, etc)")
    position_type: str = Field(..., description="Position category (center_forwards, wingers, etc)")
    
class TacticalProfileFit(BaseModel):
    """A complete profile fit with position information"""
    position: str = Field(..., description="Position code")
    position_type: str = Field(..., description="Position category")
    profile: str = Field(..., description="Profile name")
    score: int = Field(..., description="Fit score from 0-100")
    description: str = Field(..., description="Description of the tactical profile")
    category: str = Field(..., description="Qualitative category of fit")

class PositionAnalysis(BaseModel):
    """Analysis for a specific position"""
    profiles: Dict[str, ProfileFitDetails] = Field(..., description="All profiles for this position")
    best_fit: str = Field(..., description="Name of best profile for this position")
    best_score: int = Field(..., description="Score of best profile for this position")
    best_description: str = Field(..., description="Description of best profile for this position")
    key_metrics: list = Field(default_factory=list, description="Key metrics for this position")


class VersatilityMetrics(BaseModel):
    """Player versatility metrics"""
    position_count: int = Field(..., description="Number of positions the player can play")
    viable_roles_count: int = Field(..., description="Number of viable tactical roles (score >= 60)")

class TacticalFitAnalysis(BaseModel):
    """Complete tactical fit analysis for a player"""
    player_name: str = Field(..., description="Player's name")
    player_id: int = Field(..., description="Player's ID")
    primary_position: Optional[str] = Field(None, description="Player's primary position code")
    all_positions: List[str] = Field(..., description="All positions the player can play")
    
    # Position-specific analysis
    by_position: Dict[str, PositionAnalysis] = Field(..., description="Analysis by position")
    
    # Overall best fits
    best_fits: List[TacticalProfileFit] = Field(..., description="Top 5 tactical fits across positions")
    optimal_role: Optional[TacticalProfileFit] = Field(None, description="Best overall tactical fit")
    
    # Primary position specific
    primary_position_best_fit: Optional[str] = Field(None, description="Best fit for primary position")
    
    # Versatility
    versatility: VersatilityMetrics = Field(..., description="Player versatility metrics")
    
 ####### SWOT Analysis #########    
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal

##### SWOT Analysis Models #####
class Stat(BaseModel):
    """A statistical strength of a player"""
    stat_name: str = Field(..., description="Name of the statistic")
    percentile: float = Field(..., description="Percentile value (0-100)")
    
    class Config:
        schema_extra = {
            "example": {"stat_name": "goals", "percentile": 92.5}
        }


class SwotInput(BaseModel):
    """Input data for SWOT analysis"""
    strengths: List[Stat] = Field(..., description="Statistical strengths with percentiles")
    weaknesses: List[Stat] = Field(..., description="Statistical weaknesses with percentiles")
    
    class Config:
        schema_extra = {
            "example": {
                "strengths": [
                    {"stat_name": "goals", "percentile": 92.5},
                    {"stat_name": "shotsOnTarget", "percentile": 87.3}
                ],
                "weaknesses": [
                    {"stat_name": "defensiveDuelsWon", "percentile": 23.1},
                    {"stat_name": "interceptions", "percentile": 28.5}
                ]
            }
        }

class AIInsight(BaseModel):
    """An AI-generated insight for opportunities or threats"""
    insight: str = Field(..., description="Word or phrase describing the insight")
    based_on: List[str] = Field(default_factory=list, description="Stats this insight is based on")
    importance: int = Field(default=1, ge=1, le=3, description="Importance level (1-3)")
    
    class Config:
        schema_extra = {
            "example": {
                "insight": "Benefit from playing in a possession-based system",
                "based_on": ["goals", "shotsOnTarget"],
                "importance": 3
            }
        }

class SwotOutput(BaseModel):
    """AI-generated output for SWOT analysis"""
    opportunities: List[AIInsight] = Field(..., description="Opportunities based on strengths")
    threats: List[AIInsight] = Field(..., description="Threats based on weaknesses")
    summary: Optional[str] = Field(None, description="Brief summary of SWOT Analysis")
    
    class Config:
        schema_extra = {
            "example": {
                "opportunities": [
                    {"text": "Would excel in a team that creates many scoring chances", 
                     "based_on": ["goals", "shotsOnTarget"], 
                     "importance": 3}
                ],
                "threats": [
                    {"text": "May struggle in systems requiring forwards to press aggressively", 
                     "based_on": ["defensiveDuelsWon"], 
                     "importance": 2}
                ],
                "summary": "Player profile indicates a pure finisher who would thrive in possession-based teams"
            }
        }

class SwotAnalysis(BaseModel):
    """Complete SWOT analysis with original data and AI insights"""
    # Statistical components
    strengths: List[Stat] = Field(..., description="Statistical strengths with percentiles")
    weaknesses: List[Stat] = Field(..., description="Statistical weaknesses with percentiles")
    
    # AI-generated components
    opportunities: List[AIInsight] = Field(..., description="AI-generated opportunities")
    threats: List[AIInsight] = Field(..., description="AI-generated threats")
    
    # Summary text
    summary: Optional[str] = Field(None, description="Overall summary of the SWOT analysis")
    
    class Config:
        schema_extra = {
            "example": {
                "strengths": [
                    {"stat_name": "goals", "percentile": 92.5, "category": "offensive"}
                ],
                "weaknesses": [
                    {"stat_name": "defensiveDuelsWon", "percentile": 23.1, "category": "defensive"}
                ],
                "opportunities": [
                    {"text": "Would excel in a team that creates many scoring chances", 
                     "based_on": ["goals"], "importance": 3}
                ],
                "threats": [
                    {"text": "May struggle in systems requiring forwards to press aggressively", 
                     "based_on": ["defensiveDuelsWon"], "importance": 2}
                ],
                "summary": "A clinical finisher who would benefit from playing in an attack-minded system"
            }
        }
    
class RankingItem(BaseModel):
    """Detailed ranking information for a position"""
    rank: int = Field(..., description="Ranking position among players of same position")
    key_metrics: List[str] = Field(default_factory=list, description="Key metrics contributing to this ranking")


class DataAnalysis(BaseModel):
    swot: SwotAnalysis = Field(..., description="SWOT analysis of the player")
    ranking: List[Dict[str, RankingItem]] = Field(..., 
        description="Ranking of the player for each position he plays")
    tactical_fit: TacticalFitAnalysis = Field(..., description="Tactical fit analysis of the player")
    tactical_styles: Dict[str,Any] = Field(..., description="Tactical style fit analysis of the player")
    player: dict = Field(..., description="Player data")
    player_id: str = Field(..., description="Player ID")
    percentiles: Dict[str,dict[str, float]] = Field(..., description="Percentiles of the player")
    percentiles_by_category: Dict[str,dict[str, float]] = Field(..., description="Percentiles of the player by category")
    position_group: str

"""
class CompleteAnalysis(BaseModel):
    data_analysis: DataAnalysis
    subjective_analysis: SubjectiveAnalysis
    historical_analysis: HistoricalAnalysis
    player: Player

"""
#################
class Atribute(BaseModel):
    analysis: str = Field(..., description="Brief analysis of the player's attribute, poiting out the player's signtature style and tendencies")
    key_metrics: list[str] = Field(default_factory=list, description="Key points of the player's attributes. Ex: 'Good dribbler', 'Excellent passer'")


class TacticalFlexibility(BaseModel):
    analysis: str = Field(..., description="Analysis of the player's tactical flexibility")
    best_systems: Optional[List[str]] = Field(default_factory=list, description="List of best-suited tactical systems for the player")
    unsuitable_systems: Optional[List[str]] = Field(default_factory=list, description="List of unsuitable tactical systems for the player")
    reasoning: Optional[str] = Field(None, description="Reasoning behind the analysis of tactical flexibility")

class ContextualRecommendations(BaseModel):
    analysis: str = Field(..., description="Analysis of contextual recommendations for the player")
    key_recommendations: Optional[List[str]] = Field(default_factory=list, description="Key recommendations for maximizing the player's strengths")
    complementary_player_types: Optional[List[str]] = Field(default_factory=list, description="Complementary player types to pair with the player")

class AIAnalysis(BaseModel):
    defensive_contributions: Atribute = Field(..., description="Analysis of player's defensive work, counter-pressing, and defensive duels")
    attack_patterns: Atribute = Field(..., description="Analysis of player's offensive work, including goal contributions and playmaking")
    physical_technical_profile: Atribute = Field(..., description="Analysis of player's physical attributes.")
    tactical_flexibility: TacticalFlexibility = Field(..., description="Analysis of the player profile and its relation to tactical systems")
    contextual_recommendations: ContextualRecommendations = Field(..., description="Recommendations for team structure to maximize player's strengths")
    overall_summary: Optional[str] = Field(None, description="Overall summary of the tactical analysis")

class DesignCriteria(BaseModel):
    score: int = Field(...,ge=0,le=10,description="Score from 0-10")
    rationale: str = Field(..., description="Rationale for the score")

class Recommendation(BaseModel):
    overall_score: int = Field(...,ge=0,le=10,description="Overall score from 0-10")
    justification: str = Field(..., description="Justification for the recommendation")
    recommendation : str = Field(default=["Monitor"], description="Recommendation for the player", enum=["Monitor", "Acquisition","Loan", "Dismiss" ])


class AcquisitionStrategy(BaseModel):
    negotiation_approach: str = Field(..., description="Negotiation approach for the player")
    suggested_contract: str = Field(..., description="Suggested contract terms for the player")
    integration_plan: str = Field(..., description="Integration plan for the player into the team")
    key_considerations: list[str] = Field(..., description="Key considerations for the acquisition strategy")


class RecruitmentDecisionMatrix(BaseModel):
    acquisition_viability: DesignCriteria = Field(..., description="Acquisition viability of the player")
    tactical_fit: DesignCriteria = Field(..., description="Tactical fit of the player to the team")
    age_development_profile: DesignCriteria = Field(..., description="Age and development potential of the player")

    final_recommendation: Recommendation = Field(..., description="Final recommendation based on the matrix")
    acquisition_strategy: Optional[AcquisitionStrategy]