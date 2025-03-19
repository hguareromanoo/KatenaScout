# KatenaScout Backend

A unified backend for the KatenaScout football scouting AI application.

## Overview

KatenaScout is a football scouting AI application that helps scouts and coaches find players matching specific criteria. The application features multi-language support (English, Portuguese, Spanish, Bulgarian), conversation orchestration with intent recognition, a favorites system, and detailed player profiles.

## Architecture

The backend follows a modular architecture with clear separation of concerns:

- **core/** - Core business logic
  - **session.py** - Unified session management
  - **intent.py** - Intent recognition and entity extraction
  - **player_search.py** - Player search functionality
  - **comparison.py** - Player comparison functionality
  - **handlers.py** - Intent-specific handlers

- **models/** - Data models
  - **parameters.py** - Parameter models for search
  - **player.py** - Player data models
  - **response.py** - Response models for API endpoints

- **services/** - Service wrappers
  - **claude_api.py** - Claude API integration
  - **data_service.py** - Data access and loading
  - **nlp_service.py** - Natural language processing utilities

- **utils/** - Utilities
  - **formatters.py** - Response formatting
  - **validators.py** - Input validation

- **app.py** - Main Flask application and routes
- **config.py** - Configuration constants

## API Endpoints

- `/enhanced_search` - Main endpoint for AI chat interactions with orchestration
- `/player_comparison` - Compare multiple players across key metrics
- `/explain_stats` - Get explanations for football statistics
- `/follow_up_suggestions/<session_id>` - Get context-aware follow-up suggestions
- `/player-image/<player_id>` - Get player images
- `/languages` - Get available languages
- `/chat_history/<session_id>` - Get chat history for a session

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/KatenaScout.git
cd KatenaScout

# Install backend dependencies
pip install -r backend/requirements.txt

# Run the backend
cd backend
chmod +x run.sh
./run.sh
```

## Development

The codebase follows these principles:

1. **Single source of truth** - Each piece of functionality is defined in one place
2. **Separation of concerns** - Clear boundaries between different parts of the system
3. **Dependency injection** - Components receive their dependencies instead of creating them
4. **Error handling** - Robust error handling and fallbacks

## Environment Variables

- `ANTHROPIC_API_KEY` - API key for Claude AI (or use `env_keys.py`)
- `FLASK_ENV` - Environment (development or production)
- `PORT` - Port for the Flask server (default: 5000)