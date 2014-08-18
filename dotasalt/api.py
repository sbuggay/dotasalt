from flask import Flask, request

from dotasalt import app



@app.route('/api/match/')
def match_api():
	args = request.args.get('match_id')
	return args