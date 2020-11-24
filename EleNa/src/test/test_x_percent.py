import random
import sys

import googlemaps

import json

from EleNa.src.app.data_model.data_model import DataModel
from EleNa.src.app.data_model.shortest_path import Routing

from EleNa.src.config import Config

import matplotlib.pyplot as plt


class Evaluation:

    def __init__(self, x=1.5, city_name='Amherst, MA', n_tests=50):
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
        self.num_tests = n_tests

        self.eval()

    def load_config(self, loc):
        try:
            cfg_file = open(loc, "r")
            self.config = json.load(cfg_file)
        except OSError as err:
            print("Config File Read Error: {0}".format(err))
        else:
            cfg_file.close()

    def eval(self):
        # setup EleNa for evaluation purposes
        routing = Routing(self.data_model)
        nodes = self.graph.nodes()

        # randomly sample nodes from this list of nodes
        from_nodes = random.sample(nodes, self.num_tests)
        to_nodes = random.sample(nodes, self.num_tests)

        max_task_elev = []
        min_task_elev = []
        gt_elev = []
        max_task_dist_per = []
        min_task_dist_per = []

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

            if ground_truth * self.x < log_min['optimal_path_dist']:
                print("Elevation minimization task failed ground-truth verification for:")
                self.dump_evalution_params()
                print("\t From: ", from_node)
                print("\t To: ", to_node)
                # sys.exit("Error in verification. Exiting!")

            if ground_truth * self.x < log_max['optimal_path_dist']:
                print("Elevation maximization task failed ground-truth verification for:")
                self.dump_evalution_params()
                print("\t From: ", from_node)
                print("\t To: ", to_node)
                # sys.exit("Error in verification. Exiting!")

            max_task_elev.append(log_max['optimal_path_gain'])
            min_task_elev.append(log_min['optimal_path_gain'])
            gt_elev.append(log_min['shortest_path_gain'])

            max_task_dist_per.append(log_max['optimal_path_dist'] * 100 / ground_truth)
            min_task_dist_per.append(log_min['optimal_path_dist'] * 100 / ground_truth)

        plt.scatter([i for i in range(self.num_tests)], max_task_elev, color='blue',
                    label='EleNa - elevation from maximization task', s=8)
        plt.scatter([i for i in range(self.num_tests)], min_task_elev, color='green',
                    label='EleNa - elevation from minimization task', s=8)
        plt.scatter([i for i in range(self.num_tests)], gt_elev, color='red', label='Ground truth elevation', s=8)
        plt.vlines([i for i in range(self.num_tests)], ymin=0, ymax=200, color='black', linestyle="--", linewidth=1)
        plt.xticks([])
        plt.ylabel("Elevation (in metres)")
        plt.legend()
        plt.title(label="EleNa - evaluating elevation w.r.t. ground truth")
        plt.tight_layout()
        # plt.show()
        plt.savefig('1.png')
        plt.close()

        plt.scatter([i for i in range(self.num_tests)], max_task_dist_per, color='blue',
                    label='EleNa - maximization task', s=8)
        plt.scatter([i for i in range(self.num_tests)], min_task_dist_per, color='green',
                    label='EleNa - minimization task', s=8)
        plt.vlines([i for i in range(self.num_tests)], ymin=0, ymax=200, color='black', linestyle="--", linewidth=1)
        plt.xticks([])
        plt.ylabel("Percentage w.r.t ground truth")
        plt.legend()
        plt.title(label="EleNa - distance (x%) w.r.t. ground truth")
        plt.tight_layout()
        # plt.show()
        plt.savefig('2.png')
        plt.close()

    def dump_evalution_params(self):
        print(self.city_name, self.num_tests, self.x)


if __name__ == '__main__':
    evaluation = Evaluation()
