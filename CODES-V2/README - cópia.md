# KatenaScout - Intelligent Soccer Scouting Platform

KatenaScout is an AI-powered soccer scouting platform that helps clubs, scouts, and players discover and analyze soccer talent. The application features an intelligent chat interface that leverages Anthropic's Claude AI to understand natural language queries about player characteristics and translate them into structured search parameters.

## Features

- **AI-Powered Search**: Find players based on natural language descriptions of required attributes 
- **Multilingual Support**: Full support for English, Portuguese, Spanish, and Bulgarian
- **Enhanced Chat Interface**: Contextual conversation with memory of previous queries
- **Player Analysis**: Comprehensive statistical breakdowns and performance metrics
- **Authentication System**: Separate account types for clubs/scouts and players
- **Favorites System**: Save and organize players of interest
- **Responsive Design**: Works seamlessly across desktop and mobile devices

## Tech Stack

### Backend
- Python Flask API
- Anthropic Claude and OpenAI integration
- Supabase for authentication and database
- JWT token-based authentication
- RESTful API architecture

### Frontend
- React.js
- Tailwind CSS
- Recharts for data visualization
- Lucide React for icons

## Project Structure

The project consists of two main components:

1. **Backend**: A Flask API that handles:
   - User authentication
   - AI-powered player search
   - Session management
   - Player data access

2. **Frontend**: A React application that provides:
   - Chat interface for player discovery
   - Player profiles and visualizations
   - User management
   - Favorites system

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Anthropic API key
- OpenAI API key (optional)
- Supabase account (optional for authentication)

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/katenascout.git
   cd katenascout
   ```

2. Install backend dependencies
   ```
   pip install -r requirements.txt
   ```

3. Install frontend dependencies
   ```
   cd frontend
   npm install
   ```

4. Set up environment variables
   - Create a `.env` file in the project root with the following variables:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   OPENAI_API_KEY=your_openai_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   JWT_SECRET=your_jwt_secret_key
   ```

### Running the Application

1. Start the backend server
   ```
   python enhanced_chat.py
   ```

2. Start the frontend development server
   ```
   cd frontend
   npm start
   ```

3. Access the application at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /auth/signup`: Register a new user
- `POST /auth/login`: Log in an existing user
- `POST /auth/verify-email`: Verify email with confirmation code

### Player Search
- `POST /enhanced_search`: Primary endpoint for AI-powered player search

### Utilities
- `GET /health`: Health check endpoint
- `GET /languages`: Get available languages
- `GET /player-image/<player_id>`: Get player image
- `GET /chat_history/<session_id>`: Get chat history for a session

## AI Integration

KatenaScout leverages Anthropic's Claude AI to:

1. Interpret natural language queries about player requirements
2. Convert these into structured search parameters
3. Weigh and score players based on how well they match the criteria
4. Generate natural language responses about the found players

The system maintains conversation context to refine searches over multiple interactions.

## Dataset Structure

The application works with soccer player data that includes:
- Basic attributes (name, age, height, weight, etc.)
- Position information
- Statistical metrics (goals, assists, passes, etc.)
- Performance indicators by category (offe