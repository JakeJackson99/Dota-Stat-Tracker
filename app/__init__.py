from flask import Flask
from flask_caching import Cache
from config import Config

URL = 'https://api.opendota.com/api/'
MY_STEAM32_ID = 197033655
HERO_AMOUNT = 4

app = Flask(__name__)
app.config.from_object(Config)
cache = Cache(app)

from app import routes
