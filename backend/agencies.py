import json
import os

with open('backend/database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

agency_list = []
for player_name, player_data in data.items():
    # Ensure 'contract' exists and is not None
    contract = player_data.get('contract')
    if not contract or not contract.get('agencies'):
        continue
    for agencia in contract['agencies']:
        if agencia not in agency_list:
            agency_list.append(agencia)

with open('agencies.json', 'w', encoding='utf-8') as f:
    json.dump(agency_list, f, indent=2)

print("Agency list saved to 'agencies.json'")