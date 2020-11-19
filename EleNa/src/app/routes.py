from flask import render_template, redirect, url_for, request, jsonify
from flask_googlemaps import Map
from googlemaps import Client

from EleNa.src.app import app
from EleNa.src.config import Config
from EleNa.src.app.data_model.data_model import DataModel
from EleNa.src.app.data_model.shortest_path import Routing

gmaps = Client(key=Config.API_KEY)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    page_title = 'Home Page'
    return render_template('home.html', title=page_title)


@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'username': 'Test_User_1'}
    # 42.375755, -72.519789
    # 42.350887, -72.528246
    # 42.395215, -72.531281
    # map_obj = Map(
    #     identifier="map",
    #     lat=42.375755,
    #     lng=-72.519789,
    #     zoom=13,
    #     center_on_user_location=False
    # )
    return render_template('index.html', title='Home Page', user=user)  #


# @app.route('/map', methods=['POST', 'GET'])
# def load_map():
#     map_view = Map(
#         identifier="map_view",
#         lat=42.375755,
#         lng=-72.519789,
#         zoom=13,
#         # markers=[
#         #     {
#         #         'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
#         #         'lat': 42.350887,
#         #         'lng': -72.528246,
#         #         'infobox': "<b>Source</b>"
#         #     },
#         #     {
#         #         'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
#         #         'lat': 42.395215,
#         #         'lng': -72.531281,
#         #         'infobox': "<b>Destination</b>"
#         #     }
#         # ],
#         style="height:500px;width:750px;margin:10;",
#         center_on_user_location=False
#     )
#     form = SearchForm()
#     if form.validate_on_submit():
#         return redirect(url_for('submit'))
#     return render_template('rendermap.html', form=form, map_view=map_view)


@app.route('/submit<data>', methods=['GET', 'POST'])
def submit(data):
    if bool(data):
        data = data.replace("%2C", ",")
        data = data.replace("%20", " ")
        source, destination, percent, maxmin = data.split(":")
        source_coords = [gmaps.geocode(source)[0]['geometry']['location']['lat'],
                         gmaps.geocode(source)[0]['geometry']['location']['lng']]
        destination_coords = [gmaps.geocode(destination)[0]['geometry']['location']['lat'],
                              gmaps.geocode(destination)[0]['geometry']['location']['lng']]

        print(source_coords)
        print(destination_coords)
        print(percent)
        print(maxmin)

        result = get_route(source_coords, destination_coords, float(percent) / 100.0, maxmin)
        print(result)
        return result


def get_route(source, destination, per, task):
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

    print(log)

    if task == "minimize":
        return jsonify(waypoints=result, elevation=log['best_path_gain_min'], distance=log['best_path_dist_min'],
                       groundTruthDistance=log['shortest_path_dist'], groundTruthElevation=log['min_dist_grade'],
                       ground_truth=gmap_route)
    else:
        return jsonify(waypoints=result, elevation=log['best_path_gain_max'], distance=log['best_path_dist_max'],
                       groundTruthDistance=log['shortest_path_dist'], groundTruthElevation=log['min_dist_grade'],
                       ground_truth=gmap_route)
