"""
Player data models for KatenaScout
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class PlayerPosition(BaseModel):
    """Position a player can play in"""
    code: str = Field(..., description="Position code (e.g., 'cb', 'amf')")
    name: Optional[str] = Field(None, description="Position name (e.g., 'Center Back')")

class PlayerStats(BaseModel):
    """Statistics for a player"""
    # These are dynamic based on the stats available
    # The model allows any field name with numeric values
    model_config = {
        "extra": "allow"
    }
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def get(self, key, default=None):
        return getattr(self, key, default)
    
    def keys(self):
        return self.model_dump().keys()
    
    def items(self):
        return self.model_dump().items()
    
    def update(self, other_dict):
        for key, value in other_dict.items():
            setattr(self, key, value)

class PlayerSummary(BaseModel):
    """Summary data for a player (used in search results)"""
    wyId: Optional[str] = Field(None, description="Player ID (typically from database, stringified)") # Changed to Optional[str]
    name: str = Field(..., description="Player name")
    age: Optional[int] = Field(None, description="Player age")
    height: Optional[int] = Field(None, description="Player height in cm")
    weight: Optional[int] = Field(None, description="Player weight in kg") # Not in SQL Player model
    positions: List[str] = Field(default_factory=list, description="List of granular position codes (e.g., ['cb', 'rb'])")
    club: Optional[str] = Field(None, description="Current club name (simplified)")
    nationality: Optional[str] = Field(None, description="Player nationality name (simplified)")
    foot: Optional[str] = Field(None, description="Preferred foot")
    stats: Dict[str, Optional[float]] = Field(default_factory=dict, description="Key player statistics")
    score: Optional[float] = Field(None, description="Search match score (0-1)")
    
    # Additional fields for improved frontend integration
    image_url: Optional[str] = Field(None, description="URL to player image")
    detailed_stats: Optional[Dict[str, Any]] = Field(None, description="Complete stats for detailed view")
    
    model_config = {
        "extra": "allow",  # Allow extra fields for flexibility
    }

class Player(BaseModel):
    """Detailed player data"""
    wyId: Optional[str] = Field(None, description="Player ID (typically from database, stringified)")
    name: str = Field(..., description="Player name")
    age: Optional[int] = Field(None, description="Player age")
    height: Optional[int] = Field(None, description="Player height in cm")
    weight: Optional[int] = Field(None, description="Player weight in kg") # Not in SQL Player model
    positions: List[PlayerPosition] = Field(default_factory=list, description="Detailed positions data using PlayerPosition model")
    club: Optional[str] = Field(None, description="Current club name (simplified)") # Simplified
    contractUntil: Optional[str] = Field(None, description="Contract expiration date (YYYY-MM-DD)")
    nationality: Optional[str] = Field(None, description="Player nationality name (simplified)") # Simplified
    foot: Optional[str] = Field(None, description="Preferred foot")
    stats: Dict[str, Optional[float]] = Field(default_factory=dict, description="Player statistics")
    
    # Convert complex Player object to simplified PlayerSummary
    def to_summary(self, score: Optional[float] = None) -> PlayerSummary:
        """Convert to PlayerSummary with simplified fields"""
        # Extract position codes from List[PlayerPosition]
        position_codes = [pos.code for pos in self.positions]
        
        # Club is now Optional[str]
        club_name_summary = self.club 
        
        # Nationality is now Optional[str]
        nationality_summary_str = self.nationality
        
        return PlayerSummary(
            wyId=self.wyId, # Should be Optional[str]
            name=self.name,
            age=self.age,
            height=self.height,
            weight=self.weight, # Not in SQL Player model
            positions=position_codes,
            club=club_name_summary,
            nationality=nationality_summary_str,
            foot=self.foot,
            stats=self.stats,
            score=score
        )