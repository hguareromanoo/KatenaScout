"""
KatenaScout - Main Application

This is the main application file that initializes the Flask app and defines routes.
The routes are kept clean by delegating business logic to the core modules.
"""

import os
import json
import tempfile
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

# Import core components
from core.session import UnifiedSession
from models.parameters import SearchParameters

# Import scout report components
from core.processor import ScoutReportProcessor, TranslationManager
from core.generator import generate_scout_report_html, generate_scout_report_pdf

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
@app.route('/players/search', methods=['GET'])
def search_players_by_name():
    """Lightweight endpoint for searching players directly by name"""
    try:
        # Get query parameters
        query = request.args.get('query', '')
        limit = int(request.args.get('limit', 15))
        
        # Directly search players in database by name
        from services.data_service import get_player_database, get_team_names
        db = get_player_database()
        teams = get_team_names()
        
        matched_players = []
        query_lower = query.lower() if query else ''
        
        # If query is empty, return popular players (up to the limit)
        if not query:
            # Just return most common players
            player_count = 0
            for name, player in db.items():
                if player_count >= limit:
                    break
                
                # Skip if player has no ID
                if not player.get('wyId') and not player.get('id'):
                    continue
                
                # Format response data with only necessary fields
                matched_players.append({
                    "id": player.get('wyId') or player.get('id'),
                    "name": name,
                    "team": {
                        "name": teams.get(str(player.get('currentTeamId')), {}).get('name', 'Unknown Team') 
                    },
                    "positions": player.get('positions', []),
                    "image_url": f"/player-image/{player.get('wyId') or player.get('id')}"
                })
                player_count += 1
                
            return jsonify({"success": True, "players": matched_players})
        
        # Regular search logic for when query is not empty
        for name, player in db.items():
            # Skip if player has no ID
            if not player.get('wyId') and not player.get('id'):
                continue
                
            # Check if player name contains query
            name_lower = name.lower()
            if query_lower in name_lower:
                # Add relevance score - exact matches or starts with are prioritized
                score = 0
                if name_lower == query_lower:
                    score = 100  # Exact match
                elif name_lower.startswith(query_lower):
                    score = 75   # Starts with
                else:
                    score = 50   # Contains
                    
                # Format response data with only necessary fields
                matched_players.append({
                    "id": player.get('wyId') or player.get('id'),
                    "name": name,
                    "team": {
                        "name": teams.get(str(player.get('currentTeamId')), {}).get('name', 'Unknown Team')
                    },
                    "positions": player.get('positions', []),
                    "image_url": f"/player-image/{player.get('wyId') or player.get('id')}",
                    "score": score  # For sorting by relevance
                })
        
        # Sort by relevance score and limit results
        matched_players.sort(key=lambda p: p.pop('score', 0), reverse=True)
        return jsonify({"success": True, "players": matched_players[:limit]})
        
    except Exception as e:
        print(f"Error searching players by name: {str(e)}")
        return jsonify({
            "success": False,
            "error": "search_error",
            "message": "An error occurred while searching for players."
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
            # Print debug info for in-chat comparison flag
            print(f"DEBUG - Player comparison response with in_chat_comparison: {response_data.get('in_chat_comparison', False)}")
            
            return jsonify(format_comparison_response(
                players=response_data["players"],
                comparison_text=response_data["text"],
                comparison_aspects=response_data["comparison_aspects"],
                language=language,
                in_chat_comparison=response_data.get("in_chat_comparison", False)
            ))
        elif response_data["type"] == "error":
            from utils.formatters import format_error_response
            return jsonify(format_error_response(
                error="processing_error",
                message=response_data["message"],
                language=language
            ))
        else:
            # Text response or other types (like the modified comparison handler, explain_stats, casual_chat, fallback)
            return jsonify({
                "success": True,
                "type": response_data.get("type", "text"), # Include the type from the handler
                "response": response_data.get("text", ""), # Use .get for safety
                "language": language,
                # Include other potential fields if the handler provides them (e.g., explanations)
                **{k: v for k, v in response_data.items() if k not in ['success', 'type', 'text', 'language']}
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
        "include_ai_analysis": false (optional, defaults to false),
        "playing_style": "possession_based" (optional),
        "formation": "4-3-3" (optional)
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
        
        # Extract additional tactical parameters directly from request data
        # Assuming validator might not handle these yet, provide defaults
        playing_style = data.get("playing_style", "") # Get from original data
        formation = data.get("formation", "")       # Get from original data
        
        # Get session
        session = session_manager.get_session(session_id, language)
        players = []
        # Find players for comparison (from direct API)
        from core.player_search import get_player_info
        from services.data_service import get_player_database, get_player_database_by_id
        db = get_player_database()
        db_by_id = get_player_database_by_id()
        search_params = SearchParameters(**session.last_search_params)
        for player_id in player_ids:
            player = get_player_info(player_id, database=db,database_id=db_by_id,params=search_params)
            if player:
                players.append(player)
            else:
                print(f"Player with ID {player_id} not found in the database.")
        




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
            # Generate comparison with text analysis, including tactical parameters if provided
            from core.comparison import compare_players
            comparison_result = compare_players(
                players=players,
                session_manager=session_manager,
                language=language,
                playing_style=playing_style,
                formation=formation
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
                            continue
                    
                    # Check if it's a URL
                    elif image_data_url and isinstance(image_data_url, str) and (image_data_url.startswith('http://') or image_data_url.startswith('https://')):
                        try:
                            # Try to fetch the image
                            response = requests.get(image_data_url, timeout=5)
                            if response.status_code == 200:
                                # Get the content type
                                content_type = response.headers.get('Content-Type', 'image/jpeg')
                                # Return the image with CORS headers
                                flask_response = app.response_class(response.content, mimetype=content_type)
                                return add_cors_headers(flask_response)
                        except Exception as e:
                            print(f"Error fetching image from URL {image_data_url}: {str(e)}")
                            continue
        
        # If we couldn't find an image in the database, try to find a local file
        try:
            # Check if the player image exists in the local directory
            if os.path.exists(PLAYER_IMAGES_DIR):
                # Try different file extensions
                for ext in ['jpg', 'jpeg', 'png', 'webp']:
                    image_path = os.path.join(PLAYER_IMAGES_DIR, f"{safe_id}.{ext}")
                    if os.path.exists(image_path):
                        response = send_from_directory(PLAYER_IMAGES_DIR, f"{safe_id}.{ext}")
                        return add_cors_headers(response)
        except Exception as e:
            print(f"Error serving local image: {str(e)}")
        
        # If we still couldn't find an image, return a default image
        try:
            default_image_path = os.path.join(PLAYER_IMAGES_DIR, "default.png")
            if os.path.exists(default_image_path):
                response = send_from_directory(PLAYER_IMAGES_DIR, "default.png")
                return add_cors_headers(response)
        except Exception as e:
            print(f"Error serving default image: {str(e)}")
        
        # If all else fails, return a 404
        return jsonify({"error": "Image not found"}), 404
    
    except Exception as e:
        print(f"Error in player image endpoint: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@app.route('/scout_report', methods=['POST'])
def generate_scout_report():
    """
    Endpoint for generating a scout report for a player
    
    Request:
    {
        "session_id": "unique-session-id",
        "player_id": "12345",
        "language": "pt" (optional, defaults to "pt"),
        "format": "html" (optional, defaults to "html")
    }
    
    Response:
    - If format is "html":
        HTML content of the report
    - If format is "pdf":
        PDF file download
    - If error:
        {
            "success": false,
            "error": "error_code",
            "message": "Error message",
            "language": "language"
        }
    """
    try:
        data = request.json
        
        # Validate request data
        if not data:
            return jsonify({
                "success": False,
                "error": "invalid_request",
                "message": "Request body is required",
                "language": "english"
            })
        
        # Check if session_id is provided
        if "session_id" not in data:
            return jsonify({
                "success": False,
                "error": "invalid_request",
                "message": "session_id is required",
                "language": "english"
            })
        
        # Check if player_id is provided
        if "player_id" not in data:
            return jsonify({
                "success": False,
                "error": "invalid_request",
                "message": "player_id is required",
                "language": "english"
            })
        
        # Extract data
        session_id = data["session_id"]
        player_id = str(data["player_id"])
        language = data.get("language", "pt")
        format_type = data.get("format", "html").lower()
        
        # Validate language
        if language not in TranslationManager.SUPPORTED_LANGUAGES:
            return jsonify({
                "success": False,
                "error": "invalid_language",
                "message": f"Unsupported language. Supported languages: {', '.join(TranslationManager.SUPPORTED_LANGUAGES)}",
                "language": "english"
            })
        
        # Validate format
        if format_type not in ["html", "pdf"]:
            return jsonify({
                "success": False,
                "error": "invalid_format",
                "message": "Unsupported format. Supported formats: html, pdf",
                "language": language
            })
        
        # Get session
        session = session_manager.get_session(session_id, language)
        
        # Add request to session history
        session.messages.append({
            "role": "user",
            "content": f"Generate scout report for player {player_id}"
        })
        
        # Create a temporary directory for the report
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Get player info to verify player exists
                from services.data_service import find_player_by_id
                player = find_player_by_id(player_id)
                
                if not player:
                    # Add error to session history
                    session.messages.append({
                        "role": "assistant",
                        "content": f"Player with ID {player_id} not found."
                    })
                    
                    return jsonify({
                        "success": False,
                        "error": "player_not_found",
                        "message": f"Player with ID {player_id} not found.",
                        "language": language
                    })
                
                # Generate the report
                if format_type == "pdf":
                    # Generate PDF report
                    report_path = generate_scout_report_pdf(player_id, language, temp_dir)
                    
                    # Add success to session history
                    session.messages.append({
                        "role": "assistant",
                        "content": f"Scout report for {player.get('name', player_id)} generated successfully in PDF format."
                    })
                    
                    # Return the PDF file
                    return send_file(
                        report_path,
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name=f"scout_report_{player_id}_{language}.pdf"
                    )
                else:
                    # Generate HTML report
                    report_path = generate_scout_report_html(player_id, language, temp_dir)
                    
                    # Add success to session history
                    session.messages.append({
                        "role": "assistant",
                        "content": f"Scout report for {player.get('name', player_id)} generated successfully in HTML format."
                    })
                    
                    # Read the HTML content
                    with open(report_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    # Return the HTML content
                    return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
            
            except Exception as e:
                error_message = f"Error generating scout report: {str(e)}"
                print(error_message)
                
                # Add error to session history
                session.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
                
                return jsonify({
                    "success": False,
                    "error": "generation_error",
                    "message": error_message,
                    "language": language
                })
    
    except Exception as e:
        error_message = f"Error in scout report endpoint: {str(e)}"
        print(error_message)
        
        return jsonify({
            "success": False,
            "error": "server_error",
            "message": "An unexpected error occurred. Please try again.",
            "language": "english"
        })

@app.route('/scout_report/<player_id>', methods=['GET'])
def get_scout_report(player_id):
    """
    Endpoint for getting a scout report for a player via GET request
    
    Query parameters:
    - session_id: Session ID (required)
    - language: Language of the report (optional, defaults to "pt")
    - format: Format of the report (optional, defaults to "html")
    
    Response:
    - If format is "html":
        HTML content of the report
    - If format is "pdf":
        PDF file download
    - If error:
        {
            "success": false,
            "error": "error_code",
            "message": "Error message",
            "language": "language"
        }
    """
    try:
        # Get query parameters
        session_id = request.args.get('session_id')
        language = request.args.get('language', 'pt')
        format_type = request.args.get('format', 'html').lower()
        
        # Validate session_id
        if not session_id:
            return jsonify({
                "success": False,
                "error": "invalid_request",
                "message": "session_id is required",
                "language": "english"
            })
        
        # Validate language
        if language not in TranslationManager.SUPPORTED_LANGUAGES:
            return jsonify({
                "success": False,
                "error": "invalid_language",
                "message": f"Unsupported language. Supported languages: {', '.join(TranslationManager.SUPPORTED_LANGUAGES)}",
                "language": "english"
            })
        
        # Validate format
        if format_type not in ["html", "pdf"]:
            return jsonify({
                "success": False,
                "error": "invalid_format",
                "message": "Unsupported format. Supported formats: html, pdf",
                "language": language
            })
        
        # Get session
        session = session_manager.get_session(session_id, language)
        
        # Add request to session history
        session.messages.append({
            "role": "user",
            "content": f"Generate scout report for player {player_id}"
        })
        
        # Create a temporary directory for the report
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Get player info to verify player exists
                from services.data_service import find_player_by_id
                player = find_player_by_id(player_id)
                
                if not player:
                    # Add error to session history
                    session.messages.append({
                        "role": "assistant",
                        "content": f"Player with ID {player_id} not found."
                    })
                    
                    return jsonify({
                        "success": False,
                        "error": "player_not_found",
                        "message": f"Player with ID {player_id} not found.",
                        "language": language
                    })
                
                # Generate the report
                if format_type == "pdf":
                    # Generate PDF report
                    report_path = generate_scout_report_pdf(player_id, language, temp_dir)
                    
                    # Add success to session history
                    session.messages.append({
                        "role": "assistant",
                        "content": f"Scout report for {player.get('name', player_id)} generated successfully in PDF format."
                    })
                    
                    # Return the PDF file
                    return send_file(
                        report_path,
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name=f"scout_report_{player_id}_{language}.pdf"
                    )
                else:
                    # Generate HTML report
                    report_path = generate_scout_report_html(player_id, language, temp_dir)
                    
                    # Add success to session history
                    session.messages.append({
                        "role": "assistant",
                        "content": f"Scout report for {player.get('name', player_id)} generated successfully in HTML format."
                    })
                    
                    # Read the HTML content
                    with open(report_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    # Return the HTML content
                    return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
            
            except Exception as e:
                error_message = f"Error generating scout report: {str(e)}"
                print(error_message)
                
                # Add error to session history
                session.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
                
                return jsonify({
                    "success": False,
                    "error": "generation_error",
                    "message": error_message,
                    "language": language
                })
    
    except Exception as e:
        error_message = f"Error in scout report endpoint: {str(e)}"
        print(error_message)
        
        return jsonify({
            "success": False,
            "error": "server_error",
            "message": "An unexpected error occurred. Please try again.",
            "language": "english"
        })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
