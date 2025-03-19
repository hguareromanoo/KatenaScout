import os
import sys
from dotenv import load_dotenv

# Try to load environment variables from different possible .env locations
env_paths = ['.env', os.path.join(os.path.dirname(__file__), '.env')]
for env_path in env_paths:
    if os.path.exists(env_path):
        print(f"Loading environment from {env_path}", file=sys.stderr)
        load_dotenv(env_path)
        break
else:
    print("No .env file found, using system environment variables", file=sys.stderr)

def get_anthropic_api_key():
    """Get Anthropic API key from environment variables."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("WARNING: ANTHROPIC_API_KEY not found in environment variables", file=sys.stderr)
    return api_key

def get_openai_api_key():
    """Get OpenAI API key from environment variables."""
    return os.getenv("OPENAI_API_KEY")

def get_wyscout_credentials():
    """Get Wyscout API credentials from environment variables."""
    username = os.getenv("WYSCOUT_API_USERNAME")
    password = os.getenv("WYSCOUT_API_PASSWORD")
    return username, password