# KatenaScout Architecture Documentation

## Overview

KatenaScout is a football scouting AI application that helps scouts and coaches find players matching specific criteria. The application features multi-language support, conversation orchestration with intent recognition, and detailed player profiles.

This document describes the architecture of the backend system after the unification refactoring.

## System Architecture

The backend follows a modular architecture with clear separation of concerns:

```
backend/
├── app.py               # Main Flask app with route definitions
├── config.py            # Configuration constants
├── core/                # Core business logic
│   ├── session.py       # Unified session management
│   ├── intent.py        # Intent recognition and entity extraction
│   ├── player_search.py # Player search functionality
│   ├── comparison.py    # Player comparison functionality
│   └── handlers.py      # Intent-specific handlers
├── models/              # Data models
│   ├── parameters.py    # Search parameter models
│   ├── player.py        # Player data models
│   └── response.py      # API response models
├── services/            # Service wrappers
│   ├── claude_api.py    # Claude API integration
│   ├── data_service.py  # Data access and loading
│   └── nlp_service.py   # Natural language processing
├── utils/               # Utilities
│   ├── formatters.py    # Response formatting
│   └── validators.py    # Input validation
└── requirements.txt     # Dependencies
```

## Key Components

### Session Management (core/session.py)

The `UnifiedSession` class manages user sessions, combining the functionality from the old `ChatSession` and `ConversationMemory` classes. It provides:

- Session creation, retrieval, and updating
- Claude API integration
- Parameter extraction from natural language
- Player search and information retrieval

### Intent Recognition (core/intent.py)

The intent recognition system identifies the user's intent from their message:

- **player_search**: User wants to find players with specific characteristics
- **player_comparison**: User wants to compare two or more players
- **explain_stats**: User wants an explanation of football statistics or metrics
- **casual_conversation**: User is engaging in small talk or asking about the system itself

### Parameter Models (models/parameters.py)

Defines structured models for search parameters, ensuring a single source of truth for parameter definitions:

- `SearchParameters`: Comprehensive model for all search criteria
- `PositionCorrection`: Model for correcting invalid position codes
- `SearchRequest` and `ComparisonRequest`: Models for API request validation

### Player Search (core/player_search.py)

Contains the core functionality for searching players based on parameters:

- `search_players()`: Main search function that scores and ranks players
- `get_player_info()`: Function to retrieve detailed player information
- `get_score()`: Function to calculate player scores based on parameters

### Handlers (core/handlers.py)

Intent-specific handlers process user requests based on the identified intent:

- `handle_player_search()`: Handles player search requests
- `handle_player_comparison()`: Handles player comparison requests
- `handle_stats_explanation()`: Handles requests to explain statistics
- `handle_casual_chat()`: Handles casual conversation
- `handle_fallback()`: Handles unrecognized intents

### API Routes (app.py)

The main Flask application defines the following routes:

- `/enhanced_search`: Main endpoint for chat interactions
- `/player_comparison`: Compare multiple players
- `/explain_stats`: Get explanations for football statistics
- `/follow_up_suggestions/<session_id>`: Get follow-up suggestions
- `/player-image/<player_id>`: Get player images
- `/languages`: Get available languages
- `/chat_history/<session_id>`: Get chat history for a session

## Data Flow

### Player Search Flow

1. User sends a query to `/enhanced_search`
2. The request is validated using `validate_search_request()`
3. Intent is identified using `identify_intent()`
4. If the intent is `player_search`, parameters are extracted using `get_parameters()`
5. Players are searched using `search_players()`
6. Results are formatted and returned to the user

### Player Comparison Flow

1. User sends a request to `/player_comparison` or asks for comparison in chat
2. If via chat, the orchestrator identifies the `player_comparison` intent
3. Players to compare are determined from request data or session memory
4. Player details are retrieved using `get_player_info()`
5. Comparison is generated using `compare_players()`
6. Results are formatted and returned to the user

## Design Principles

The architecture follows these key principles:

1. **Single Responsibility Principle**: Each module has a single responsibility
2. **Dependency Injection**: Components receive their dependencies rather than creating them
3. **Separation of Concerns**: Clear boundaries between different parts of the system
4. **Single Source of Truth**: Each piece of functionality is defined in one place
5. **Error Handling**: Robust error handling at each level with appropriate fallbacks

## Future Considerations

The architecture is designed to support future enhancements:

- **Scalability**: The modular design allows for horizontal scaling
- **Extensibility**: New intents and handlers can be added without modifying existing code
- **Maintainability**: Clear separation of concerns makes the codebase easier to maintain
- **Testing**: Each component can be tested in isolation

---

Document prepared by: Senior Programmer, KatenaScout Team
Date: March 15, 2025