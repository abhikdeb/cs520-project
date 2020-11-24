---
description: |
    API documentation for modules: EleNa, EleNa.src, EleNa.src.app, EleNa.src.app.data_model, EleNa.src.app.data_model.data_model, EleNa.src.app.data_model.shortest_path, EleNa.src.app.data_model.shortest_path_experiments, EleNa.src.app.forms, EleNa.src.app.routes, EleNa.src.config, EleNa.src.elena_app, EleNa.src.test, EleNa.src.test.test_model, EleNa.src.test.test_x_percent.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `EleNa` {#EleNa}




    
## Sub-modules

* [EleNa.src](#EleNa.src)






    
# Module `EleNa.src` {#EleNa.src}




    
## Sub-modules

* [EleNa.src.app](#EleNa.src.app)
* [EleNa.src.config](#EleNa.src.config)
* [EleNa.src.elena_app](#EleNa.src.elena_app)
* [EleNa.src.test](#EleNa.src.test)






    
# Module `EleNa.src.app` {#EleNa.src.app}




    
## Sub-modules

* [EleNa.src.app.data_model](#EleNa.src.app.data_model)
* [EleNa.src.app.forms](#EleNa.src.app.forms)
* [EleNa.src.app.routes](#EleNa.src.app.routes)






    
# Module `EleNa.src.app.data_model` {#EleNa.src.app.data_model}




    
## Sub-modules

* [EleNa.src.app.data_model.data_model](#EleNa.src.app.data_model.data_model)
* [EleNa.src.app.data_model.shortest_path](#EleNa.src.app.data_model.shortest_path)
* [EleNa.src.app.data_model.shortest_path_experiments](#EleNa.src.app.data_model.shortest_path_experiments)






    
# Module `EleNa.src.app.data_model.data_model` {#EleNa.src.app.data_model.data_model}







    
## Classes


    
### Class `DataModel` {#EleNa.src.app.data_model.data_model.DataModel}



> `class DataModel(city_name='Amherst, MA')`


Data Model part of Tech Stack to store spatial geo data in graph structure (adjacency lists)
Use OSMNX services to get graph as per location. Use Google Maps API to fetch elevation information

Initialize Data Model

#### Args

**```city_name```**
:   string with city name, state name.


If pre-built data model exists, load it. Else create and dump it







    
#### Methods


    
##### Method `add_elevation_to_graph` {#EleNa.src.app.data_model.data_model.DataModel.add_elevation_to_graph}



    
> `def add_elevation_to_graph(self)`


Use google maps API to add elevation to the graph
Returns: None

    
##### Method `dump_graph_pickle` {#EleNa.src.app.data_model.data_model.DataModel.dump_graph_pickle}



    
> `def dump_graph_pickle(self, pickle_path)`



###### Args

**```pickle_path```**
:   local path to dump data model graph


**```Returns```** :&ensp;<code>None</code>
:   &nbsp;



    
##### Method `get_adjacency_for_node` {#EleNa.src.app.data_model.data_model.DataModel.get_adjacency_for_node}



    
> `def get_adjacency_for_node(self, node_id)`



###### Args

**```node_id```**
:   node for which connections are required


**```Returns```** :&ensp;<code>adjacency list for the node corresponding to node\_id</code>
:   &nbsp;



    
##### Method `get_graph` {#EleNa.src.app.data_model.data_model.DataModel.get_graph}



    
> `def get_graph(self)`


Returns: graph to be used in shortest path algorithm

    
##### Method `get_stats` {#EleNa.src.app.data_model.data_model.DataModel.get_stats}



    
> `def get_stats(self)`


Returns: statistics corresponding to the graph, i.e number of nodes & edges

    
##### Method `load_config` {#EleNa.src.app.data_model.data_model.DataModel.load_config}



    
> `def load_config(self, loc)`


Load config corresponding to directory paths and API keys

###### Args

**```loc```**
:   path to config file


**```Returns```** :&ensp;<code>None</code>
:   &nbsp;



    
##### Method `load_graph_from_path` {#EleNa.src.app.data_model.data_model.DataModel.load_graph_from_path}



    
> `def load_graph_from_path(self, pickle_path)`



###### Args

**```pickle_path```**
:   path in the directory to load pre-built graph


**```Returns```** :&ensp;<code>data model (graph)</code>
:   &nbsp;



    
##### Method `load_locations_metadata` {#EleNa.src.app.data_model.data_model.DataModel.load_locations_metadata}



    
> `def load_locations_metadata(self)`


Load pre-built graphs from local directory path
Returns: None

    
##### Method `plot_graph` {#EleNa.src.app.data_model.data_model.DataModel.plot_graph}



    
> `def plot_graph(self)`


Plot graph using OSMNX
Returns: None

    
##### Method `update_locations_metadata` {#EleNa.src.app.data_model.data_model.DataModel.update_locations_metadata}



    
> `def update_locations_metadata(self)`


Update json with loaded_graphs information
Returns: None



    
# Module `EleNa.src.app.data_model.shortest_path` {#EleNa.src.app.data_model.shortest_path}






    
## Functions


    
### Function `find_path_edges` {#EleNa.src.app.data_model.shortest_path.find_path_edges}



    
> `def find_path_edges(graph, path, weight, mode)`


used to alter the path edges in case multiple edges exist between two neigbors
weight: length or grade or elevation(=length*grade)
mode: min or max


    
## Classes


    
### Class `Routing` {#EleNa.src.app.data_model.shortest_path.Routing}



> `class Routing(data_model)`


Routing part of Tech Stack to find shortest path using elevation data
Dijkstra and optimization based solution to find optimal solution (based on distance & elevation gain)







    
#### Methods


    
##### Method `get_gmap_ground_truth` {#EleNa.src.app.data_model.shortest_path.Routing.get_gmap_ground_truth}



    
> `def get_gmap_ground_truth(self, source, destination)`


Get ground truth (shortest path) from Google Maps API with given source and destination

###### Args

**```source```**
:    starting coordinates (latitude and longitude)


**```destination```**
:   ending coordinates (latitude and longitude)


**```Returns```** :&ensp;<code>Shortest Path based on Google Maps API</code>
:   &nbsp;



    
##### Method `get_node` {#EleNa.src.app.data_model.shortest_path.Routing.get_node}



    
> `def get_node(self, loc)`



###### Args

**```loc```**
:   coordinates to get the node


**```Returns```** :&ensp;`Nearest Node from the location specified by 'loc'`
:   &nbsp;



    
##### Method `get_shortest_path` {#EleNa.src.app.data_model.shortest_path.Routing.get_shortest_path}



    
> `def get_shortest_path(self, mode)`


Find optimal path based on three modes - 'baseline' , 'minimize', 'maximize'

###### Args

**```mode```**
:   mode in which to find optimal path


- baseline : find shortest path using networkx's inbuilt algorithm using only 'length' and no 'elevation'
- minimize : find shortest path which minimizes elevation gain and stays within x% of baseline shortest path length
- maximize : find shortest path which maximizes elevation gain and stays within x% of baseline shortest path length

###### Returns

<code>Optimal path as a list</code> of <code>nodes</code>
:   &nbsp;



    
##### Method `optimize_elevation_gain` {#EleNa.src.app.data_model.shortest_path.Routing.optimize_elevation_gain}



    
> `def optimize_elevation_gain(self, x, baseline_dict, mode)`


x: (> 1.0) how large can the path length be, compared to the shortest existing path
baseline_dict: {'path': min_dist_path, 'length': min_dist, 'ele_gain': min_ele_gain, 'edge_keys': min_dist_keys}
mode: 'minimize' or 'maximize'

    
##### Method `plot_route` {#EleNa.src.app.data_model.shortest_path.Routing.plot_route}



    
> `def plot_route(self, route)`


Plot the graph with given route using OSMNX plot feature

###### Args

**```route```**
:   plot the given route


**```Returns```** :&ensp;<code>None</code>
:   &nbsp;



    
##### Method `set_max_deviation` {#EleNa.src.app.data_model.shortest_path.Routing.set_max_deviation}



    
> `def set_max_deviation(self, x)`


Set maximum constraints on distance to travel

###### Args

**```x```**
:   x% constraint on the shortest path length


**```Returns```** :&ensp;<code>None</code>
:   &nbsp;



    
##### Method `set_start_end` {#EleNa.src.app.data_model.shortest_path.Routing.set_start_end}



    
> `def set_start_end(self, start_loc, end_loc)`


Get start, end nodes as per start, end coordinates

###### Args

**```start_loc```**
:   starting coordinates (latitude and longitude)


**```end_loc```**
:   ending coordinates (latitude and longitude)


**```Returns```** :&ensp;<code>None</code>
:   &nbsp;





    
# Module `EleNa.src.app.data_model.shortest_path_experiments` {#EleNa.src.app.data_model.shortest_path_experiments}






    
## Functions


    
### Function `find_path_edges` {#EleNa.src.app.data_model.shortest_path_experiments.find_path_edges}



    
> `def find_path_edges(graph, path, min_weight='grade')`




    
### Function `find_path_edges_max` {#EleNa.src.app.data_model.shortest_path_experiments.find_path_edges_max}



    
> `def find_path_edges_max(graph, path, min_weight='grade')`




    
### Function `find_path_edges_min` {#EleNa.src.app.data_model.shortest_path_experiments.find_path_edges_min}



    
> `def find_path_edges_min(graph, path, min_weight='grade')`





    
## Classes


    
### Class `Routing` {#EleNa.src.app.data_model.shortest_path_experiments.Routing}



> `class Routing(data_model)`










    
#### Methods


    
##### Method `dfs_get_all_paths` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.dfs_get_all_paths}



    
> `def dfs_get_all_paths(self, graph, start, goal, max_length)`




    
##### Method `get_all_paths` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.get_all_paths}



    
> `def get_all_paths(self, graph, source, target, allowed_hops)`




    
##### Method `get_cost` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.get_cost}



    
> `def get_cost(self, graph_projection, a, b)`




    
##### Method `get_elevation_of_path` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.get_elevation_of_path}



    
> `def get_elevation_of_path(self, graph, path)`




    
##### Method `get_gmap_ground_truth` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.get_gmap_ground_truth}



    
> `def get_gmap_ground_truth(self, source, destination)`




    
##### Method `get_length_of_path` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.get_length_of_path}



    
> `def get_length_of_path(self, graph, path)`




    
##### Method `get_node` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.get_node}



    
> `def get_node(self, loc)`




    
##### Method `get_shortest_path` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.get_shortest_path}



    
> `def get_shortest_path(self, mode)`




    
##### Method `get_shortest_path_length` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.get_shortest_path_length}



    
> `def get_shortest_path_length(self)`


arguments: start and end locations
returns: the shortest path length between the start and the end nodes
Note: it can also be modified to return the path as list of nodes using backtrace()
credits: <https://github.com/blkrt/dijkstra-python>

    
##### Method `maximize_elevation_gain` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.maximize_elevation_gain}



    
> `def maximize_elevation_gain(self, percent_shortest_path)`




    
##### Method `maximize_elevation_gain_ML` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.maximize_elevation_gain_ML}



    
> `def maximize_elevation_gain_ML(self, percent_shortest_path)`




    
##### Method `minimize_elevation_gain` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.minimize_elevation_gain}



    
> `def minimize_elevation_gain(self, percent_shortest_path)`




    
##### Method `minimize_elevation_gain_ML` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.minimize_elevation_gain_ML}



    
> `def minimize_elevation_gain_ML(self, percent_shortest_path)`




    
##### Method `plot_route` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.plot_route}



    
> `def plot_route(self, route)`




    
##### Method `set_max_deviation` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.set_max_deviation}



    
> `def set_max_deviation(self, x)`




    
##### Method `set_start_end` {#EleNa.src.app.data_model.shortest_path_experiments.Routing.set_start_end}



    
> `def set_start_end(self, start_loc, end_loc)`






    
# Module `EleNa.src.app.forms` {#EleNa.src.app.forms}







    
## Classes


    
### Class `FieldsRequiredForm` {#EleNa.src.app.forms.FieldsRequiredForm}



> `class FieldsRequiredForm(*args, **kwargs)`


Require all fields to have content. This works around the bug that WTForms radio
fields don't honor the <code>DataRequired</code> or <code>InputRequired</code> validators.

:param formdata:
    Used to pass data coming from the enduser, usually <code>request.POST</code> or
    equivalent. formdata should be some sort of request-data wrapper which
    can get multiple parameters from the form input, and values are unicode
    strings, e.g. a Werkzeug/Django/WebOb MultiDict
:param obj:
    If <code>formdata</code> is empty or not provided, this object is checked for
    attributes matching form field names, which will be used for field
    values.
:param prefix:
    If provided, all fields will have their name prefixed with the
    value.
:param data:
    Accept a dictionary of data. This is only used if <code>formdata</code> and
    <code>obj</code> are not present.
:param meta:
    If provided, this is a dictionary of values to override attributes
    on this form's meta instance.
:param `**kwargs`:
    If <code>formdata</code> is empty or not provided and <code>obj</code> does not contain
    an attribute named the same as a field, form will assign the value
    of a matching keyword argument to the field, if one exists.


    
#### Ancestors (in MRO)

* [flask_wtf.form.FlaskForm](#flask_wtf.form.FlaskForm)
* [wtforms.form.Form](#wtforms.form.Form)
* [wtforms.compat.NewBase](#wtforms.compat.NewBase)
* [wtforms.form.BaseForm](#wtforms.form.BaseForm)


    
#### Descendants

* [EleNa.src.app.forms.SearchForm](#EleNa.src.app.forms.SearchForm)


    
#### Class variables


    
##### Variable `Meta` {#EleNa.src.app.forms.FieldsRequiredForm.Meta}






    
### Class `SearchForm` {#EleNa.src.app.forms.SearchForm}



> `class SearchForm(*args, **kwargs)`


Require all fields to have content. This works around the bug that WTForms radio
fields don't honor the <code>DataRequired</code> or <code>InputRequired</code> validators.

:param formdata:
    Used to pass data coming from the enduser, usually <code>request.POST</code> or
    equivalent. formdata should be some sort of request-data wrapper which
    can get multiple parameters from the form input, and values are unicode
    strings, e.g. a Werkzeug/Django/WebOb MultiDict
:param obj:
    If <code>formdata</code> is empty or not provided, this object is checked for
    attributes matching form field names, which will be used for field
    values.
:param prefix:
    If provided, all fields will have their name prefixed with the
    value.
:param data:
    Accept a dictionary of data. This is only used if <code>formdata</code> and
    <code>obj</code> are not present.
:param meta:
    If provided, this is a dictionary of values to override attributes
    on this form's meta instance.
:param `**kwargs`:
    If <code>formdata</code> is empty or not provided and <code>obj</code> does not contain
    an attribute named the same as a field, form will assign the value
    of a matching keyword argument to the field, if one exists.


    
#### Ancestors (in MRO)

* [EleNa.src.app.forms.FieldsRequiredForm](#EleNa.src.app.forms.FieldsRequiredForm)
* [flask_wtf.form.FlaskForm](#flask_wtf.form.FlaskForm)
* [wtforms.form.Form](#wtforms.form.Form)
* [wtforms.compat.NewBase](#wtforms.compat.NewBase)
* [wtforms.form.BaseForm](#wtforms.form.BaseForm)



    
#### Class variables


    
##### Variable `destination` {#EleNa.src.app.forms.SearchForm.destination}



    
##### Variable `maxmin` {#EleNa.src.app.forms.SearchForm.maxmin}



    
##### Variable `percent` {#EleNa.src.app.forms.SearchForm.percent}



    
##### Variable `source` {#EleNa.src.app.forms.SearchForm.source}



    
##### Variable `submit` {#EleNa.src.app.forms.SearchForm.submit}








    
# Module `EleNa.src.app.routes` {#EleNa.src.app.routes}






    
## Functions


    
### Function `compute_route` {#EleNa.src.app.routes.compute_route}



    
> `def compute_route(source, destination, per, task)`


Returns the best route with the given constraints.


###### Args

**```source```**
:   Coordinates of the starting position


**```destination```**
:   Coordinates of the destination


**```per```**
:   x percentage of the shortest path to be computed


**```task```**
:   maximize or minimize



###### Returns

<code>JSON object containing information on the routes to be rendered</code>
:   &nbsp;



    
### Function `home` {#EleNa.src.app.routes.home}



    
> `def home()`


Flask Gateway to the home page of the web server.


###### Returns

<code>Flask rendered HTML page</code>
:   &nbsp;



    
### Function `submit` {#EleNa.src.app.routes.submit}



    
> `def submit(data)`


Gateway to computing the route on submit from flask.

###### Args

**```data```**
:   Contains encoded string extract constraints for route computations



###### Returns

Resulting route info to be rendered.




    
# Module `EleNa.src.config` {#EleNa.src.config}







    
## Classes


    
### Class `Config` {#EleNa.src.config.Config}



> `class Config()`







    
#### Class variables


    
##### Variable `API_KEY` {#EleNa.src.config.Config.API_KEY}



    
##### Variable `SECRET_KEY` {#EleNa.src.config.Config.SECRET_KEY}



    
##### Variable `cfg` {#EleNa.src.config.Config.cfg}



    
##### Variable `cfg_file` {#EleNa.src.config.Config.cfg_file}








    
# Module `EleNa.src.elena_app` {#EleNa.src.elena_app}









    
# Module `EleNa.src.test` {#EleNa.src.test}




    
## Sub-modules

* [EleNa.src.test.test_model](#EleNa.src.test.test_model)
* [EleNa.src.test.test_x_percent](#EleNa.src.test.test_x_percent)






    
# Module `EleNa.src.test.test_model` {#EleNa.src.test.test_model}






    
## Functions


    
### Function `test_config_value` {#EleNa.src.test.test_model.test_config_value}



    
> `def test_config_value()`




    
### Function `test_evaluation` {#EleNa.src.test.test_model.test_evaluation}



    
> `def test_evaluation()`




    
### Function `test_get_stats_function` {#EleNa.src.test.test_model.test_get_stats_function}



    
> `def test_get_stats_function()`




    
### Function `test_load_config_function` {#EleNa.src.test.test_model.test_load_config_function}



    
> `def test_load_config_function()`




    
### Function `test_load_locations_metadata_function` {#EleNa.src.test.test_model.test_load_locations_metadata_function}



    
> `def test_load_locations_metadata_function()`




    
### Function `test_model_availability` {#EleNa.src.test.test_model.test_model_availability}



    
> `def test_model_availability()`







    
# Module `EleNa.src.test.test_x_percent` {#EleNa.src.test.test_x_percent}







    
## Classes


    
### Class `Evaluation` {#EleNa.src.test.test_x_percent.Evaluation}



> `class Evaluation(x=1.5, city_name='Amherst, MA', n_tests=50)`










    
#### Methods


    
##### Method `dump_evalution_params` {#EleNa.src.test.test_x_percent.Evaluation.dump_evalution_params}



    
> `def dump_evalution_params(self)`




    
##### Method `eval` {#EleNa.src.test.test_x_percent.Evaluation.eval}



    
> `def eval(self)`




    
##### Method `load_config` {#EleNa.src.test.test_x_percent.Evaluation.load_config}



    
> `def load_config(self, loc)`





-----
Generated by *pdoc* 0.8.1 (<https://pdoc3.github.io>).
