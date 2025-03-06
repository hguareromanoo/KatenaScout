import json
import requests
import base64

username = "l1jsi8z-rk2cscjeh-yksn0zo-ss56jtursm"
password = "#(cIoC&CoG:8VhEh8zW7thwBqPwoJq"
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
auth_header = {
    "Authorization": f"Basic {encoded_credentials}"
}

with open('backend/database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

team_dict = {}
teamId = []

# Extract unique team IDs
for player_name, player_data in data.items():
    if 'currentTeamId' in player_data and player_data['currentTeamId'] is not None:
        team_id = player_data['currentTeamId']
        if team_id not in teamId:
            teamId.append(team_id)

print(f"Found {len(teamId)} unique team IDs")

# Fetch team information for each ID
for team in teamId:
    url = f'https://apirest.wyscout.com/v3/teams/{team}'
    print(f"Requesting data for team ID: {team}")
    response = requests.get(url, headers=auth_header)
    if response.status_code != 200:
        print(f"Error for team ID {team}: Status code {response.status_code}")
        continue
    
    team_data = response.json()
    team_name = team_data.get("name", "")
    team_image = team_data.get("imageDataURL", "")
    team_dict[team] = {"name": team_name, "image": team_image}
    print(f"Successfully retrieved data for team: {team_name}")

with open("team.json", "w", encoding='utf-8') as file:
    json.dump(team_dict, file, indent=2)
    print(f"Retrieved {len(team_dict)} teams.")