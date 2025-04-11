# KatenaScout - AI Football Scouting Assistant

KatenaScout is an AI-powered football scouting application that helps scouts and coaches find players matching specific criteria. This application features multi-language support (English, Portuguese, Spanish, Bulgarian), a favorites system, and detailed player profiles.

## Features

- **Multi-language support**: English, Portuguese, Spanish, Bulgarian
- **Chat-based AI player search**: Natural language interface to find players
- **Context-Aware Conversation**: Intent recognition and context-aware parameter extraction using conversation history.
- **Player Dashboard**: Quick view of player stats with radar chart visualization
- **Complete Player Profiles**: Detailed view of all player metrics and attributes
- **Player Comparisons**: Compare multiple players across key metrics (including tactical fit analysis).
- **Stats Explanations**: Detailed explanations of football statistics
- **Follow-up Suggestions**: Smart suggestions for continuing the conversation
- **Favorites System**: Save and organize players of interest
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

- `/backend`: Flask backend with AI player search capabilities
  - `app.py`: Main Flask application file, defines routes and handles request flow.
  - `config.py`: Configuration settings (e.g., position mappings, API keys).
  - `/core`: Core business logic modules.
    - `session.py`: Manages user sessions and conversation state (`UnifiedSession`). Includes context-aware parameter extraction (`get_parameters`).
    - `intent.py`: Handles intent recognition and entity extraction.
    - `handlers.py`: Contains functions for specific user intents (search, comparison, explanation, etc.).
    - `player_search.py`: Implements the core player search and scoring logic.
    - `comparison.py`: Logic for comparing players based on stats.
    - `enhanced_comparison.py`: Provides enhanced comparison metrics and winners.
    - `tactical_analysis.py`: Analyzes player fit for specific tactical styles.
  - `/models`: Pydantic models for data structures.
    - `parameters.py`: Defines the `SearchParameters` model used for player searches.
    - `player.py`: (Likely) Defines player data models.
    - `response.py`: (Likely) Defines API response models.
  - `/utils`: Utility functions.
    - `validators.py`: Functions for validating incoming API request data.
    - `formatters.py`: Functions for formatting API responses.
  - `/services`: Modules for interacting with external services or data sources.
    - `claude_api.py`: Handles communication with the Claude AI API.
    - `data_service.py`: (Likely) Handles loading and accessing player data.
  - `requirements.txt`: Python dependencies.
  - `.env` / `.env.example`: Environment variables (API keys).
  - `*.json`: Data files (player database, weights, averages).
  - `/player_images`: Directory for storing player images.

- `/frontend`: React frontend applications
  - `/client`: Original client application (potentially deprecated).
  - `/enhanced-client`: Current enhanced version with improved UI/UX.

## Setup and Installation

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file based on `.env.example` with required API keys:
    ```
    CLAUDE_API_KEY=your_api_key_here
    ```
4.  Run the backend server:
    ```bash
    python app.py 
    ```
    *(Note: Verify if `run.sh` or `run_enhanced.sh` are still relevant or if `python app.py` is the standard way)*

### Frontend Setup

1.  Navigate to the enhanced client directory:
    ```bash
    cd frontend/enhanced-client
    ```
2.  Install Node.js dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm start
    ```
4.  Open your browser to `http://localhost:3001` (or the port specified by `npm start`).

## Usage

1.  Select your preferred language on the onboarding screen.
2.  Use the chat interface to describe the type of player you're looking for (e.g., "Find fast wingers", then "show me ones under 20").
3.  View player cards in the results and click to see detailed information.
4.  Follow suggested follow-up queries or ask your own follow-up questions.
5.  Request player comparisons between two or more selected players.
6.  Ask for explanations of football statistics you're not familiar with.
7.  Save interesting players to your favorites for later reference.
8.  View all player metrics in the complete profile view.

## API Endpoints

- `/health`: Health check endpoint.
- `/enhanced_search`: Main endpoint for AI chat interactions.
- `/player_comparison`: Compare multiple players based on stats.
- `/tactical_analysis`: Compare players based on tactical fit.
- `/explain_stats`: Get explanations for football statistics and metrics.
- `/follow_up_suggestions/<session_id>`: Get context-aware follow-up suggestions.
- `/player-image/<player_id>`: Get player images.
- `/languages`: Get available languages.
- `/chat_history/<session_id>`: Get chat history for a session.

## Technologies Used

- **Backend**: Python, Flask, Pydantic, Claude AI API
- **Frontend**: React, Tailwind CSS, Recharts
- **Data Visualization**: Radar charts, performance metrics
- **Styling**: Custom CSS with responsive design

## Contributing

1.  Fork the repository.
2.  Create a feature branch: `git checkout -b feature-name`
3.  Commit your changes: `git commit -am 'Add feature'`
4.  Push to the branch: `git push origin feature-name`
5.  Submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Powered by Claude AI for natural language processing.
- Data sourced from various football statistics providers.
