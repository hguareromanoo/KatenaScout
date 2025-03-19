#!/usr/bin/env python3
"""
Script to fetch all player images from database.json and save them locally.
This helps with caching images and reducing dependency on external services.
"""

import os
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import unidecode

# Constants
DATABASE_FILE = 'database.json'
DB_BY_ID_FILE = 'db_by_id.json'
OUTPUT_DIR = 'player_images'
DEFAULT_TIMEOUT = 5  # seconds
MAX_RETRIES = 3
MAX_WORKERS = 10  # Number of concurrent downloads
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'


def sanitize_player_id(player_id):
    """Sanitize player ID to prevent path traversal and other issues"""
    if not player_id:
        return "unknown"
    return str(player_id).replace("/", "").replace("\\", "").replace("..", "").replace("%", "")


def load_database():
    """Load the player database"""
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            db = json.load(f)
            print(f"Loaded {len(db)} players from database")
            return db
    except Exception as e:
        print(f"Error loading database: {str(e)}")
        return {}


def download_image(player_name, player_id, image_url, output_dir, session):
    """Download a single player image with retries"""
    if not image_url or not image_url.startswith('http'):
        return False, None, f"Invalid URL: {image_url}"
    
    safe_id = sanitize_player_id(player_id)
    output_path = os.path.join(output_dir, f"{safe_id}.png")
    
    # Skip if already downloaded
    if os.path.exists(output_path):
        return True, output_path, "Already exists"
    
    # Try to download with retries
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(image_url, timeout=DEFAULT_TIMEOUT)
            if response.status_code == 200:
                # Ensure directory exists
                os.makedirs(output_dir, exist_ok=True)
                
                # Save the image
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                return True, output_path, "Success"
            
            elif response.status_code == 404:
                return False, None, f"Image not found (404): {image_url}"
            else:
                error_msg = f"HTTP error {response.status_code}"
                if attempt < MAX_RETRIES - 1:
                    time.sleep(1)  # Wait before retry
        except requests.exceptions.Timeout:
            error_msg = "Timeout"
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)
        except Exception as e:
            error_msg = str(e)
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)
    
    return False, None, f"Failed after {MAX_RETRIES} attempts: {error_msg}"


def download_all_images(db, output_dir):
    """Download all player images using a thread pool"""
    # Create session for connection pooling
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    
    # Collect all download tasks
    tasks = []
    image_fields = ['imageDataURL', 'photoUrl', 'profileUrl', 'image', 'photo', 'profileImage']
    
    for player_name, player_data in db.items():
        player_id = player_data.get('playerId') or player_data.get('wyId')
        if not player_id:
            continue
        
        # Find image URL (try each possible field)
        image_url = None
        for field in image_fields:
            if field in player_data and player_data[field]:
                image_url = player_data[field]
                break
        
        if image_url:
            tasks.append((player_name, player_id, image_url))
    
    print(f"Found {len(tasks)} players with image URLs")
    
    # Create progress bar
    progress_bar = tqdm(total=len(tasks), desc="Downloading images")
    
    # Track results
    success_count = 0
    error_count = 0
    skipped_count = 0
    error_log = []
    
    # Process downloads with thread pool
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for player_name, player_id, image_url in tasks:
            future = executor.submit(
                download_image, player_name, player_id, image_url, output_dir, session
            )
            futures.append((player_name, player_id, future))
        
        # Process results as they complete
        for player_name, player_id, future in futures:
            success, path, message = future.result()
            progress_bar.update(1)
            
            if success and message == "Already exists":
                skipped_count += 1
            elif success:
                success_count += 1
            else:
                error_count += 1
                error_log.append(f"Error for {player_name} (ID: {player_id}): {message}")
    
    progress_bar.close()
    
    # Print summary
    print(f"\nDownload Summary:")
    print(f"  - Successfully downloaded: {success_count}")
    print(f"  - Skipped (already exists): {skipped_count}")
    print(f"  - Errors: {error_count}")
    
    # Save error log if there are errors
    if error_log:
        error_log_path = os.path.join(output_dir, "download_errors.log")
        with open(error_log_path, 'w') as f:
            f.write("\n".join(error_log))
        print(f"Error log saved to: {error_log_path}")


def create_default_avatar():
    """Create a simple default avatar if it doesn't exist"""
    default_path = os.path.join(OUTPUT_DIR, "default_avatar.png")
    
    # Skip if already exists
    if os.path.exists(default_path):
        print("Default avatar already exists")
        return
    
    # Try to download a generic placeholder avatar
    try:
        placeholder_url = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png"
        response = requests.get(placeholder_url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            # Ensure directory exists
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            
            # Save the image
            with open(default_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Created default avatar: {default_path}")
        else:
            print(f"Failed to download default avatar: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error creating default avatar: {str(e)}")


def main():
    """Main function"""
    print("=== Player Image Downloader ===")
    
    # Load database
    db = load_database()
    if not db:
        print("No players found in database. Exiting.")
        return
    
    # Create default avatar
    create_default_avatar()
    
    # Download all images
    download_all_images(db, OUTPUT_DIR)
    
    print("Done!")


if __name__ == "__main__":
    main()