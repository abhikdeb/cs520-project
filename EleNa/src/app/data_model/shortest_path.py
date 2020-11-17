import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import operator
import numpy as np
from queue import PriorityQueue
from data_model import DataModel
from scipy.optimize import minimize, minimize_scalar, differential_evolution
import time
import copy


def find_path_edges_min(graph, path, min_weight='grade'):
    path_length = 0
    path_ele_gain = 0
    path_edge_keys = []
    for i in range(len(path) - 1):
        edges = graph[path[i]][path[i + 1]]
        min_weight_edge = min(edges.keys(), key=lambda k: edges[k][min_weight] * edges[k]['length'])
        path_length += edges[min_weight_edge]['length']
        path_ele_gain += max(0, edges[min_weight_edge]['grade'] * edges[min_weight_edge]['length'])
        path_edge_keys.append(min_weight_edge)
    return (path_length, path_ele_gain, path_edge_keys)


def find_path_edges(graph, path, min_weight='grade'):
    path_length = 0
    path_ele_gain = 0
    path_edge_keys = []
    for i in range(len(path) - 1):
        edges = graph[path[i]][path[i + 1]]
        min_weight_edge = min(edges.keys(), key=lambda k: edges[k][min_weight])
        path_length += edges[min_weight_edge]['length']
        path_ele_gain += edges[min_weight_edge]['grade'] * edges[min_weight_edge]['length']
        path_edge_keys.append(min_weight_edge)
    return (path_length, path_ele_gain, path_edge_keys)


## add for max vals
def find_path_edges_max(graph, path, min_weight='grade'):
    path_length = 0
    path_ele_gain = 0
    path_edge_keys = []
    for i in range(len(path) - 1):
        edges = graph[path[i]][path[i + 1]]
        min_weight_edge = max(edges.keys(), key=lambda k: edges[k][min_weight] * edges[k]['length'])
        path_length += edges[min_weight_edge]['length']
        path_ele_gain += max(0, edges[min_weight_edge]['grade'] * edges[min_weight_edge]['length'])
        path_edge_keys.append(min_weight_edge)
    return (path_length, path_ele_gain, path_edge_keys)


class Routing:
    def __init__(self, data_model):
        self.data_model = data_model
        self.G = self.data_model.get_graph()
        self.start = None
        self.end = None
        self.paths = None
        self.paths_with_stats = None

        # hardcoded: to be removed later
        start_loc = (42.432121, -72.4916)
        end_loc = (42.31338, -72.4672)  # (42.3857, -72.5298)
        self.set_start_end(start_loc, end_loc)

    def plot_route(self, route):
        fig, ax = ox.plot_graph_route(self.G, route, route_linewidth=6, node_size=0, bgcolor='k')
        plt.show()

    def get_node(self, loc):
        return ox.get_nearest_node(self.G, loc)

    def set_start_end(self, start_loc, end_loc):
        self.start = self.get_node(start_loc)
        self.end = self.get_node(end_loc)

    def get_shortest_path_length(self):
        '''
            arguments: start and end locations
            returns: the shortest path length between the start and the end nodes
            Note: it can also be modified to return the path as list of nodes using backtrace()
            credits: https://github.com/blkrt/dijkstra-python
        '''

        def backtrace(previous, start, end):
            '''
                returns the shortest path between start and end as a list of nodes
            '''
            node = end
            path = []
            while node != start:
                path.append(node)
                node = previous[node]
            path.append(node)
            path.reverse()
            return path

        def get_shortest_edge_length(node1, node2):
            '''
                returns the length of the shortest edge between a pair of neighboring nodes
            '''
            edges = self.G.get_edge_data(node1, node2)
            if len(edges.keys()) == 1:
                return edges[0]['length']

            edge_to_len = {}
            for key in edges.keys():
                edge_to_len[key] = edges[key]['length']
            min_key = min(edge_to_len, key=edge_to_len.get)
            return edges[min_key]['length']

        previous = {}
        distance = {v: np.inf for v in list(self.G.nodes())}
        visited = set()
        pq = PriorityQueue()
        distance[self.start] = 0
        pq.put((distance[self.start], self.start))

        while pq.qsize():
            dist, node = pq.get()
            visited.add(node)
            # print('Visiting {}'.format(node))

            for nbr in dict(self.G.adjacency()).get(node):
                edge_length = get_shortest_edge_length(node, nbr)
                # print(edge_length)
                path_length = distance[node] + edge_length
                if path_length < distance[nbr]:
                    distance[nbr] = path_length
                    previous[nbr] = node
                    if nbr not in visited:
                        visited.add(nbr)
                        pq.put((distance[nbr], nbr))
                    else:
                        _, _ = pq.get((distance[nbr], nbr))
                        pq.put((distance[nbr], nbr))

        shortest_path = backtrace(previous, self.start, self.end)  # shortest path with the list of intermediate nodes
        # print(shortest_path)
        return distance[self.end]

    def get_shortest_path(self, mode):
        # call when entered from UI
        # self.set_start_end()

        # Baseline
        if mode == "baseline":
            path = ox.distance.shortest_path(self.G, self.start, self.end, weight='length')
            dist, min_dist_grade, min_dist_keys = find_path_edges_min(self.G, path, min_weight='length')
            logs = {}
            logs['dist'] = dist
            logs['min_dist_grade'] = min_dist_grade
            return path, logs
        elif mode == 'minimize':
            return self.minimize_elevation_gain_ML(1.9)
        elif mode == 'maximize':
            return self.maximize_elevation_gain_ML(1.9)

    # exhaustive
    # return self.minimize_elevation_gain(1.5)

    # algo2
    # graph_proj = ox.project_graph(self.G)
    # shortest_path_dist = nx.shortest_path_length(self.G, self.start, self.end, 'length')

    # return self.dfs_get_all_paths(graph_proj, self.start, self.end, shortest_path_dist * 1.2)

    def dfs_get_all_paths(self, graph, start, goal, max_length):
        paths = []

        def dfs(current, le, current_path, visited):
            if current == goal:
                if le > max_length:
                    return
                else:
                    current_path.append(current)
                    paths.append(current_path)
                    # print ("This path length:",length)
                    # print ("path found")
                    return
            if le > max_length:
                return
            for u, next_node, data in graph.edges(current, data=True):
                if next_node in visited:
                    continue
                dfs(next_node, le + abs(self.get_cost(graph, current, next_node)), current_path + [current],
                    visited + [next_node])
            return

        dfs(start, 0, [], [])
        print ("Total paths:", len(paths))

        min_val = sys.maxsize
        max_val = -1 * sys.maxsize
        min_path, max_path = [], []
        for path in paths:
            elevation_data = self.get_elevation_of_path(graph, path)
            if min_val != min(elevation_data, min_val):
                min_val = elevation_data
                min_path = path
            if max_val != max(elevation_data, max_val):
                max_val = elevation_data
                max_path = path
        return min_path, max_path

    def get_cost(self, graph_projection, a, b):
        return graph_projection.edges[a, b, 0]['length']

    def minimize_elevation_gain_ML(self, percent_shortest_path):
        # Enforce x% of shortest path 1.0 or larger
        if percent_shortest_path < 1.0:
            raise Exception("Cannot find a path shorter than the shortest path.")

        # Find shortest distance path
        min_dist, min_dist_path = nx.single_source_dijkstra(self.G, self.start, self.end, weight='length')
        _, min_dist_grade, min_dist_keys = find_path_edges_min(self.G, min_dist_path, min_weight='length')
        # Set maximum distance willing to travel
        max_dist = min_dist * percent_shortest_path

        # Find total distance and grade gain of the edges for normalization
        total_dist = 0
        total_grade = 0
        for u, v, data in self.G.edges(data=True):
            total_dist += data['length']
            total_grade += data['grade']

        # Dictionary for all paths found within max distance
        paths_found = [{'path': min_dist_path, 'length': min_dist,
                        'grade': min_dist_grade, 'keys': min_dist_keys}]

        G_processed = copy.deepcopy(self.G)

        def minimize_alpha(alpha):

            for u, v, k, data in self.G.edges(keys=True, data=True):
                G_processed.add_edge(u, v, key=k, grade=
                max(0, alpha * data['grade'] * data['length']) +
                (1 - alpha) * data['length'])

            # Find shortest path for new grade
            path = ox.distance.shortest_path(G_processed, self.start, self.end, weight='grade')
            path_length, path_grade, path_keys = find_path_edges_min(self.G, path)

            # If the path found has a shorter distance than the max,
            if path_length <= max_dist:
                # Add it to the list of paths to pick from
                print("path_length", path_length, path_grade)
                paths_found.append({'path': path, 'length': path_length,
                                    'grade': path_grade, 'keys': path_keys})

            print("alpha:", alpha, "loss:", (max_dist - path_length) ** 2)
            return (max_dist - path_length) ** 2

        s = time.time()
        a = minimize_scalar(minimize_alpha, method="Bounded", bounds=(0, 1))
        # a = minimize(minimize_alpha, 0.5, bounds = [(0,1)])
        # a = differential_evolution(minimize_alpha, bounds = [(0, 1)])
        print("Time taken", time.time() - s, a)

        # Return the lowest grade gain within max distance
        logs = {}
        # best_path_max = max(paths_found, key=lambda d: d['grade'])
        # logs['best_path_dist_max'] = best_path_max['length']
        # logs['best_path_gain_max'] = best_path_max['grade']
        # best_path_max = best_path_max['path']

        best_path_min = min(paths_found, key=lambda d: d['grade'])
        logs['best_path_dist_min'] = best_path_min['length']
        logs['best_path_gain_min'] = best_path_min['grade']
        best_path_min = best_path_min['path']

        logs['shortest_path_dist'] = min_dist
        logs['min_dist_grade'] = min_dist_grade

        return best_path_min, logs

    def maximize_elevation_gain_ML(self, percent_shortest_path):
        # Enforce x% of shortest path 1.0 or larger
        if percent_shortest_path < 1.0:
            raise Exception("Cannot find a path shorter than the shortest path.")

        # Find shortest distance path
        min_dist, min_dist_path = nx.single_source_dijkstra(self.G, self.start, self.end, weight='length')
        _, min_dist_grade, min_dist_keys = find_path_edges_min(self.G, min_dist_path, min_weight='length')
        # Set maximum distance willing to travel
        max_dist = min_dist * percent_shortest_path

        # Find total distance and grade gain of the edges for normalization
        total_dist = 0
        total_grade = 0
        for u, v, data in self.G.edges(data=True):
            total_dist += data['length']
            total_grade += data['grade']

        # Dictionary for all paths found within max distance
        paths_found = [{'path': min_dist_path, 'length': min_dist,
                        'grade': min_dist_grade, 'keys': min_dist_keys}]

        G_processed = copy.deepcopy(self.G)

        def minimize_alpha(alpha):
            for u, v, k, data in self.G.edges(keys=True, data=True):
                G_processed.add_edge(u, v, key=k, grade=
                max(0, (1 - alpha) / (1e-6 + data['grade'])) + (alpha) / (1e-6 + data['length']))

            # Find shortest path for new grade
            path = ox.distance.shortest_path(G_processed, self.start, self.end, weight='grade')
            path_length, path_grade, path_keys = find_path_edges_max(self.G, path)

            # If the path found has a shorter distance than the max,
            if path_length <= max_dist:
                # Add it to the list of paths to pick from
                print("path_length", path_length, path_grade)

                paths_found.append({'path': path, 'length': path_length,
                                    'grade': path_grade, 'keys': path_keys})
            print("alpha:", alpha, "loss:", (max_dist - path_length) ** 2)
            return (max_dist - path_length) ** 2

        s = time.time()
        a = minimize_scalar(minimize_alpha, method="Bounded", bounds=(0, 1))
        # a = minimize(minimize_alpha, 0.5, method = "Nelder-Mead")
        # a = differential_evolution(minimize_alpha, bounds = [(0, 1)])
        print("Time taken", time.time() - s, a)

        # Return the lowest grade gain within max distance
        logs = {}
        best_path_max = max(paths_found, key=lambda d: d['grade'])
        logs['best_path_dist_max'] = best_path_max['length']
        logs['best_path_gain_max'] = best_path_max['grade']
        best_path_max = best_path_max['path']

        # best_path_min = min(paths_found, key=lambda d: d['grade'])
        # logs['best_path_dist_min'] = best_path_min['length']
        # logs['best_path_gain_min'] = best_path_min['grade']
        # best_path_min = best_path_min['path']

        logs['shortest_path_dist'] = min_dist
        logs['min_dist_grade'] = min_dist_grade

        return best_path_max, logs

    def get_elevation_of_path(self, graph, path):
        elevation_cost = 0
        if not path:
            return 0
        for i in range(len(path) - 1):
            nodeA = path[i]
            nodeB = path[i + 1]

            # method 1: using node_info
            elevation_data = graph.nodes[nodeB]['elevation'] - graph.nodes[nodeA]['elevation']

            # method 2: using edge_info
            # edge_data = self.G.edges[nodeA, nodeB, 0]
            # elevation_data = edge_data['grade'] * edge_data['length']

            if elevation_data > 0:
                elevation_cost += elevation_data
        return elevation_cost

    def get_length_of_path(self, graph, path):
        length_cost = 0
        if not path:
            return 0
        for i in range(len(path) - 1):
            nodeA = path[i]
            nodeB = path[i + 1]

            edge_data = graph.edges[nodeA, nodeB, 0]
            length_cost += edge_data['length']

        return length_cost

    def get_all_paths(self, graph, source, target, allowed_hops):
        # [[length, elevation_gain, [path]]]
        graph_proj = ox.project_graph(graph)
        self.paths = list(nx.all_simple_paths(graph_proj, source, target, allowed_hops))
        min_val = sys.maxsize
        max_val = -1 * sys.maxsize
        min_path, max_path = [], []
        for path in self.paths:
            print("Path is", path)
            elevation_data = self.get_elevation_of_path(graph_proj, path)
            length_data = self.get_length_of_path(graph_proj, path)
            if min_val != min(elevation_data, min_val) and length_data < can_travel:
                min_val = elevation_data
                min_path = path
            if max_val != max(elevation_data, max_val) and length_data < can_travel:
                max_val = elevation_data
                max_path = path
        return min_path, max_path

    # self.paths_with_stats = []

    # for path in self.paths:
    #     self.paths_with_stats.append([self.get_length_of_path(path), self.get_elevation_of_path(path), path])

    def minimize_elevation_gain(self, percent_shortest_path):

        # TODO: Replace with videsh algo (replace shortest path length)
        shortest_path = nx.shortest_path(self.G, self.start, self.end, weight='length')
        shortest_path_dist = nx.shortest_path_length(self.G, self.start, self.end, 'length')
        cutoff_dist = shortest_path_dist * percent_shortest_path
        print("cutoff", cutoff_dist, "shortest", shortest_path_dist)

        self.get_all_paths(self.G, self.start, self.end, len(shortest_path) + 1)

    # return min(self.paths_with_stats, key=lambda x: x[1])

    def maximize_elevation_gain(self, percent_shortest_path):

        # TODO: Replace with videsh algo (replace shortest path length)

        shortest_path_len = nx.shortest_path_length(self.G, self.start, self.end, 'length')
        cutoff_dist = shortest_path_len * percent_shortest_path

        self.get_all_paths(self.G, self.start, self.end, cutoff_dist)
        return max(self.paths_with_stats, key=lambda x: x[1])
