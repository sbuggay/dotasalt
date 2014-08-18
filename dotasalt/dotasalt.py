from dotasalt import app

# Flask imports
from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response

# Requests
import requests

# Other
import os, json, datetime, time

# Steam key goes here
STEAM_API_KEY = '1578879989BD74A6D189050250810E86'

# API URLs
MATCH_HISTORY_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/'
MATCH_DETAIL_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
PLAYER_SUMMARIES_URL = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
PLAYER_VANITY_URL = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'

# Static URLs
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

with open(os.path.join(APP_STATIC, 'assets/items.json')) as f:
    item_json = json.load(f)

def get_name_from_account_id(account_id):
    if int(account_id) == 4294967295:
        return 'private'
    steam_id_64 = int(account_id) + 76561197960265728 # convert to 64 bit
    payload = {'key': STEAM_API_KEY, 'steamids': steam_id_64}
    r = requests.get(PLAYER_SUMMARIES_URL, params=payload)
    return r.json()['response']['players'][0]['personaname']

@app.route('/andrea/')
def andrea():
    return render_template('test.html')

### Index

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('theme', 'darkly')

    searchparams = request.args.get('q')

    # If there are search parameters we will get info and pass it on to search.html
    if searchparams:

        payload = {'key': STEAM_API_KEY, 'vanityurl': searchparams}
        r = requests.get(PLAYER_VANITY_URL, params=payload).json()
        
        print(r)

        # If lookup is a success for a player, return their player page
        if r['response']['success'] == 1:
            return redirect(url_for('show_player', account_id = int(r['response']['steamid'])))

        # If nothing can be looked up 1 to 1, display the results
        return render_template('search.html') # With whatever parameters

    # If not just render the index
    return resp


### Matches

# Show last 50 matches

@app.route('/matches/')
def show_matches():
    payload = {'key': STEAM_API_KEY, 'matches_requested': 10}
    r = requests.get(MATCH_HISTORY_URL, params=payload)

    print(r.url)

    r = r.json()

    for match in r['result']['matches']:
        d = datetime.datetime.fromtimestamp(match['start_time']/1000)
        print(d)

    return render_template('matches.html', matches = r['result'])

# Specific Match

@app.route('/matches/<match_id>/')
def show_match(match_id):
    payload = {'key': STEAM_API_KEY, 'match_id': match_id}
    r = requests.get(MATCH_DETAIL_URL, params=payload).json()
    for player in r['result']['players']:
        player['name'] = get_name_from_account_id(player['account_id'])


    print(item_json['1'])
    return render_template('match.html', match = r['result'], items = item_json)

### Players

# Show top players ?

@app.route('/players/')
def show_players():
    return render_template('players.html')

# Show specific player

@app.route('/players/<account_id>/')
def show_player(account_id):
    if int(account_id) < 76561197960265728:
        account_id_64 = int(account_id) + 76561197960265728 # convert to 64 bit
    else:
        account_id_64 = int(account_id)

    payload = {'key': STEAM_API_KEY, 'steamids': account_id_64}
    player = requests.get(PLAYER_SUMMARIES_URL, params=payload).json()
    return render_template('player_overview.html', player = player['response']['players'][0])

# Show specific player's matches

@app.route('/players/<account_id>/matches/')
def show_player_matches(account_id):
    if int(account_id) < 76561197960265728:
        account_id_64 = int(account_id) + 76561197960265728 # convert to 64 bit
    else:
        account_id_64 = int(account_id)

    payload = {'key': STEAM_API_KEY, 'account_id': account_id}
    matches = requests.get(MATCH_HISTORY_URL, params=payload).json()

    payload = {'key': STEAM_API_KEY, 'steamids': account_id_64}
    player = requests.get(PLAYER_SUMMARIES_URL, params=payload).json()

    return render_template('player_matches.html', matches = matches['result']['matches'], player = player['response']['players'][0])

### Heroes

### Items

### Utilities

@app.route('/_switch_theme/<theme_id>')
def switch_theme(theme_id):
    return 'test'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(port=9090)