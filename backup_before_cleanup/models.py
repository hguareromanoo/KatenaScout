"""
Data models for the KatenaScout conversation orchestrator
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class Intent(BaseModel):
    """Model representing a user intent with confidence score"""
    name: str = Field(..., description="Intent name")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")


class ConversationMemory(BaseModel):
    """Model for tracking conversation state and context"""
    session_id: str
    messages: List[Dict] = Field(default_factory=list)
    entities: Dict[str, Any] = Field(default_factory=dict)  # Players, teams mentioned
    current_intent: Optional[str] = None
    recent_function_calls: List[str] = Field(default_factory=list)
    language: str = "english"
    search_history: List[str] = Field(default_factory=list)
    selected_players: List[Dict] = Field(default_factory=list)
    search_params: Dict[str, Any] = Field(default_factory=dict)
    satisfaction: Optional[bool] = None
    current_prompt: str = ""
    is_follow_up: bool = False