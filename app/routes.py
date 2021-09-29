from flask import render_template, request, url_for, request
from app import app, MY_STEAM32_ID
from app.util import gather_user_data

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/account', methods=['POST'])
def account():
    steam_id = request.form['steamID']

    data = gather_user_data(steam_id)

    return render_template('account.html', profile=data['profile'], wl=data['wl'], heroes=data['heroes'])


@app.route('/recent_matches')
def recent_matches():
    pass

@app.route('/get_steam_id')
def get_steam_id():
    value = MY_STEAM32_ID
    return {'steam_id': str(value)}



