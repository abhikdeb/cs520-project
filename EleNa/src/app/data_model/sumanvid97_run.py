import osmnx as ox
import networkx as nx 
from data_model import DataModel
from shortest_path import *
from shortest_path import Routing

data_model = DataModel()

G = data_model.get_graph()

start_loc=(42.35042, -72.52712)
end_loc=(42.40791, -72.53425)


routing = Routing(data_model)
print(routing.get_shortest_path_length(start_loc, end_loc))


# start = routing.get_node(start_loc)
# end = routing.get_node(end_loc)

# print(start, end)

# print(G.nodes[start])

# for u, v, k, data in G.edges(keys=True, data=True):
#     print(G.get_edge_data(u, v))
#     print(u, v, k)
#     print(data)
#     print(dict(G.adjacency()).get(u))
#     input()

# grade = elevation / length