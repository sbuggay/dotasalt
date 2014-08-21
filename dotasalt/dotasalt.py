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
