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
teams_adv_stats ={}
for player_id, player_data in data.items():
    if player_data.get("team_id") and player_data.get("team_id") not in teams_adv_stats:
        team_id = player_data["team_id"]
        teams_adv_stats[team_id] = {"competitionId": player_data.get("competition_id"), "seasonId": player_data.get("season_id")}
print(teams_adv_stats)
with open('teams_adv_stats.json', 'w', encoding='utf-8') as f:
    json.dump(teams_adv_stats, f, indent=2)

'''for team_id, team_data in teams_adv_stats.items():
    response = requests.get(f"https://apirest.wyscout.com/v3/teams/{team_id}/advancedstats?compId={team_data.get('competitionId')}&seasonId={team_data.get('seasonId')}", headers=auth_header)
    if response.status_code != 200:
        print("Error in fetching advanced stats for team with id", team_id)
        continue
    data = response.json()
    teams_adv_stats[team_id].update(data)
    print("gathered advanced stats for team with id", team_id)


with open('teams_adv_stats.json', 'w', encoding='utf-8') as f:
    json.dump(teams_adv_stats, f, ensure_ascii=False, indent=4)
print("advanced stats for teams saved in teams_adv_stats.json")
    '''
