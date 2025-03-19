# KatenaScout - AI Football Scouting Assistant

KatenaScout is an AI-powered football scouting application that helps scouts and coaches find players matching specific criteria. This application features multi-language support (English, Portuguese, Spanish, Bulgarian), a favorites system, and detailed player profiles.

## Features

- **Multi-language support**: English, Portuguese, Spanish, Bulgarian
- **Chat-based AI player search**: Natural language interface to find players
- **Conversation Orchestration**: Intent recognition and context-aware responses
- **Player Dashboard**: Quick view of player stats with radar chart visualization
- **Complete Player Profiles**: Detailed view of all player metrics and attributes
- **Player Comparisons**: Compare multiple players across key metrics
- **Stats Explanations**: Detailed explanations of football statistics
- **Follow-up Suggestions**: Smart suggestions for continuing the conversation
- **Favorites System**: Save and organize players of interest
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

- `/backend`: Flask backend with AI player search capabilities
  - `enhanced_chat.py`: Main backend service with player search logic
  - `orchestrator/`: Conversation orchestration module
    - `models.py`: Data models for conversation memory and intents
    - `orchestrator.py`: Main orchestration logic
    - `intents.py`: Intent recognition and entity extraction
    - `handlers.py`: Intent-specific handler functions
    - `response.py`: Response generation utilities
  - `player-image.py`: Service for serving player images
  - `team.json`: Team data with names and images
  
- `/frontend`: React frontend applications
  - `/client`: Original client application
  - `/enhanced-client`: Enhanced version with improved UI/UX

## Setup and Installation

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with required API keys:
   ```
   CLAUDE_API_KEY=your_api_key_here
   ```

4. Run the backend server:
   ```
   chmod +x run_enhanced.sh
   ./run_enhanced.sh
   ```

### Frontend Setup

1. Navigate to the enhanced client directory:
   ```
   cd frontend/enhanced-client
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. Open your browser to http://localhost:3001

## Usage

1. Select your preferred language on the onboarding screen
2. Use the chat interface to describe the type of player you're looking for
3. View player cards in the results and click to see detailed information
4. Follow suggested follow-up queries or ask your own follow-up questions
5. Request player comparisons between two or more selected players
6. Ask for explanations of football statistics you're not familiar with
7. Save interesting players to your favorites for later reference
8. View all player metrics in the complete profile view

## API Endpoints

- `/enhanced_search`: Main endpoint for AI chat interactions with orchestration
- `/player_comparison`: Compare multiple players across key metrics
- `/explain_stats`: Get explanations for football statistics and metrics
- `/follow_up_suggestions/<session_id>`: Get context-aware follow-up suggestions
- `/player-image/<player_id>`: Get player images
- `/languages`: Get available languages
- `/chat_history/<session_id>`: Get chat history for a session

## Technologies Used

- **Backend**: Python, Flask, Claude AI API
- **Frontend**: React, Tailwind CSS, Recharts 
- **Data Visualization**: Radar charts, performance metrics
- **Styling**: Custom CSS with responsive design

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Powered by Claude AI for natural language processing
- Data sourced from various football statistics providers