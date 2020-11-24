import os
import json
os.chdir("./EleNa/src")

class Config(object):
    cfg = {}
    try:
        cfg_file = open('./app/config.json', "r")
        cfg = json.load(cfg_file)
    except OSError as err:
        print("Config File Read Error: {0}".format(err))
    else:
        cfg_file.close()

    SECRET_KEY = os.environ.get('SECRET_KEY') or cfg.get('app')['security_key']
    API_KEY = cfg.get('google_api')['api_key']
