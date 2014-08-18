# DotA 2 API Scraper

import json
import requests

STEAM_API_KEY = '1578879989BD74A6D189050250810E86'

MATCH_HISTORY_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/'
MATCH_DETAIL_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
PLAYER_SUMMARIES_URL = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'

payload = {'key': STEAM_API_KEY, 'min_players': 10}
r = requests.get(MATCH_HISTORY_URL, params=payload)

items = r.json()['result']['matches'][0]
columns = list(items.keys())
print(columns)

