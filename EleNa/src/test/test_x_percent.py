import random
import sys

import googlemaps

import json

from EleNa.src.app.data_model.data_model import DataModel
from EleNa.src.app.data_model.shortest_path import Routing

from EleNa.src.config import Config


class Evaluation:

    def __init__(self, x=50, city_name='Amherst, MA'):
        self.config = {}
        self.key = Config.API_KEY

        # get the API-key and set up the google maps client
        # specifically for direction service
        self.client = googlemaps.Client(self.key)
        self.x = x
        self.city_name = city_name

        # get the data model for evaluation
        self.data_model = DataModel()
        self.graph = self.data_model.get_graph()
        print(self.data_model.get_stats())
        self.num_tests = 100
        self.x = 1.5

        self.test_x_percent()

    def load_config(self, loc):
        try:
            cfg_file = open(loc, "r")
            self.config = json.load(cfg_file)
        except OSError as err:
            print("Config File Read Error: {0}".format(err))
        else:
            cfg_file.close()

    def test_x_percent(self):
        # setup EleNa for evaluation purposes
        routing = Routing(self.data_model)
        nodes = self.graph.nodes()

        # randomly sample nodes from this list of nodes
        from_nodes = random.sample(nodes, self.num_tests)
        to_nodes = random.sample(nodes, self.num_tests)

        for i in range(self.num_tests):
            # get results from EleNa
            # print(from_nodes[i], self.graph.nodes[from_nodes[i]]['y'])
            from_node = (self.graph.nodes[from_nodes[i]]['y'], self.graph.nodes[from_nodes[i]]['x'])
            to_node = (self.graph.nodes[to_nodes[i]]['y'], self.graph.nodes[to_nodes[i]]['x'])
            routing.set_start_end(from_node, to_node)
            routing.set_max_deviation(self.x)
            best_path_min, log_min = routing.get_shortest_path("minimize")
            best_path_max, log_max = routing.get_shortest_path("maximize")

            # get distance from Google MAps - Direction Service
            routes = self.client.directions(from_node, to_node, mode="walking")
            ground_truth = routes[0]["legs"][0]["distance"]["value"]
            print(json.dumps(routes, indent=4))

            if ground_truth * self.x < log_min['best_path_dist_min']:
                print("Elevation minimization task failed ground-truth verification for:")
                self.dump_evalution_params()
                print("\t From: ", from_node)
                print("\t To: ", to_node)
                sys.exit("Error in verification. Exiting!")

            if ground_truth * self.x < log_max['best_path_dist_max']:
                print("Elevation maximization task failed ground-truth verification for:")
                self.dump_evalution_params()
                print("\t From: ", from_node)
                print("\t To: ", to_node)
                sys.exit("Error in verification. Exiting!")

    def dump_evalution_params(self):
        print(self.city_name, self.num_tests, self.x)


if __name__ == '__main__':
    evaluation = Evaluation()
