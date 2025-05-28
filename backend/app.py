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

# Database session management
from backend.database import get_db
from sqlalchemy.orm import Session

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
        query_param = request.args.get('query', '')
        limit = int(request.args.get('limit', 15))

        db_gen = get_db()
        db: Session = next(db_gen)
        matched_players_data = []

        try:
            # Import necessary models and converters
            from backend.models.sql_models import Player as PlayerModel
            from backend.utils.converters import convert_player_model_to_pydantic_summary
            from sqlalchemy import func as sql_alchemy_func_app # Alias for SQLAlchemy func

            if not query_param:
                # "Popular players" - replaced with fetching first N players.
                all_players_sql = db.query(PlayerModel).limit(limit).all()
                for player_sql in all_players_sql:
                    pydantic_summary = convert_player_model_to_pydantic_summary(player_sql)
                    matched_players_data.append(pydantic_summary.model_dump())
            else:
                name_query_lower = query_param.lower()
                players_sql = db.query(PlayerModel).filter(
                    sql_alchemy_func_app.lower(PlayerModel.name).contains(name_query_lower)
                ).limit(limit).all()

                for player_sql in players_sql:
                    # Relevance score (simplified)
                    score = 0
                    if player_sql.name.lower() == name_query_lower: score = 100
                    elif player_sql.name.lower().startswith(name_query_lower): score = 75
                    else: score = 50
                    
                    pydantic_summary = convert_player_model_to_pydantic_summary(player_sql, score=score)
                    matched_players_data.append(pydantic_summary.model_dump())
            
            # Sort by 'score' if present, Pydantic model_dump() creates dicts.
            matched_players_data.sort(key=lambda p: p.get('score', 0), reverse=True)
            return jsonify({"success": True, "players": matched_players_data})

        finally:
            next(db_gen, None) # Ensure session is closed
            
    except Exception as e:
        print(f"Error searching players by name: {str(e)}") # Keep existing logging
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
        
        db_gen = get_db()
        db: Session = next(db_gen)
        try:
            # Handle based on intent
            from core.handlers import (
                handle_player_search, 
                handle_player_comparison, 
                handle_stats_explanation, 
                handle_casual_chat, 
                handle_fallback
            )
            
            # Pass db to handlers
            if intent.name == "player_search":
                response_data = handle_player_search(session, query, session_manager, db)
            elif intent.name == "player_comparison":
                response_data = handle_player_comparison(session, query, session_manager, db)
            elif intent.name == "explain_stats":
                response_data = handle_stats_explanation(session, query, session_manager, db)
            elif intent.name == "casual_conversation":
                response_data = handle_casual_chat(session, query, session_manager, db)
            else:
                response_data = handle_fallback(session, query, session_manager, db)
            
            # Format the response based on response type (this part remains the same)
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
            else: # Text response or other types
                return jsonify({
                    "success": True,
                    "type": response_data.get("type", "text"),
                    "response": response_data.get("text", ""),
                    "language": language,
                    **{k: v for k, v in response_data.items() if k not in ['success', 'type', 'text', 'language']}
                })
        finally:
            next(db_gen, None) # Close session
        
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
        db_gen = get_db()
        db: Session = next(db_gen)
        players_data = [] # Renamed to avoid conflict
        try:
            # Get session
            session = session_manager.get_session(session_id, language) # session already fetched earlier, this is fine

            # Find players for comparison. session_manager.get_players_info now requires db.
            search_params_obj = SearchParameters(**session.last_search_params) if session.last_search_params else None
            
            for player_id_str_req in player_ids: # player_ids from request are strings
                # session_manager.get_players_info expects player_id_str and db
                player_detail = session_manager.get_players_info(player_id_str=player_id_str_req, db=db, params=search_params_obj)
                if player_detail and not player_detail.get('error'):
                    players_data.append(player_detail)
                else:
                    print(f"Player with ID {player_id_str_req} not found or error fetching details.")
            
            if len(players_data) < 2:
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
                # Generate comparison with text analysis, including tactical parameters
                from core.comparison import compare_players as compare_players_core
                # Pass db to compare_players_core if it needs to fetch more data
                comparison_result = compare_players_core(
                    players=players_data,
                    session_manager=session_manager,
                    language=language,
                    playing_style=playing_style,
                    formation=formation,
                    db=db 
                )
                
                comparison_text = comparison_result.get("comparison", "")
                comparison_aspects = comparison_result.get("comparison_aspects", comparison_aspects)
                enhanced_data = comparison_result.get("enhanced_data", {})
                
                session.messages.append({"role": "assistant", "content": comparison_text})
            else:
                # Use enhanced comparison directly without AI analysis
                from core.enhanced_comparison import enhance_player_comparison
                # Pass db to enhance_player_comparison if it needs to fetch more data
                enhanced_data = enhance_player_comparison(
                    players=players_data,
                    comparison_text="", 
                    search_weights=None, # This might need weights from data_service (which could use db)
                    db=db 
                )
            
            from utils.formatters import format_comparison_response
            return jsonify(format_comparison_response(
                players=players_data,
                comparison_text=comparison_text,
                comparison_aspects=comparison_aspects,
                language=language,
                metric_winners=enhanced_data.get("metric_winners", {}),
                overall_winner=enhanced_data.get("overall_winner", {}),
                categorized_metrics=enhanced_data.get("categorized_metrics", {}),
                category_winners=enhanced_data.get("category_winners", {}),
                negative_metrics=enhanced_data.get("negative_metrics", [])
            ))
        finally:
            next(db_gen, None) # Close session
            
    except Exception as e:
        print(f"Error in player comparison endpoint: {str(e)}") # Logging
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
        
        db_gen = get_db()
        db: Session = next(db_gen)
        player_obj = None
        try:
            # Create a safe player ID string with additional security checks
            safe_id_int = 0
            try:
                safe_id_int = int(sanitize_player_id(player_id))
            except ValueError:
                return jsonify({"error": "Invalid player ID format"}), 400

            from services.data_service import find_player_by_id as find_player_by_id_service
            player_obj = find_player_by_id_service(player_id=safe_id_int, db=db) # Pass db session
            
            # The PRD states player image URL isn't in the Player model.
            # The old logic for image_fields ('imageDataURL', 'photoUrl', etc.) was based on JSON.
            # This needs to be re-evaluated based on FR8.
            # For now, if player_obj exists, we assume no direct image URL is on it.
            # The old code had a complex fallback. This route will simplify to local file check primarily.

            # Local file check (current primary logic if DB doesn't store URL)
            if os.path.exists(PLAYER_IMAGES_DIR):
                for ext in ['jpg', 'jpeg', 'png', 'webp']:
                    # Use safe_id_int (which is an int) for constructing filename if IDs are numeric
                    image_path = os.path.join(PLAYER_IMAGES_DIR, f"{safe_id_int}.{ext}")
                    if os.path.exists(image_path):
                        response = send_from_directory(PLAYER_IMAGES_DIR, f"{safe_id_int}.{ext}")
                        return add_cors_headers(response)
            
            # Default image if no specific one is found
            default_image_path = os.path.join(PLAYER_IMAGES_DIR, "default.png")
            if os.path.exists(default_image_path):
                response = send_from_directory(PLAYER_IMAGES_DIR, "default.png")
                return add_cors_headers(response)
            
            return jsonify({"error": "Image not found"}), 404

        finally:
            next(db_gen, None) # Close session

    except Exception as e:
        print(f"Error in player image endpoint: {str(e)}") # Keep existing logging
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
        db_gen = get_db()
        db: Session = next(db_gen)
        try:
            # Create a temporary directory for the report
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    from services.data_service import find_player_by_id as find_player_by_id_service
                    # player_id from request is string, convert to int for DB
                    player_id_int = int(player_id)
                    player_obj = find_player_by_id_service(player_id=player_id_int, db=db)
                    
                    if not player_obj:
                        session.messages.append({"role": "assistant", "content": f"Player with ID {player_id} not found."})
                        return jsonify({"success": False, "error": "player_not_found", "message": f"Player with ID {player_id} not found.", "language": language})
                    
                    player_name_for_report = player_obj.name # Use attribute access

                    if format_type == "pdf":
                        report_path = generate_scout_report_pdf(player_id, language, temp_dir) # generate_scout_report_pdf might need player_obj not just id
                        session.messages.append({"role": "assistant", "content": f"Scout report for {player_name_for_report} generated successfully in PDF format."})
                        return send_file(report_path, mimetype='application/pdf', as_attachment=True, download_name=f"scout_report_{player_id}_{language}.pdf")
                    else: # html
                        report_path = generate_scout_report_html(player_id, language, temp_dir) # Same here, might need player_obj
                        session.messages.append({"role": "assistant", "content": f"Scout report for {player_name_for_report} generated successfully in HTML format."})
                        with open(report_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
                
                except Exception as e:
                    error_message = f"Error generating scout report: {str(e)}"
                    print(error_message)
                    session.messages.append({"role": "assistant", "content": error_message})
                    return jsonify({"success": False, "error": "generation_error", "message": error_message, "language": language})
        finally:
            next(db_gen, None) # Close session
    
    except Exception as e:
        error_message = f"Error in scout report endpoint: {str(e)}" # Keep existing logging
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
        
        db_gen = get_db()
        db: Session = next(db_gen)
        try:
            # Get session
            session = session_manager.get_session(session_id, language)
            session.messages.append({"role": "user", "content": f"Generate scout report for player {player_id}"})

            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    from services.data_service import find_player_by_id as find_player_by_id_service
                    player_id_int = int(player_id) # player_id from path is string
                    player_obj = find_player_by_id_service(player_id=player_id_int, db=db)
                    
                    if not player_obj:
                        session.messages.append({"role": "assistant", "content": f"Player with ID {player_id} not found."})
                        return jsonify({"success": False, "error": "player_not_found", "message": f"Player with ID {player_id} not found.", "language": language})

                    player_name_for_report = player_obj.name

                    if format_type == "pdf":
                        report_path = generate_scout_report_pdf(player_id, language, temp_dir) # Might need player_obj
                        session.messages.append({"role": "assistant", "content": f"Scout report for {player_name_for_report} generated successfully in PDF format."})
                        return send_file(report_path, mimetype='application/pdf', as_attachment=True, download_name=f"scout_report_{player_id}_{language}.pdf")
                    else: # html
                        report_path = generate_scout_report_html(player_id, language, temp_dir) # Might need player_obj
                        session.messages.append({"role": "assistant", "content": f"Scout report for {player_name_for_report} generated successfully in HTML format."})
                        with open(report_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
                
                except Exception as e: # Catches errors from report generation or player not found
                    error_message = f"Error generating scout report: {str(e)}"
                    print(error_message)
                    session.messages.append({"role": "assistant", "content": error_message})
                    return jsonify({"success": False, "error": "generation_error", "message": error_message, "language": language})
        finally:
            next(db_gen, None) # Close session
    
    except Exception as e: # Catches errors like invalid session_id, language, format, or top-level issues
        error_message = f"Error in scout report endpoint GET: {str(e)}"
        print(error_message)
        
        return jsonify({
            "success": False,
            "error": "server_error",
            "message": "An unexpected error occurred. Please try again.",
            "language": "english"
        })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
