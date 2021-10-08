import requests
from flask import render_template, request, url_for, request, session
from app import app, URL
from app.util import static_user_data, match_data

LIMIT = 10


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

    # send back LIMIT
    offset = request.args.get('offset')
    steam_id = session.get('steam_id')

    matches = requests.get(
        '{}players/{}/matches?limit={}&offset={}&project=heroes'.format(URL, steam_id, LIMIT, offset)).json()

    data = match_data(matches)

    print(matches[0])

    return {'matches': matches}


@app.route('/get_steam_id')
def get_steam_id():
    """Returns the user's Steam32 ID from the session cookie."""

    return {'steam_id': session.get('steam_id')}
