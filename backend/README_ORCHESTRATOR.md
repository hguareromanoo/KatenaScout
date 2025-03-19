# KatenaScout Conversation Orchestrator

The conversation orchestrator is a new module added to KatenaScout that enhances the natural language capabilities of the application. It provides intent recognition, context-aware responses, and specialized handlers for different types of user queries.

## Architecture

The orchestrator follows a modular design pattern with the following components:

### Models (`models.py`)

- `ConversationMemory`: Tracks conversation state, including message history, entities, and user intentions
- `Intent`: Represents a user intent with confidence score

### Orchestrator (`orchestrator.py`)

- `process_user_message()`: Entry point for processing user messages
- `conversation_orchestrator()`: Central orchestration function that decides what to do with a message
- `format_response()`: Formats responses based on intent type

### Intents (`intents.py`)

- `identify_intent()`: Recognizes user intent from message
- `extract_entities()`: Extracts entities (players, stats) from message
- `generate_follow_up_suggestions()`: Creates context-aware follow-up suggestions

### Handlers (`handlers.py`)

- `handle_player_search()`: Existing player search functionality
- `handle_player_comparison()`: New player comparison functionality
- `handle_stats_explanation()`: Explains football statistics
- `handle_casual_chat()`: Handles general conversation

### Response (`response.py`)

- Natural language response generation utilities
- Format different response types into user-friendly text

## Supported Intents

The orchestrator recognizes the following user intents:

1. **player_search**: Finding players matching specific criteria
   - "Find me technical midfielders with good passing"
   - "Show me attackers who score a lot of goals"

2. **player_comparison**: Comparing multiple players
   - "Compare these two players"
   - "Which of these forwards is better at scoring?"

3. **explain_stats**: Explaining football statistics
   - "What is xG?"
   - "Explain progressive passes"

4. **casual_conversation**: General chat
   - "Hello"
   - "Thank you"

## New API Endpoints

The orchestrator implementation adds several new endpoints:

- `/player_comparison`: Compare multiple players across key metrics
- `/explain_stats`: Get explanations for football statistics
- `/follow_up_suggestions/<session_id>`: Get context-aware follow-up suggestions

The existing `/enhanced_search` endpoint has been updated to use the orchestrator.

## How It Works

1. When a user sends a message, it first goes through the `process_user_message()` function
2. The message is analyzed by `identify_intent()` to determine the user's intention
3. Relevant entities are extracted based on the intent
4. The message is routed to the appropriate handler based on intent
5. The handler processes the message and returns structured data
6. The response is formatted into natural language and returned to the user

## Example Flow

User: "Find me midfielders with good passing skills"

1. Intent identified: player_search (confidence: 0.95)
2. Extract search parameters (position_codes: ["cmf", "amf"], passing thresholds)
3. Route to `handle_player_search()`
4. Search database for matching players
5. Format response with player details
6. Generate follow-up suggestions like "Show me younger players" or "Compare top two players"

## Future Enhancements

Potential future enhancements for the orchestrator:

1. More sophisticated entity extraction
2. Learning from conversation history to improve recommendations
3. Integration with user preferences
4. Support for multi-turn complex queries
5. Team composition recommendations

## Testing

See `HOW_TO_TEST.md` for instructions on testing the orchestrator implementation.