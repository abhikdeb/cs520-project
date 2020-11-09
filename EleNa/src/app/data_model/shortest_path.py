import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt

from data_model import DataModel


class Routing:
    def __init__(self):
        data_model = DataModel()
        self.G = data_model.get_graph()
        self.start = None
        self.end = None

    def plot_route(self, route):
        fig, ax = ox.plot_graph_route(self.G, route, route_linewidth=6, node_size=0, bgcolor='k')
        plt.show()

    def get_start_end(self, start_loc=(42.35042, -72.52712), end_loc=(42.40791, -72.53425)):
        self.start = ox.get_nearest_node(self.G, start_loc)
        self.end = ox.get_nearest_node(self.G, end_loc)

    def get_shortest_path(self):
        # ToDo : Videsh
        self.get_start_end()

        # returns a list of nodes
        path = nx.shortest_path(self.G, self.start, self.end, weight='length')
        print('Path == ')
        print(path)
        self.plot_route(path)
