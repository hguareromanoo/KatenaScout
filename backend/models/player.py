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
    # Use Any type for wyId to accept both string and int types
    wyId: Any = Field(None, description="Wyscout ID - can be string or int")
    name: str = Field(..., description="Player name")
    age: Optional[int] = Field(None, description="Player age")
    height: Optional[int] = Field(None, description="Player height in cm")
    weight: Optional[int] = Field(None, description="Player weight in kg")
    positions: List[str] = Field(default_factory=list, description="Position codes (e.g., ['cb', 'rb'])")
    club: Optional[str] = Field(None, description="Current club name")
    nationality: Optional[str] = Field(None, description="Player nationality")
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
    wyId: Optional[str] = Field(None, description="Wyscout ID")
    name: str = Field(..., description="Player name")
    age: Optional[int] = Field(None, description="Player age")
    height: Optional[int] = Field(None, description="Player height in cm")
    weight: Optional[int] = Field(None, description="Player weight in kg")
    positions: List[Dict[str, Any]] = Field(default_factory=list, description="Detailed positions data")
    club: Optional[Dict[str, Any]] = Field(None, description="Current club data")
    contractUntil: Optional[str] = Field(None, description="Contract expiration date")
    nationality: Optional[Dict[str, Any]] = Field(None, description="Nationality data")
    foot: Optional[str] = Field(None, description="Preferred foot")
    stats: Dict[str, Optional[float]] = Field(default_factory=dict, description="Player statistics")
    
    # Convert complex Player object to simplified PlayerSummary
    def to_summary(self, score: Optional[float] = None) -> PlayerSummary:
        """Convert to PlayerSummary with simplified fields"""
        # Extract position codes
        position_codes = [
            pos["position"]["code"] for pos in self.positions 
            if isinstance(pos, dict) and "position" in pos
        ]
        
        # Extract club name
        club_name = None
        if isinstance(self.club, dict) and "name" in self.club:
            club_name = self.club["name"]
        
        # Extract nationality
        nationality_str = None
        if isinstance(self.nationality, dict):
            if "name" in self.nationality:
                nationality_str = self.nationality["name"]
            elif "alpha3code" in self.nationality:
                nationality_str = self.nationality["alpha3code"]
        elif isinstance(self.nationality, str):
            nationality_str = self.nationality
        
        return PlayerSummary(
            wyId=self.wyId,
            name=self.name,
            age=self.age,
            height=self.height,
            weight=self.weight,
            positions=position_codes,
            club=club_name,
            nationality=nationality_str,
            foot=self.foot,
            stats=self.stats,
            score=score
        )