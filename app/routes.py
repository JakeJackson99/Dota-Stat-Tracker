import requests
from flask import render_template, request, request, session, jsonify
from app import app
from app.util import format_match_data, static_user_data
from app.static_data import URL


@app.route('/')
def index():
    """Returns the index page."""

    return render_template('index.html')


@app.route('/account', methods=['POST'])
def account():
    """Returns account information for a user via a provided Steam32 ID."""

    steam_id = request.form['steamID']
    session['steam_id'] = steam_id

    data = static_user_data(steam_id)

    return render_template('account.html', profile=data['profile'], wl=data['wl'], heroes=data['heroes'])


@app.route('/recent_matches')
def recent_matches():
    """Loads the user's recent matches"""

    limit = request.args.get('limit')
    offset = request.args.get('offset')
    steam_id = session.get('steam_id')

    matches = requests.get(
        '{}players/{}/matches?limit={}&offset={}&project=heroes'.format(URL, steam_id, limit, offset)).json()

    return jsonify(format_match_data(matches, steam_id))


@app.route('/match/<match_id>')
def match(match_id):
    # match = get_match_details()
    match = "hello"

    return render_template('match.html', match=match)
