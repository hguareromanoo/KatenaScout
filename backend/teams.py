from services.data_service import find_club_by_id,  get_player_database, get_team_names



db = get_player_database()
player = db['Lautaro Javier Martínez']

team_id = player.get('currentTeamId')

team = find_club_by_id(team_id)
print(team)

teams = get_team_names()

team_1 = teams.get(team_id)
print(team_1)