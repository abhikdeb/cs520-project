from flask import Flask
from EleNa.src.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from EleNa.src.app import routes
