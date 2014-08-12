from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)

@app.route('/_request_matches')
def request_matches():
    payload = {'key': '1578879989BD74A6D189050250810E86'}
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/",params=payload)
    return r.json

@app.route('/')
def index():
    return render_template('index.html')

# routes for players and matches

@app.route('/matches/')
def show_matches():
    payload = {'key': '1578879989BD74A6D189050250810E86'}
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/", params=payload)
    print(r.url)
    return render_template('matches.html', matches = r.json()['result']['matches'])

@app.route('/matches/<match_id>/')
def show_match(match_id):
    payload = {'key': '1578879989BD74A6D189050250810E86', 'match_id': match_id}
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/", params=payload)
    print(r.url)
    return render_template('match.html', match = r.json()['result'])

@app.route('/players/')
def show_players():
    return 'all players'

@app.route('/players/<player_id>/')
def show_player(player_id):
    return player_id

if __name__ == '__main__':
    app.run()