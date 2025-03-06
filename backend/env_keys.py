import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_anthropic_api_key():
    """Get Anthropic API key from environment variables."""
    return os.getenv("ANTHROPIC_API_KEY")

def get_openai_api_key():
    """Get OpenAI API key from environment variables."""
    return os.getenv("OPENAI_API_KEY")

def get_wyscout_credentials():
    """Get Wyscout API credentials from environment variables."""
    username = os.getenv("WYSCOUT_API_USERNAME")
    password = os.getenv("WYSCOUT_API_PASSWORD")
    return username, password