import googlemaps

import json

from EleNa.src.app.data_model.data_model import DataModel

import sys

sys.path.append('../../')


class Evaluation:

    def __init__(self, x=50, city_name='Amherst, MA'):
        self.config = {}
        self.load_config('../app/config.json')
        self.key = self.config['google_api']['api_key']
        print(self.key)
        self.client = googlemaps.Client(self.key)
        self.x = x
        self.city_name = city_name
        self.test_x_percent()
        # self.data_model = DataModel()
        # self.graph = self.data_model.get_graph()

    def load_config(self, loc):
        try:
            cfg_file = open(loc, "r")
            self.config = json.load(cfg_file)
        except OSError as err:
            print("Config File Read Error: {0}".format(err))
        else:
            cfg_file.close()

    def test_x_percent(self):
        start_loc = (42.349004, -72.528118)
        end_loc = (42.377684, -72.520563)
        routes = self.client.directions(start_loc, end_loc, mode="walking")
        steps = routes[0]["legs"][0]["steps"]
        distance = 0.0
        for step in steps:
            distance += step["distance"]["value"]

        print(json.dumps(routes, indent=4))
        print("Total distance: ", distance)


if __name__ == '__main__':
    evaluation = Evaluation()
