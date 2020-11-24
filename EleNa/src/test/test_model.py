import random
import googlemaps

from EleNa.src.app.data_model.data_model import DataModel
from EleNa.src.app.data_model.shortest_path import Routing
from EleNa.src.config import Config


def test_model_availability():
    dm = DataModel('Amherst, MA')
    assert dm.G != {}

def test_config_value():
    d = DataModel('Amherst, MA')
    assert d.config != {}

def test_load_locations_metadata_function():
    dm = DataModel('Amherst, MA')
    dm.load_locations_metadata()
    assert dm.loaded_graphs != {}

def test_load_config_function():
    dm = DataModel('Amherst, MA')
    dm.load_config('../app/config.json')
    assert dm.config != {}

def test_get_stats_function():
    dm = DataModel('Amherst, MA')
    num_nodes, num_edges = dm.get_stats()
    assert num_nodes>=0 and num_edges>=0

def test_evaluation():
    x = 1.6

    key = Config.API_KEY
    client = googlemaps.Client(key)

    # setup EleNa for evaluation purposes
    data_model = DataModel('Amherst, MA')
    graph = data_model.get_graph()
    routing = Routing(data_model)
    nodes = graph.nodes()

    # randomly sample nodes from this list of nodes
    p1 = random.sample(nodes, 1)[0]
    p2 = random.sample(nodes, 1)[0]
    from_node = (graph.nodes[p1]['y'], graph.nodes[p1]['x'])
    to_node = (graph.nodes[p2]['y'], graph.nodes[p2]['x'])
    # print(from_node, to_node)
    routing.set_start_end(from_node, to_node)
    routing.set_max_deviation(x)
    best_path_min, log_min = routing.get_shortest_path("minimize")
    best_path_max, log_max = routing.get_shortest_path("maximize")

    # get distance from Google Maps - Direction Service
    routes = client.directions(from_node, to_node, mode="walking")
    ground_truth = routes[0]["legs"][0]["distance"]["value"]

    assert ground_truth * x > log_min['optimal_path_dist']
    assert ground_truth * x > log_max['optimal_path_dist']
