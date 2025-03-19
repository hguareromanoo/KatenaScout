import json
import re

# Load the original database
with open('backend/database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Function to correct player names
def correct_player_name(name):
    # Add a space between lowercase letters (including special characters) and uppercase letters
    corrected_name = re.sub(r'([a-záéíóúñü])([A-ZÁÉÍÓÚÑÜ])', r'\1 \2', name)
    return corrected_name

# Create a new dictionary with corrected names as keys
db_by_id = {}
for player_name, player_data in data.items():
    corrected_name = correct_player_name(player_name)
    db_by_id[corrected_name] = player_data

# Save the new dictionary to db_by_id.json
with open('backend/db_by_id.json', 'w', encoding='utf-8') as f:
    json.dump(db_by_id, f, ensure_ascii=False, indent=4)

print("New database saved to 'backend/db_by_id.json'")