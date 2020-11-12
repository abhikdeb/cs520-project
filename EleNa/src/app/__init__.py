from flask import Flask

app = Flask(__name__)

from EleNa.src.app import routes
