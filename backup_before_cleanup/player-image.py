from flask import Flask, send_from_directory, jsonify, app, Response
import os
import requests
import unidecode
from env_keys import get_anthropic_api_key, get_openai_api_key
import json
import base64

# Player images directory
PLAYER_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'player_images')
os.makedirs(PLAYER_IMAGES_DIR, exist_ok=True)

# Load necessary data files
def _load_json(filename: str) -> dict:
    """Load a JSON file, trying different paths"""
    paths = [
        filename,  # Current directory
        f'backend/{filename}',  # Backend subdirectory
        f'../backend/{filename}'  # Parent directory's backend
    ]
    
    for path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            continue
    
    raise FileNotFoundError(f"Could not find {filename} in any expected location")

# Load the database
database = _load_json('database.json')
database_id = _load_json('db_by_id.json')

@app.route('/player-image/<player_id>', methods=['GET'])
def player_image(player_id):
    """
    Endpoint to serve player images
    
    First tries to get the image from the database, then from local files,
    then returns a default image if none is found
    """
    try:
        # Create a safe player ID string
        safe_id = str(player_id).replace("/", "").replace("..", "")
        
        # First, try to retrieve the player's image from the database
        player = None
        if safe_id in database_id:
            player = database_id[safe_id]
        else:
            # Try to find by name if ID not found
            for name, p_data in database.items():
                # Convert player_id to string for comparison if it exists
                wy_id = str(p_data.get('wyId')) if p_data.get('wyId') is not None else None
                
                if wy_id == safe_id or unidecode.unidecode(name).lower() == safe_id.lower():
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
                            # Return the image
                            response = Response(image_data, mimetype=mime_type)
                            return response
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
                                # Return the image
                                response = Response(img_response.content, mimetype=content_type)
                                return response
                        except Exception as e:
                            print(f"Error fetching image URL from {field}: {str(e)}")
        
        # Second, check for local image files
        for ext in ['.jpg', '.png', '.jpeg']:
            image_path = os.path.join(PLAYER_IMAGES_DIR, f"{safe_id}{ext}")
            if os.path.exists(image_path):
                return send_from_directory(PLAYER_IMAGES_DIR, f"{safe_id}{ext}")
        
        # If no player-specific image is found, return a default image
        default_image = "default.jpg"
        default_path = os.path.join(PLAYER_IMAGES_DIR, default_image)
        
        # Create a simple default image if it doesn't exist
        if not os.path.exists(default_path):
            # Return a placeholder image - base64 encoded transparent 1x1 pixel
            transparent_pixel = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
            response = Response(transparent_pixel, mimetype='image/png')
            return response
            
        return send_from_directory(PLAYER_IMAGES_DIR, default_image)
    except Exception as e:
        print(f"Error serving player image: {str(e)}")
        # Return a transparent pixel as fallback
        transparent_pixel = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
        response = Response(transparent_pixel, mimetype='image/png')
        return response