from dotasalt import app

# Flask imports
from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response

# Requests
import requests

# Other
import os, json

from dotasalt.dotasalt import *


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

    # for match in r['result']['matches']:
    #     # d = datetime.datetime.fromtimestamp(match['start_time']/1000)
    #     # print(d)

    return render_template('matches.html', matches = r['result'])

# Specific Match

@app.route('/matches/<match_id>/')
def show_match(match_id):
    payload = {'key': STEAM_API_KEY, 'match_id': match_id}
    r = requests.get(MATCH_DETAIL_URL, params=payload).json()
    for player in r['result']['players']:
        player['name'] = get_name_from_account_id(player['account_id'])



        salt = 0
        salt = int(player['gold_per_min']) * 0.002
        salt += int(player['xp_per_min']) * 0.002
        salt += int(player['kills']) * 0.5
        salt -= int(player['deaths']) * 0.5
        salt += int(player['assists']) * 0.25
        salt += int(player['tower_damage']) * 0.003
        salt += int(player['hero_damage']) * 0.002
        salt += int(player['hero_healing']) * 0.002
        salt += int(player['tower_damage'] / 1800)
        print(salt)
        player['salt'] = int(100 - salt)


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