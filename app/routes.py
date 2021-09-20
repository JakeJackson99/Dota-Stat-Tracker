from flask import render_template, request, url_for
import requests

from app import app, cache

URL = 'https://api.opendota.com/api'
MY_STEAM32_ID = 197033655
HERO_AMOUNT = 4


# TODO
# account()
# - check the account name is a valid Steam ID
#   - handle TypeErrors


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/account', methods=['POST'])
def account():
    steam_id = request.form['steamID']

    data = gather_user_data(steam_id)

    return render_template('account.html', profile=data['profile'], wl=data['wl'], heroes=data['heroes'])


@cache.cached(timeout=0, key_prefix='user_data')
def gather_user_data(steam_id):
    profile = requests.get('{}/players/{}'.format(URL, steam_id)).json()
    wl = requests.get('{}/players/{}/wl'.format(URL, steam_id)).json()
    heroes = format_user_hero_data(requests.get(
        '{}/players/{}/heroes'.format(URL, steam_id)).json(), HERO_AMOUNT)

    return {'profile': profile, 'wl': wl, 'heroes': heroes}


def format_user_hero_data(hero_data, amount=3):
    hero_list = []
    keys = ["hero_id", "games", "win"]

    for hero in hero_data[:HERO_AMOUNT]:
        dictt = {key: value for key, value in hero.items() if key in keys}
        dictt["name"] = id_to_name(dictt["hero_id"])
        hero_list.append(dictt)

    return hero_list


def id_to_name(id):
    heroes = requests.get('https://api.opendota.com/api/heroes').json()

    for hero in heroes:
        if id == str(hero["id"]):
            return hero["localized_name"]
