"""
KatenaScout - Main Application

This is the main application file that initializes the Flask app and defines routes.
The routes are kept clean by delegating business logic to the core modules.
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import core components
from core.session import UnifiedSession
from models.parameters import SearchParameters

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize session manager
session_manager = UnifiedSession()

# ================ ROUTES ================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the service is running"""
    return jsonify({
        "status": "healthy", 
        "message": "Katena Scout Unified API v4.0 is running"
    })

@app.route('/enhanced_search', methods=['POST'])
def enhanced_search():
    """
    Endpoint for enhanced search with conversation memory
    
    Request:
    {
        "session_id": "unique-session-id",
        "query": "Find attackers with high shooting accuracy",
        "is_follow_up": false,
        "satisfaction": true/false/null,
        "language": "english" (optional)
    }
    
    Response:
    {
        "success": true,
        "response": "Natural language response with player recommendations",
        "satisfaction_question": "Are you satisfied with these players?",
        "players": [... array of player objects with scores ...],
        "language": "english"
    }
    """
    try:
        data = request.json
        
        # Validate request data
        from utils.validators import validate_search_request
        valid, error_msg, validated_data = validate_search_request(data)
        
        if not valid:
            from utils.formatters import format_error_response
            return jsonify(format_error_response(
                error="invalid_request", 
                message=error_msg,
                language=validated_data.get("language", "english")
            ))
        
        # Extract validated data
        session_id = validated_data["session_id"]
        query = validated_data["query"]
        is_follow_up = validated_data["is_follow_up"]
        satisfaction = validated_data["satisfaction"]
        language = validated_data["language"]
        
        # Get session
        session = session_manager.get_session(session_id, language)
        
        # Update session with request data
        session.is_follow_up = is_follow_up
        if satisfaction is not None:
            session.satisfaction = satisfaction
        
        # Add user message to session history
        session.messages.append({"role": "user", "content": query})
        
        # Determine the user's intent
        from core.intent import identify_intent, extract_entities
        
        try:
            intent = identify_intent(session, query, session_manager.call_claude_api)
            print(f"Identified intent: {intent.name} with confidence {intent.confidence}")
            session.current_intent = intent.name
            
            # Extract relevant entities based on intent
            entities = extract_entities(session, query, intent, session_manager.call_claude_api)
        except Exception as e:
            # Log the error but continue with a safe default
            print(f"Error in intent recognition: {str(e)}")
            from core.intent import Intent
            intent = Intent(name="casual_conversation", confidence=0.9)
            session.current_intent = intent.name
            entities = {}
        session.entities.update(entities)
        
        # Handle based on intent
        from core.handlers import (
            handle_player_search, 
            handle_player_comparison, 
            handle_stats_explanation, 
            handle_casual_chat, 
            handle_fallback
        )
        
        if intent.name == "player_search":
            response_data = handle_player_search(session, query, session_manager)
        elif intent.name == "player_comparison":
            response_data = handle_player_comparison(session, query, session_manager)
        elif intent.name == "explain_stats":
            response_data = handle_stats_explanation(session, query, session_manager)
        elif intent.name == "casual_conversation":
            response_data = handle_casual_chat(session, query, session_manager)
        else:
            response_data = handle_fallback(session, query, session_manager)
        
        # Format the response based on response type
        if response_data["type"] == "search_results":
            from utils.formatters import format_search_response
            return jsonify(format_search_response(
                players=response_data["players"],
                text_response=response_data["text"],
                language=language,
                follow_up_suggestions=response_data.get("follow_up_suggestions", [])
            ))
        elif response_data["type"] == "player_comparison":
            from utils.formatters import format_comparison_response
            return jsonify(format_comparison_response(
                players=response_data["players"],
                comparison_text=response_data["text"],
                comparison_aspects=response_data["comparison_aspects"],
                language=language
            ))
        elif response_data["type"] == "error":
            from utils.formatters import format_error_response
            return jsonify(format_error_response(
                error="processing_error",
                message=response_data["message"],
                language=language
            ))
        else:
            # Text response or other types
            return jsonify({
                "success": True,
                "response": response_data["text"],
                "language": language
            })
    
    except Exception as e:
        print(f"Error in enhanced search endpoint: {str(e)}")
        from utils.formatters import format_error_response
        return jsonify(format_error_response(
            error="server_error",
            message="An unexpected error occurred. Please try again.",
            language="english"
        ))

@app.route('/player_comparison', methods=['POST'])
def compare_players():
    """
    Endpoint for comparing players
    
    Request:
    {
        "session_id": "unique-session-id",
        "player_ids": ["player_id_1", "player_id_2"],
        "language": "english" (optional),
        "include_ai_analysis": false (optional, defaults to false)
    }
    
    Response:
    {
        "success": true,
        "comparison": "Natural language comparison of the players (if requested)",
        "comparison_aspects": ["Passing", "Shooting", "Defense", "Physical"],
        "players": [... array of player objects ...],
        "language": "english",
        "metric_winners": {...},
        "overall_winner": {...},
        "categorized_metrics": {...},
        "category_winners": {...}
    }
    """
    try:
        data = request.json
        
        # Validate request data
        from utils.validators import validate_comparison_request
        valid, error_msg, validated_data = validate_comparison_request(data)
        
        if not valid:
            from utils.formatters import format_error_response
            return jsonify(format_error_response(
                error="invalid_request", 
                message=error_msg,
                language=validated_data.get("language", "english")
            ))
        
        # Extract validated data
        session_id = validated_data["session_id"]
        player_ids = validated_data["player_ids"]
        language = validated_data["language"]
        include_ai_analysis = validated_data.get("include_ai_analysis", False)
        
        # Get session
        session = session_manager.get_session(session_id, language)
        
        # Find players for comparison
        from core.comparison import find_players_for_comparison
        players = find_players_for_comparison(
            session_manager,
            session_id,
            player_ids,
            language
        )
        
        # Ensure we have at least 2 players to compare
        if len(players) < 2:
            from utils.formatters import format_error_response
            return jsonify(format_error_response(
                error="insufficient_players",
                message="Could not find enough valid players to compare",
                language=language
            ))
        
        # Initialize vars for result
        comparison_text = ""
        comparison_aspects = ["Technical", "Physical", "Mental", "Experience"]
        
        # If AI analysis is requested, use the standard comparison function
        if include_ai_analysis:
            # Generate comparison with text analysis
            from core.comparison import compare_players
            comparison_result = compare_players(
                players=players,
                session_manager=session_manager,
                language=language
            )
            
            comparison_text = comparison_result.get("comparison", "")
            comparison_aspects = comparison_result.get("comparison_aspects", comparison_aspects)
            enhanced_data = comparison_result.get("enhanced_data", {})
            
            # Add to session history
            session.messages.append({
                "role": "assistant", 
                "content": comparison_text
            })
        else:
            # Use enhanced comparison directly without AI analysis
            from core.enhanced_comparison import enhance_player_comparison
            enhanced_data = enhance_player_comparison(
                players=players,
                comparison_text="",  # No AI text to process
                search_weights=None
            )
        
        # Format response
        from utils.formatters import format_comparison_response
        
        return jsonify(format_comparison_response(
            players=players,
            comparison_text=comparison_text,
            comparison_aspects=comparison_aspects,
            language=language,
            metric_winners=enhanced_data.get("metric_winners", {}),
            overall_winner=enhanced_data.get("overall_winner", {}),
            categorized_metrics=enhanced_data.get("categorized_metrics", {}),
            category_winners=enhanced_data.get("category_winners", {}),
            negative_metrics=enhanced_data.get("negative_metrics", [])
        ))
        
    except Exception as e:
        print(f"Error in player comparison endpoint: {str(e)}")
        from utils.formatters import format_error_response
        return jsonify(format_error_response(
            error="server_error",
            message="An error occurred while comparing players. Please try again.",
            language="english"
        ))

@app.route('/player-image/<player_id>', methods=['GET'])
def player_image(player_id):
    """
    Endpoint to serve player images
    
    First tries to get the image from the database, then from local files,
    then returns a default image if none is found
    """
    from utils.validators import sanitize_player_id
    from flask import send_from_directory
    import os
    import requests
    import base64
    import unidecode
    from config import PLAYER_IMAGES_DIR
    
    # Add proper CORS headers to allow the image to be accessed from frontend
    def add_cors_headers(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
        
    try:
        # Create a safe player ID string with additional security checks
        safe_id = sanitize_player_id(player_id)
        
        # First, try to retrieve the player's image from the database
        from services.data_service import find_player_by_id, get_player_database
        player = find_player_by_id(safe_id)
        
        if not player:
            # Try to find by name if ID not found
            db = get_player_database()
            # Convert player_id to string for comparison
            for name, p_data in db.items():
                # Convert player_id to string for comparison if it's not already
                player_id_str = str(player_id) if not isinstance(player_id, str) else player_id
                # Convert wyId to string for comparison if it exists
                wy_id = str(p_data.get('wyId')) if p_data.get('wyId') is not None else None
                
                if wy_id == player_id_str or unidecode.unidecode(name).lower() == safe_id.lower():
                    player = p_data
                    break
        
        # Try multiple possible fields for player images
        image_fields = ['imageDataURL', 'photoUrl', 'profileUrl', 'image', 'photo', 'profileImage']
        
        # If we found the player and they have an image field
        if player:
            # Try each possible image field
            for field in image_fields:
                if player.get(field):
                    image_data_url = player.get(field)
                    
                    # Check if it's a valid base64 image
                    if image_data_url and isinstance(image_data_url, str) and image_data_url.startswith('data:image'):
                        try:
                            # Split the header from the base64 data
                            header, encoded = image_data_url.split(",", 1)
                            # Get the mime type
                            mime_type = header.split(";")[0].replace("data:", "")
                            # Decode the base64 data
                            image_data = base64.b64decode(encoded)
                            # Return the image with CORS headers
                            response = app.response_class(image_data, mimetype=mime_type)
                            return add_cors_headers(response)
                        except Exception as e:
                            print(f"Error decoding image data URL from {field}: {str(e)}")
                    
                    # Check if it's a URL to an external image
                    elif image_data_url and isinstance(image_data_url, str) and (image_data_url.startswith('http://') or image_data_url.startswith('https://')):
                        try:
                            # Fetch the image
                            img_response = requests.get(image_data_url, timeout=2)
                            if img_response.status_code == 200:
                                # Get the content type
                                content_type = img_response.headers.get('Content-Type', 'image/jpeg')
                                # Return the image with CORS headers
                                response = app.response_class(img_response.content, mimetype=content_type)
                                return add_cors_headers(response)
                        except Exception as e:
                            print(f"Error fetching image URL from {field}: {str(e)}")
        
        # Second, check for local image files
        for ext in ['.jpg', '.png', '.jpeg']:
            image_path = os.path.join(PLAYER_IMAGES_DIR, f"{safe_id}{ext}")
            if os.path.exists(image_path):
                response = send_from_directory(PLAYER_IMAGES_DIR, f"{safe_id}{ext}")
                return add_cors_headers(response)
        
        # Finally, return a default avatar image
        default_image_path = os.path.join(PLAYER_IMAGES_DIR, 'default_avatar.png')
        if os.path.exists(default_image_path):
            response = send_from_directory(PLAYER_IMAGES_DIR, 'default_avatar.png')
        else:
            # If default avatar doesn't exist, return generic response
            response = app.response_class(
                b'No image available',
                mimetype='text/plain',
                status=404
            )
        
        return add_cors_headers(response)
        
    except Exception as e:
        print(f"Error serving player image: {str(e)}")
        response = app.response_class(
            b'Error serving image',
            mimetype='text/plain',
            status=500
        )
        return add_cors_headers(response)

@app.route('/follow_up_suggestions/<session_id>', methods=['GET'])
def get_follow_up_suggestions(session_id):
    """
    Get follow-up suggestions for a conversation
    
    This endpoint returns contextual follow-up suggestions based on the 
    current conversation state and most recent search results.
    """
    try:
        # Get language from query parameter or default to English
        language = request.args.get('language', 'english')
        
        # Get session
        session = session_manager.get_session(session_id, language)
        
        # Generate follow-up suggestions based on session state
        from core.intent import generate_follow_up_suggestions
        
        # Get the selected players from the session
        players = session.selected_players if hasattr(session, "selected_players") else []
        
        # Generate suggestions
        suggestions = generate_follow_up_suggestions(session, players)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'language': language
        })
        
    except Exception as e:
        print(f"Error generating follow-up suggestions: {str(e)}")
        from utils.formatters import format_error_response
        return jsonify(format_error_response(
            error="server_error",
            message="An error occurred while generating follow-up suggestions.",
            language="english"
        ))

@app.route('/explain_stats', methods=['POST'])
def explain_stats():
    """
    Endpoint for explaining football statistics
    
    Request:
    {
        "session_id": "unique-session-id",
        "stats": ["xG", "progressive passes", "defensive duels"],
        "language": "english" (optional)
    }
    
    Response:
    {
        "success": true,
        "explanations": { 
            "xG": "Expected Goals (xG) measures...",
            "progressive passes": "Progressive passes are...",
            "defensive duels": "Defensive duels are..."
        },
        "language": "english"
    }
    """
    try:
        data = request.json
        
        # Basic validation
        if not data or 'stats' not in data or not isinstance(data['stats'], list) or not data['stats']:
            return jsonify({
                'success': False,
                'error': "Missing or invalid stats parameter",
                'language': data.get('language', 'english')
            })
        
        # Extract data
        session_id = data.get('session_id', 'default')
        stats = data.get('stats', [])
        language = data.get('language', 'english')
        
        # Get session
        session = session_manager.get_session(session_id, language)
        
        # Add message to session
        stats_request = f"Please explain these football statistics: {', '.join(stats)}"
        session.messages.append({"role": "user", "content": stats_request})
        
        # Set intent and entities
        session.current_intent = "explain_stats"
        session.entities["stats_to_explain"] = stats
        
        # Handle stats explanation
        from core.handlers import handle_stats_explanation
        response_data = handle_stats_explanation(session, stats_request, session_manager)
        
        # Format response
        if response_data["type"] == "stats_explanation":
            return jsonify({
                'success': True,
                'explanations': response_data["explanations"],
                'text': response_data["text"],
                'language': language
            })
        else:
            # Error case
            return jsonify({
                'success': False,
                'error': "Failed to generate explanations",
                'message': response_data.get("message", "An error occurred"),
                'language': language
            })
            
    except Exception as e:
        print(f"Error in explain stats endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': "An error occurred while explaining statistics. Please try again.",
            'language': 'english'
        })

@app.route('/chat_history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """
    Get the chat history for a session
    """
    try:
        # Get language from query parameter or default to English
        language = request.args.get('language', 'english')
        
        # Get session
        session = session_manager.get_session(session_id, language)
        
        # Format messages for client
        formatted_messages = []
        for msg in session.messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            # Skip system messages
            if role == "system":
                continue
                
            formatted_messages.append({
                "role": role,
                "content": content,
                "timestamp": msg.get("timestamp", None)
            })
        
        return jsonify({
            'success': True,
            'messages': formatted_messages,
            'language': language
        })
        
    except Exception as e:
        print(f"Error retrieving chat history: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': "An error occurred while retrieving chat history.",
            'language': 'english'
        })

@app.route('/languages', methods=['GET'])
def get_languages():
    """Get available languages for the app"""
    languages = {
        "english": {
            "code": "en",
            "name": "English",
            "native_name": "English"
        },
        "portuguese": {
            "code": "pt",
            "name": "Portuguese",
            "native_name": "Portugu�s"
        },
        "spanish": {
            "code": "es",
            "name": "Spanish", 
            "native_name": "Espa�ol"
        },
        "bulgarian": {
            "code": "bg",
            "name": "Bulgarian",
            "native_name": "J;30@A:8"
        }
    }
    
    return jsonify({
        "success": True,
        "languages": languages,
        "default": "english"
    })

@app.route('/tactical_analysis', methods=['POST'])
def tactical_analysis():
    """
    Endpoint for tactical analysis of players in specific styles and formations
    
    Request:
    {
        "session_id": "unique-session-id",
        "player_ids": ["player_id_1", "player_id_2"],
        "playing_style": "possession_based",
        "formation": "4-3-3",
        "original_query": "Compare players for possession style",
        "language": "english" (optional)
    }
    
    Response:
    {
        "success": true,
        "tactical_analysis": "Detailed tactical analysis text",
        "tactical_data": {
            "player1_fit": {...},
            "player2_fit": {...},
            "tactical_winner": "player1",
            "winner_name": "Player Name",
            "key_differences": [...],
            "style": "possession_based",
            "style_display_name": "Possession-Based"
        },
        "players": [...],
        "language": "english"
    }
    """
    try:
        data = request.json
        
        # Validate request data
        from utils.validators import validate_tactical_analysis_request
        valid, error_msg, validated_data = validate_tactical_analysis_request(data)
        
        if not valid:
            from utils.formatters import format_error_response
            return jsonify(format_error_response(
                error="invalid_request", 
                message=error_msg,
                language=validated_data.get("language", "english")
            ))
        
        # Extract validated data
        session_id = validated_data["session_id"]
        player_ids = validated_data["player_ids"]
        provided_players = validated_data.get("players", [])
        playing_style = validated_data["playing_style"]
        formation = validated_data["formation"]
        original_query = validated_data["original_query"]
        language = validated_data["language"]
        
        # Get session
        session = session_manager.get_session(session_id, language)
        
        # Use provided players if available, otherwise find by IDs
        players = []
        if provided_players and len(provided_players) == 2:
            # Use the provided complete player objects
            print("Using provided complete player objects for tactical analysis")
            players = provided_players
        else:
            # Find players by IDs
            print("Finding players by IDs for tactical analysis")
            from core.comparison import find_players_for_comparison
            players = find_players_for_comparison(
                session_manager,
                session_id,
                player_ids,
                language
            )
        
        # Ensure we have exactly 2 players to compare
        if len(players) != 2:
            from utils.formatters import format_error_response
            return jsonify(format_error_response(
                error="incorrect_player_count",
                message="Exactly two players are required for tactical analysis",
                language=language
            ))
        
        # Generate tactical analysis
        from core.tactical_analysis import compare_players_tactically, generate_tactical_analysis
        
        # First get the tactical fit data
        tactical_data = compare_players_tactically(
            players=players,
            style=playing_style,
            formation=formation
        )
        
        # Then generate the AI analysis
        analysis_text = generate_tactical_analysis(
            players=players,
            original_query=original_query,
            playing_style=playing_style,
            formation=formation,
            session_manager=session_manager,
            language=language
        )
        
        # Add to session history
        session.messages.append({
            "role": "assistant", 
            "content": f"Tactical Analysis ({playing_style}, {formation}): {analysis_text[:100]}..."
        })
        
        # Format response (using a custom formatter for tactical analysis)
        return jsonify({
            "success": True,
            "tactical_analysis": analysis_text,
            "tactical_data": tactical_data,
            "players": players,
            "language": language
        })
        
    except Exception as e:
        print(f"Error in tactical analysis endpoint: {str(e)}")
        from utils.formatters import format_error_response
        return jsonify(format_error_response(
            error="server_error",
            message="An error occurred during tactical analysis. Please try again.",
            language="english"
        ))

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)