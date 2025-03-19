import json
import os
import requests
import base64

username = "l1jsi8z-rk2cscjeh-yksn0zo-ss56jtursm"
password = "#(cIoC&CoG:8VhEh8zW7thwBqPwoJq"
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
auth_header = {
    "Authorization": f"Basic {encoded_credentials}"
}
with open('backend/team.json', 'r', encoding='utf-8') as f:
    teams = json.load(f)
teams_adv_stats ={}    
for team_id, team_data in teams.items():
    response = requests.get(f"https://apirest.wyscout.com/v3/teams/{team_id}/advancedstats", headers=auth_header) 
    if response.status_code != 200:
        print("Error in fetching advanced stats for team with id", team_id)
        continue
    data = response.json()
    teams_adv_stats[team_id] = data
    print("gathered advanced stats for team with id", id)

with open('teams_adv_stats.json', 'w', encoding='utf-8') as f:
    json.dump(teams_adv_stats, f, ensure_ascii=False, indent=4)
print("advanced stats for teams saved in teams_adv_stats.json")

