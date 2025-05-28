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
- `database.py` - SQLAlchemy engine setup and session management
- `models/sql_models.py` - SQLAlchemy ORM models
- `utils/converters.py` - Pydantic to SQLAlchemy model converters (and vice-versa if needed)

## Database Setup

This project now uses PostgreSQL as its database.

1.  **Ensure PostgreSQL is Installed and Running**:
    Install PostgreSQL (version 12+ recommended) if you haven't already. Make sure the service is running.

2.  **Create a Database and User**:
    You'll need to create a database and a user with privileges to connect to and modify this database. For example, using `psql`:
    ```sql
    CREATE DATABASE soccer_scout_db;
    CREATE USER your_db_user WITH PASSWORD 'your_db_password';
    GRANT ALL PRIVILEGES ON DATABASE soccer_scout_db TO your_db_user;
    ALTER ROLE your_db_user CREATEDB; -- Optional, if user needs to create DBs for tests etc.
    ```

3.  **Set Environment Variables**:
    The application uses environment variables to connect to the database. These are defined in `backend/config.py` and include:
    - `POSTGRES_HOST` (default: `localhost`)
    - `POSTGRES_PORT` (default: `5432`)
    - `POSTGRES_USER` (default: `your_db_user`)
    - `POSTGRES_PASSWORD` (default: `your_db_password`)
    - `POSTGRES_DB` (default: `soccer_scout_db`)

    You can set these in your environment directly or create a `.env` file in the `backend` directory with the following format:
    ```env
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_USER=your_actual_user
    POSTGRES_PASSWORD=your_actual_password
    POSTGRES_DB=soccer_scout_db
    # Ensure ANTHROPIC_API_KEY is also set here if using .env
    ANTHROPIC_API_KEY=your_claude_api_key 
    ```
    The application uses `python-dotenv` to load these variables.

4.  **Initialize Database Schema**:
    The SQLAlchemy models define the database schema. To create all tables, you can run the `init_db()` function. A simple way to do this is to add a temporary script or uncomment the example execution block in `backend/database.py` and run it once:
    ```python
    # In backend/database.py, at the end of the file:
    # if __name__ == "__main__":
    #     print("Initializing database...")
    #     init_db()
    #     print("Database initialization complete.")
    ```
    Then run `python backend/database.py` from the project root. Remember to comment out or remove this execution block after the first run.

5.  **Load Mock Data (Optional but Recommended for Development)**:
    A SQL script with DDL and mock DML is provided at `tasks/mock_data.sql`. You can populate your database using:
    ```bash
    psql -U your_actual_user -d soccer_scout_db -a -f ../tasks/mock_data.sql 
    ```
    (Adjust path to `mock_data.sql` based on where you run the command. This example assumes you are in the `backend` directory).
    The script includes `DROP TABLE IF EXISTS` commands, so it can be run multiple times.

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
git clone https://github.com/yourusername/KatenaScout.git # Replace with actual repo URL if different
cd KatenaScout

# Install backend dependencies
# Ensure you have PostgreSQL client libraries installed if psycopg2-binary has issues
# (e.g., sudo apt-get install libpq-dev on Debian/Ubuntu)
pip install -r backend/requirements.txt
# Key new dependencies include SQLAlchemy and psycopg2-binary for PostgreSQL.

# Run the backend
cd backend
chmod +x run.sh # Ensure run.sh is executable
./run.sh
# Make sure your PostgreSQL server is running and environment variables are set before running.
```

## Development

The codebase follows these principles:

1. **Single source of truth** - Each piece of functionality is defined in one place
2. **Separation of concerns** - Clear boundaries between different parts of the system
3. **Dependency injection** - Components receive their dependencies instead of creating them
4. **Error handling** - Robust error handling and fallbacks

## Environment Variables

- `ANTHROPIC_API_KEY` - API key for Claude AI (can be set in `.env` or system environment).
- `FLASK_ENV` - Environment (e.g., `development` or `production`).
- `PORT` - Port for the Flask server (default: `5000`).
- `POSTGRES_HOST` - Hostname of the PostgreSQL server (default: `localhost`).
- `POSTGRES_PORT` - Port of the PostgreSQL server (default: `5432`).
- `POSTGRES_USER` - PostgreSQL username.
- `POSTGRES_PASSWORD` - PostgreSQL password.
- `POSTGRES_DB` - Name of the PostgreSQL database.