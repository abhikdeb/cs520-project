from flask import render_template, jsonify
from googlemaps import Client

from EleNa.src.app import app
from EleNa.src.app.data_model.data_model import DataModel
from EleNa.src.app.data_model.shortest_path import Routing
from EleNa.src.config import Config

g_maps = Client(key=Config.API_KEY)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Flask Gateway to the home page of the web server.

    Returns:
        Flask rendered HTML page

    """
    page_title = 'Home Page'
    default_coords = {'lat': 42.3732, 'lng': -72.5199}  # Default location is Amherst, MA
    default_zoom = 15
    data_vars = {
        'zoom': default_zoom,
        'lat': default_coords['lat'],
        'lng': default_coords['lng']
    }
    return render_template('home.html', title=page_title, data=data_vars)


@app.route('/submit<data>', methods=['GET', 'POST'])
def submit(data):
    """
    Gateway to computing the route on submit from flask.
    Args:
        data: Contains encoded string extract constraints for route computations

    Returns:
        Resulting route info to be rendered.

    """
    if bool(data):
        data = data.replace("%2C", ",")
        data = data.replace("%20", " ")
        source, destination, percent, maxmin = data.split(":")
        source_coords = [g_maps.geocode(source)[0]['geometry']['location']['lat'],
                         g_maps.geocode(source)[0]['geometry']['location']['lng']]
        destination_coords = [g_maps.geocode(destination)[0]['geometry']['location']['lat'],
                              g_maps.geocode(destination)[0]['geometry']['location']['lng']]
        result = compute_route(source_coords, destination_coords, float(percent) / 100.0, maxmin)
        return result


def compute_route(source, destination, per, task):
    """
     Returns the best route with the given constraints.

    Args:
        source: Coordinates of the starting position
        destination: Coordinates of the destination
        per: x percentage of the shortest path to be computed
        task: maximize or minimize

    Returns:
        JSON object containing information on the routes to be rendered

    """
    model_obj = DataModel('Amherst, MA')
    routing_obj = Routing(model_obj)

    routing_obj.set_start_end(source, destination)
    routing_obj.set_max_deviation(per)
    best_path, log = routing_obj.get_shortest_path(task)

    sampled_coords = []
    if len(best_path) > 20:
        skip = len(best_path) // 20 + 1
        i = 0
        while i < len(best_path) - 1:
            sampled_coords.append(best_path[i])
            i += skip
        sampled_coords.append(best_path[len(best_path) - 1])
    else:
        sampled_coords = best_path

    result = []
    for node in sampled_coords:
        result.append({
            "Lat": model_obj.get_graph().nodes[node]['y'],
            "Long": model_obj.get_graph().nodes[node]['x']
        })

    gmap_route = routing_obj.get_gmap_ground_truth(source, destination)
    print(gmap_route)

    if task == "minimize":
        return jsonify(waypoints=result, elevation=round(log['best_path_gain_min'], 3),
                       distance=round(log['best_path_dist_min'], 3),
                       groundTruthDistance=round(log['shortest_path_dist'], 3),
                       groundTruthElevation=round(log['min_dist_grade'], 3),
                       upperLimit=round(per * log['shortest_path_dist'], 3), ground_truth=gmap_route)
    else:
        return jsonify(waypoints=result, elevation=round(log['best_path_gain_max'], 3),
                       distance=round(log['best_path_dist_max'], 3),
                       groundTruthDistance=round(log['shortest_path_dist'], 3),
                       groundTruthElevation=round(log['min_dist_grade'], 3),
                       upperLimit=round(per * log['shortest_path_dist'], 3), ground_truth=gmap_route)
