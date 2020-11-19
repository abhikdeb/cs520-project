import osmnx as ox
import networkx as nx 
from data_model import DataModel
from shortest_path_new import Routing

data_model = DataModel()

G = data_model.get_graph()

router = Routing(data_model)


baseline_path, logs = router.get_optimal_path("baseline")
router.plot_route(baseline_path)

best_path, logs = router.get_optimal_path("minimize")
print(logs)
router.plot_route(best_path)

best_path, logs = router.get_optimal_path("maximize")
print(logs)
router.plot_route(best_path)