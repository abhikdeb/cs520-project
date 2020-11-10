import os
import osmnx as ox
import pickle as pickle
import glob
import json


class DataModel:

    def __init__(self, city_name='Amherst, MA'):

        self.graphs_location = 'stored_locations/'
        self.load_locations_metadata()
        
        if city_name in self.loaded_graphs:
            self.load_graph_from_path(self.loaded_graphs[city_name])
            print('Loaded graph for {} from dump'.format(city_name))
        else:
            pickle_path = self.graphs_location + city_name + '.pickle'
            self.loaded_graphs[city_name] = pickle_path
            self.G = ox.graph_from_place(city_name)
            self.dump_graph_pickle(pickle_path)
            self.update_locations_metadata()
            print('Loaded graph for {} and added to dump'.format(city_name))

    def load_locations_metadata(self):
        with open(self.graphs_location + 'metadata.json') as f:
            self.loaded_graphs = json.load(f)

    def update_locations_metadata(self):
        with open(self.graphs_location + 'metadata.json', "w") as outfile:  
            json.dump(self.loaded_graphs, outfile, indent = 4) 

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
