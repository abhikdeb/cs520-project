from flask import Flask
from EleNa.src.config import Config
from flask_googlemaps import GoogleMaps


app = Flask(__name__)
app.config.from_object(Config)

GoogleMaps(app, key=Config.API_KEY)


from EleNa.src.app import routes
