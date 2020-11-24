import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, differential_evolution
import time
import copy
import googlemaps

from EleNa.src.config import Config


def find_path_edges(graph, path, weight, mode):
    """
    used to alter the path edges in case multiple edges exist between two neigbors
    weight: length or grade or elevation(=length*grade)
    mode: min or max
    """
    path_length = 0
    path_ele_gain = 0
    path_edge_keys = []
    for i in range(len(path) - 1):
        edges = graph[path[i]][path[i + 1]]
        if mode == 'min':
            if weight == 'elevation':
                weight_edge = min(edges.keys(), key=lambda k: edges[k]['grade'] * edges[k]['length'])

            # for alpha-parameterized cost
            elif weight == 'cost':
                weight_edge = min(edges.keys(), key=lambda k: edges[k]['grade'])
            else:
                weight_edge = min(edges.keys(), key=lambda k: edges[k][weight])

        elif mode == 'max':
            if weight == 'elevation':
                weight_edge = max(edges.keys(), key=lambda k: edges[k]['grade'] * edges[k]['length'])
            # for alpha-parameterized cost
            elif weight == 'cost':
                weight_edge = max(edges.keys(), key=lambda k: edges[k]['grade'])
            else:
                weight_edge = max(edges.keys(), key=lambda k: edges[k][weight])

        path_length += edges[weight_edge]['length']
        path_ele_gain += max(0, edges[weight_edge]['grade'] * edges[weight_edge]['length'])
        path_edge_keys.append(weight_edge)

    return path_length, path_ele_gain, path_edge_keys


class Routing:
    """
    Routing part of Tech Stack to find shortest path using elevation data
    Dijkstra and optimization based solution to find optimal solution (based on distance & elevation gain)
    """

    def __init__(self, data_model):
        self.data_model = data_model
        self.G = self.data_model.get_graph()
        self.start = None
        self.end = None
        self.x = 1.9
        self.baseline_dict = {}
        self.paths = None
        self.paths_with_stats = None

        start_loc = (42.432121, -72.4916)
        end_loc = (42.31338, -72.4672)
        self.set_start_end(start_loc, end_loc)

        self.gmap_client = googlemaps.Client(Config.API_KEY)

    def plot_route(self, route):
        """
        Plot the graph with given route using OSMNX plot feature
        Args:
            route: plot the given route

        Returns: None

        """
        fig, ax = ox.plot_graph_route(self.G, route, route_linewidth=6, node_size=0, bgcolor='k')
        plt.show()

    def get_node(self, loc):
        """
        Args:
            loc: coordinates to get the node

        Returns: Nearest Node from the location specified by 'loc'

        """
        return ox.get_nearest_node(self.G, loc)

    def set_start_end(self, start_loc, end_loc):
        """
        Get start, end nodes as per start, end coordinates
        Args:
            start_loc: starting coordinates (latitude and longitude)
            end_loc: ending coordinates (latitude and longitude)

        Returns: None

        """
        self.start = self.get_node(start_loc)
        self.end = self.get_node(end_loc)

    def set_max_deviation(self, x):
        """
        Set maximum constraints on distance to travel
        Args:
            x: x% constraint on the shortest path length

        Returns: None

        """
        self.x = x

    def get_gmap_ground_truth(self, source, destination):
        """
        Get ground truth (shortest path) from Google Maps API with given source and destination
        Args:
            source:  starting coordinates (latitude and longitude)
            destination: ending coordinates (latitude and longitude)

        Returns: Shortest Path based on Google Maps API

        """
        routes = self.gmap_client.directions(source, destination, mode="walking")
        steps = routes[0]["legs"][0]["steps"]

        sampled_waypoints = []
        skip = 1

        if len(steps) > 20:
            skip = len(steps) // 20 + 1

        i = 0
        while i < len(steps) - 1:
            sampled_waypoints.append({
                "Lat": steps[i]["start_location"]["lat"],
                "Long": steps[i]["start_location"]["lng"],
            })
            i += skip

        sampled_waypoints.append({
            "Lat": steps[len(steps) - 1]["end_location"]["lat"],
            "Long": steps[len(steps) - 1]["end_location"]["lng"],
        })

        return sampled_waypoints

    def get_shortest_path(self, mode):
        """
        Find optimal path based on three modes - 'baseline' , 'minimize', 'maximize'
        Args:
            mode: mode in which to find optimal path
            - baseline : find shortest path using networkx's inbuilt algorithm using only 'length' and no 'elevation'
            - minimize : find shortest path which minimizes elevation gain and stays within x% of baseline shortest path length
            - maximize : find shortest path which maximizes elevation gain and stays within x% of baseline shortest path length
        Returns:
            Optimal path as a list of nodes
        """

        path = nx.shortest_path(self.G, self.start, self.end, weight='length')
        path_length, path_ele_gain, path_edge_keys = find_path_edges(self.G, path, 'length', 'min')
        self.baseline_dict = {'path': path, 'length': path_length, 'ele_gain': path_ele_gain,
                              'edge_keys': path_edge_keys}

        if mode == 'baseline':
            logs = {}
            logs['distance'] = path_length
            logs['elevation_gain'] = path_ele_gain
            return path, logs

        elif mode == 'minimize':
            return self.optimize_elevation_gain(self.x, self.baseline_dict, mode)

        elif mode == 'maximize':
            return self.optimize_elevation_gain(self.x, self.baseline_dict, mode)

    def optimize_elevation_gain(self, x, baseline_dict, mode):
        """
			x: (> 1.0) how large can the path length be, compared to the shortest existing path
			baseline_dict: {'path': min_dist_path, 'length': min_dist, 'ele_gain': min_ele_gain, 'edge_keys': min_dist_keys}
			mode: 'minimize' or 'maximize'
		"""

        def tune_alpha(alpha):
            """
            Tune alpha as a constrained optimization problem, we want path_dist to be as close to max_dist
            """
            for u, v, k, data in self.G.edges(keys=True, data=True):
                # alpha-parameterized cost added as grade to G_copy
                if mode == 'minimize':
                    cost = max(0, alpha * data['grade'] * data['length']) + (1 - alpha) * data['length']
                elif mode == 'maximize':
                    cost = max(0, (1 - alpha) / (1e-6 + data['grade'])) + alpha / (1e-6 + data['length'])

                G_copy.add_edge(u, v, key=k, grade=cost)

            # Find shortest path with respect to new grades
            path = nx.shortest_path(G_copy, self.start, self.end, weight='grade')
            if mode == 'minimize':
                path_length, path_ele_gain, path_edge_keys = find_path_edges(self.G, path, 'cost', 'min')
            if mode == 'maximize':
                path_length, path_ele_gain, path_edge_keys = find_path_edges(self.G, path, 'cost', 'max')

            # If the path found has a shorter distance than the max,
            if path_length <= max_dist:
                # Add it to the list of paths to pick from
                # print("path_length: {:.4f}, elevation_gain: {:.4f}".format(path_length, path_ele_gain))
                paths_found.append({'path': path, 'length': path_length,
                                    'ele_gain': path_ele_gain, 'edge_keys': path_edge_keys})

            objective = (max_dist - path_length) ** 2
            # print("alpha:", alpha, "objective:", objective)

            return objective

        # Enforce x% of shortest path 1.0 or larger
        if x < 1.0:
            raise Exception("Cannot find a path shorter than the shortest path.")

        # Set maximum distance willing to travel
        max_dist = baseline_dict['length'] * x

        # Dictionary for all paths found within max distance
        paths_found = [baseline_dict]
        optimal_path_dict = {}

        G_copy = copy.deepcopy(self.G)
        s = time.time()
        if mode == 'minimize':
            opt_message = minimize_scalar(tune_alpha, method="Bounded", bounds=(0, 1))
            optimal_path_dict = min(paths_found, key=lambda d: d['ele_gain'])

        elif mode == 'maximize':
            opt_message = minimize_scalar(tune_alpha, method="Bounded", bounds=(0, 1))
            optimal_path_dict = max(paths_found, key=lambda d: d['ele_gain'])

        print("time taken: ", time.time() - s)

        # Return the lowest elevation gain within max distance
        logs = {}

        logs['optimal_path_dist'] = optimal_path_dict['length']
        logs['optimal_path_gain'] = optimal_path_dict['ele_gain']
        optimal_path = optimal_path_dict['path']

        logs['shortest_path_dist'] = baseline_dict['length']
        logs['shortest_path_gain'] = baseline_dict['ele_gain']

        return optimal_path, logs
