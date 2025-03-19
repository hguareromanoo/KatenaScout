# KatenaScout Project Notes

## Project Overview
KatenaScout is a football scouting AI application that helps scouts and coaches find players matching specific criteria. The application features multi-language support (English, Portuguese, Spanish, Bulgarian), conversation orchestration with intent recognition, a favorites system, and detailed player profiles.

## Commands

### Backend
```bash
# Run the enhanced flask backend
cd backend
chmod +x run_enhanced.sh
./run_enhanced.sh

# Install backend dependencies
pip install -r backend/requirements.txt
```

### Frontend
```bash
# Run the frontend development server
cd frontend/enhanced-client
npm start

# Install frontend dependencies
cd frontend/enhanced-client
npm install
```

## App Structure

### Main Components
- **App.js**: Main application component
- **OnboardingView**: Initial language selection screen
- **ChatInterface**: AI chat for player discovery
- **PlayerDashboard**: Quick view of player stats in a modal
- **PlayerCompletePage**: Full detailed player profile
- **FavoritesView**: View and manage favorite players
- **SettingsView**: Change language and app settings

### Key Features
- Multi-language support (English, Portuguese, Spanish, Bulgarian)
- Chat-based AI player search with natural language understanding
- Conversation orchestration with intent recognition
- Follow-up suggestions and context awareness
- Player comparison across key metrics
- Football statistics explanations
- Favorites system
- Detailed player statistics
- Player image display

## Code Style Preferences
- Use functional components with React hooks
- Components should have translations for all supported languages
- Use Tailwind CSS for styling
- Keep components modular and reusable

## API Endpoints
- `/enhanced_search`: Main endpoint for AI chat interactions with orchestration
- `/player_comparison`: Compare multiple players across key metrics
- `/explain_stats`: Get explanations for football statistics
- `/follow_up_suggestions/<session_id>`: Get context-aware follow-up suggestions
- `/player-image/<player_id>`: Get player images
- `/languages`: Get available languages
- `/chat_history/<session_id>`: Get chat history for a session

## State Management
- Use React hooks (useState, useEffect) for state management
- Store user preferences in localStorage
- Keep session state in backend for chat context

## Project Roadmap
- User accounts and cloud storage for favorites
- More advanced filtering and search capabilities
- Performance optimizations for larger datasets
- Additional language support
- Team composition recommendations