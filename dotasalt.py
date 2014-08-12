from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)

key = '1578879989BD74A6D189050250810E86'

@app.route('/')
def index():
    return render_template('index.html')

# Matches

@app.route('/matches/')
def show_matches():
    payload = {'key': key}
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/", params=payload)
    print(r.url)
    return render_template('matches.html', matches = r.json()['result']['matches'])

@app.route('/matches/<match_id>/')
def show_match(match_id):
    payload = {'key': key, 'match_id': match_id}
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/", params=payload)
    print(r.url)
    return render_template('match.html', match = r.json()['result'])

# Players

@app.route('/players/')
def show_players():
    return 'all players'

@app.route('/players/<player_id>/')
def show_player(player_id):
    payload = {'key': key, 'player_id': player_id}
    r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/", params=payload)
    print(r.url)
    return render_template('player.html', player = r.json()['result'])

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