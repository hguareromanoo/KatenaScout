# KatenaScout Project Overview

KatenaScout is a football scouting AI application that helps scouts and coaches find players matching specific criteria.

## Project Structure

```
/KatenaScout/
├── backend/                # Python Flask backend
│   ├── core/               # Core business logic
│   ├── models/             # Data models (Pydantic)
│   ├── services/           # Service wrappers
│   ├── utils/              # Utility functions
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration constants
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # React frontend 
│   ├── client/             # Original React client
│   └── enhanced-client/    # Refactored React client
│       ├── src/
│       │   ├── api/        # API service layer
│       │   ├── components/ # React components
│       │   ├── contexts/   # React context providers
│       │   ├── config/     # Configuration constants
│       │   ├── locales/    # Translation files
│       │   ├── utils/      # Utility functions
│       │   └── App.js      # Main component
│       └── STRUCTURE.md    # Detailed frontend structure
│
├── CLAUDE.md               # Project notes for Claude
└── PROJECT_OVERVIEW.md     # This file
```

## Key Features

- Multi-language support (English, Portuguese, Spanish, Bulgarian)
- Conversation orchestration with intent recognition
- Chat-based AI player search with natural language
- Player comparison across key metrics
- Favorites system for saving players
- Detailed player statistics and visualizations

## Technology Stack

### Backend
- Python/Flask: Web framework
- Claude API: Natural language generation
- Pydantic: Data validation and models

### Frontend
- React: UI library
- Context API: State management
- Tailwind CSS: Styling
- Recharts: Data visualization

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
chmod +x run_enhanced.sh
./run_enhanced.sh
```

### Frontend
```bash
cd frontend/enhanced-client
npm install
npm start
```

## Documentation

- [Backend Architecture](backend/ARCHITECTURE.md)
- [Frontend Structure](frontend/enhanced-client/STRUCTURE.md)
- [Project Roadmap](backend/ROADMAP.md)
- [Player Comparison](backend/PLAYER_COMPARISON.md)

## Development Guidelines

1. **Frontend**: Component-based architecture with React Context for state
2. **Backend**: Modular architecture with clear separation of concerns
3. **API**: RESTful endpoints with consistent response formats
4. **Translations**: All UI text should be in all supported languages
5. **Code Style**: Follow existing patterns and conventions

## Main Components

### Frontend
- **App.js**: Main application component
- **ChatInterface**: AI chat for player discovery
- **PlayerDashboard**: Quick view of player stats in a modal
- **PlayerCompletePage**: Full detailed player profile
- **FavoritesView**: View and manage favorite players

### Backend
- **app.py**: Main Flask application with routes
- **core/player_search.py**: Search logic for players
- **core/comparison.py**: Player comparison functionality
- **core/intent.py**: Intent recognition for queries
- **services/claude_api.py**: Integration with Claude API

## API Endpoints

- `/enhanced_search`: Main endpoint for AI chat interactions
- `/player_comparison`: Compare multiple players
- `/explain_stats`: Get explanations for statistics
- `/follow_up_suggestions/<session_id>`: Get context-aware suggestions
- `/player-image/<player_id>`: Fetch player images
- `/languages`: Get available languages