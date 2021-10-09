import requests
from app import cache, URL, HERO_AMOUNT

# TODO
# - create a def to fetch the list of heroes for the user and cache it;
#   - this is to be used in static_user_data, id_to_name & in recent_matches.
# - check that ['tracked_until'] is not null when gathring user data,
#   such as in static_user_data.


@cache.cached(timeout=0, key_prefix='user_hero_list')
def user_hero_list(steam_id):
    """Returns the user's hero data in a list of dicts

    steam_id -- the ID for the user
    """
    return requests.get('{}players/{}/heroes'.format(URL, steam_id)).json()


@cache.cached(timeout=0, key_prefix='hero_list')
def hero_list():
    """Returns all static hero data in a list of dicts"""
    return requests.get('https://api.opendota.com/api/heroes').json()


@cache.cached(timeout=0, key_prefix='static_user_data')
def static_user_data(steam_id):
    """Collate the user's account information into a nested dict.

    steam_id -- the ID for the user
    """
    profile = requests.get('{}players/{}'.format(URL, steam_id)).json()

    wl = requests.get('{}players/{}/wl'.format(URL, steam_id)).json()

    heroes = top_heroes(user_hero_list(steam_id), HERO_AMOUNT)

    return {'profile': profile, 'wl': wl, 'heroes': heroes}


def top_heroes(hero_data, amount=3):
    """Returns the top 'x' heroes in a list of dicts + their ingame name.

    hero_data -- user's record of games with each hero
    amount -- the top 'x' amount of heroes to return, i.e. top 3
    """
    hero_list = []
    keys = ["hero_id", "games", "win"]

    for hero in hero_data[:amount]:
        dictt = {key: value for key, value in hero.items() if key in keys}
        dictt["name"] = id_to_name(dictt["hero_id"])
        hero_list.append(dictt)

    return hero_list


def id_to_name(id):
    """Finds the ingame name of a hero given an ID

    id -- id of ingame hero
    """
    heroes = hero_list()

    for hero in heroes:
        if id == str(hero["id"]):
            return hero["localized_name"]


def format_match_data(matches, steam_id):
    """
    
    matches --  
    """  
    list = []

    for match in matches:

        dict = {'match_id': match['match_id'], 'duration': match['duration']}

        heroes = match['heroes']
        for hero in heroes.values():
            if hero['account_id'] == steam_id:
                dict['account_id'] = hero['account_id']
                dict['hero_name'] = id_to_name(str(hero['hero_id']))
                list.append(dict)
    
    return list
