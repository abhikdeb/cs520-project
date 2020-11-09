import os
import osmnx as ox
import pickle5 as pickle
import glob


class DataModel:
    # paths to pickles
    folder_name = 'graphs'
    loaded_graphs = {}

    def __init__(self, city_name='Amherst, MA'):
        # Todo: Abhik S. (loading from dump -- persistent storage)

        if city_name in self.loaded_graphs:
            self.load_graph_from_path(self.loaded_graphs[city_name])
            print('Loaded graph for {} from dump'.format(city_name))

        else:
            pickle_path = self.folder_name + '/' + city_name + '.pickle'
            self.loaded_graphs[city_name] = pickle_path
            self.G = ox.graph_from_place(city_name)
            self.dump_graph_pickle(pickle_path)
            print('Loaded graph for {} and added to dump'.format(city_name))

    def plot_graph(self):
        ox.plot_graph(self.G)

    def dump_graph_pickle(self, pickle_path):
        pickle.dump(self.G, open(pickle_path, 'wb'))

    def load_graph_from_path(self, pickle_path):
        self.G = pickle.load(open(pickle_path, 'rb'))

    def get_stats(self):
        num_nodes = self.G.number_of_nodes()
        num_edges = self.G.number_of_edges()
        return num_nodes, num_edges

    def get_adjacency_for_node(self, node_id):
        for i in self.G.adjacency():
            if i[0] == node_id:
                print(i)

    def get_graph(self):
        return self.G

    def add_elevation_to_graph(self):
        # Todo: Abhik D.
        pass
