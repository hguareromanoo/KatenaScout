"""
Configuration settings and constants for KatenaScout

This module centralizes all constant values used throughout the application.
"""

# Mapping positions to their codes
POSITIONS_MAPPING = {
    "goalkeeper": ["gk"],
    "center back": ["cb", "rcb", "lcb"],
    "right back": ["rb", "rwb"],
    "left back": ["lb", "lwb"],
    "defensive midfielder": ["dmf", "rdmf", "ldmf"],
    "central midfielder": ["cmf", "rcmf", "lcmf"],
    "attacking midfielder": ["amf", "ramf", "lamf"],
    "right winger": ["rw", "rwf"],
    "left winger": ["lw", "lwf"],
    "center forward": ["cf"],
    "striker": ["cf"],
    "forward": ["cf", "lw", "rw", "lwf", "rwf"]
}

# List of valid position codes
VALID_POSITION_CODES = [
    "gk", 
    "cb", "rcb", "lcb", 
    "rb", "rwb", "lb", "lwb", 
    "dmf", "rdmf", "ldmf", 
    "cmf", "rcmf", "lcmf", 
    "amf", "ramf", "lamf", 
    "rw", "rwf", "lw", "lwf", 
    "cf"
]

# Player search configurations
DEFAULT_SEARCH_LIMIT = 5  # Number of players to return in search results
MIN_SCORE_THRESHOLD = 0.4  # Minimum score for a player to be considered relevant

# Claude API configuration
DEFAULT_MODEL = "claude-3-5-sonnet-20240624"  # Updated to correct model identifier
DEFAULT_MAX_TOKENS = 4096

# Languages supported by the system
SUPPORTED_LANGUAGES = ["english", "portuguese", "spanish", "bulgarian"]

# Default data file paths
DATA_FILES = {
    "average_stats": "average_statistics_by_position.json",
    "weights": "weights_dict.json",
    "database": "database.json",
    "database_id": "db_by_id.json",
    "teams": "team.json"
}

# Player image directory (absolute path for reliability)
import os
PLAYER_IMAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "player_images"))