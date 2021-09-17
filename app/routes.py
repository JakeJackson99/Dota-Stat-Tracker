from flask import render_template, request, url_for
import requests

from app import app

URL = 'https://api.opendota.com/api'
MY_STEAM32_ID = 197033655
HERO_AMOUNT = 3


@app.route('/')
def index():
    return render_template('index.html')


# TODO
# - check the account name is a valid Steam ID
#   - handle TypeErrors
# - gather the information I want for the page, e.g. W/L, rank, etc.
# - combine all the data into one object and send to 'account.html'
@app.route('/account', methods=['POST'])
def account():
    steam_id = request.form['steamID']

    user_data = gather_user_data(steam_id)
    return render_template('account.html', user_data=user_data)


def gather_user_data(steam_id):
    user_data = []

    user_data.append(requests.get(
        '{}/players/{}/wl'.format(URL, steam_id)).json())
    user_data.append(requests.get(
        '{}/players/{}'.format(URL, steam_id)).json())
    user_data.append(format_user_hero_data(requests.get(
        '{}/players/{}/heroes'.format(URL, steam_id)).json()))
    return user_data


def format_user_hero_data(hero_data, amount=3):
    hero_list = []
    keys = ["hero_id", "games", "win"]

    for hero in hero_data[:HERO_AMOUNT]:
        dictt = {key: value for key, value in hero.items() if key in keys}
        dictt["name"] = id_to_name(dictt["hero_id"])
        hero_list.append(dictt)

    hero_list = hero_list[:amount]
    return hero_list


def id_to_name(id):
    heroes = requests.get('https://api.opendota.com/api/heroes').json()

    for hero in heroes:
        if id == str(hero["id"]):
            return hero["localized_name"]
