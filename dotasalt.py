from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)

STEAM_API_KEY = '1578879989BD74A6D189050250810E86'

MATCH_HISTORY_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/'
MATCH_DETAIL_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
PLAYER_SUMMARIES_URL = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'

@app.route('/')
def index():
    return render_template('index.html')

# Matches

@app.route('/matches/')
def show_matches():
    payload = {'key': STEAM_API_KEY, 'min_players': 10}
    r = requests.get(MATCH_HISTORY_URL, params=payload)
    print(r.url)
    return render_template('matches.html', matches = r.json()['result']['matches'])

@app.route('/matches/<match_id>/')
def show_match(match_id):
    payload = {'key': STEAM_API_KEY, 'match_id': match_id}
    r = requests.get(MATCH_DETAIL_URL, params=payload)
    print(r.url)
    return render_template('match.html', match = r.json()['result'])

# Players

@app.route('/players/')
def show_players():
    return 'all players'

@app.route('/players/<player_id>/')
def show_player(player_id):
    steam_id_64 = int(player_id) + 76561197960265728
    payload = {'key': STEAM_API_KEY, 'steamids': steam_id_64}
    r = requests.get(PLAYER_SUMMARIES_URL, params=payload)
    print(r.url)
    return render_template('player.html', player = r.json()['response']['players'][0])

@app.route('/players/<player_id>/matches/')
def show_player_matches(player_id):
    payload = {'key': STEAM_API_KEY, 'account_id': player_id}
    r = requests.get(MATCH_HISTORY_URL, params=payload)
    print(r.url)
    return render_template('player_matches.html', matches = r.json()['result']['matches'])

# Heroes

# Items

# Utilities

@app.route('/_get_name_from_account_id/', methods=['GET'])
def get_name_from_account_id(account_id):
    print("at least attempted")
    account_id = {"account_id": request.args.get('account_id')}
    return jsonify(account_id)


if __name__ == '__main__':
    app.run(port=9090)