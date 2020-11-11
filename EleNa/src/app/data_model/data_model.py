import osmnx as ox
import pickle as pickle
import json


class DataModel:

    def __init__(self, city_name='Amherst, MA'):
        self.config = {}
        self.load_config('../config.json')
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

    def load_config(self, loc):
        try:
            cfg_file = open(loc, "r")
            self.config = cfg_file.load(cfg_file)
        except OSError as err:
            print("Config File Read Error: {0}".format(err))
        else:
            cfg_file.close()

    def load_locations_metadata(self):
        with open(self.graphs_location + 'metadata.json') as f:
            self.loaded_graphs = json.load(f)

    def update_locations_metadata(self):
        with open(self.graphs_location + 'metadata.json', "w") as outfile:
            json.dump(self.loaded_graphs, outfile, indent=4)

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
        if len(self.config.keys()) == 0 or 'api_key' not in self.config['google_api']:
            print("Config File Error")
            raise ValueError
        ox.elevation.add_node_elevations(self.G, self.config['google_api']['api_key'],
                                         max_locations_per_batch=self.config['google_api']['elevation_api'][
                                             'batch_size'],
                                         precision=self.config['google_api']['elevation_api']['precision'])
        ox.elevation.add_edge_grades(self.G, add_absolute=self.config['google_api']['elevation_api']['add_absolute'])
        pass
