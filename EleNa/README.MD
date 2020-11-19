# EleNA : Elevation based Navigation

### Description

Existing navigation systems optimize for the shortest or fastest route. 
However, they do not consider elevation gain. 
Let’s say you are hiking or biking from one location to another. 
You may want to literally go the extra mile if that saves you a couple thousand feet in elevation gain. 
Likewise, you may want to maximize elevation gain if you are looking for an intense yet time-constrained workout.


Given a start and an end location, a route that maximizes or minimizes elevation gain, 
while limiting the total distance between the two locations to x% of the shortest path.


### Index

1. Data Model
2. Querying from Data Model
3. Routing Algorithm
4. Rendering the computed output

### Components

1. DATA - Region graph (GoogleMaps/OpenStreetMap)
2. Query/Extract from graph

--------------------------------------------------------


- UI -> Inputs: start, end, x%, elevetion(Min/Max); Output: Maps
- Geocoding Inputs () - searchable Inputs
- Routing Algo (Graph, input_params) - A-Star, Djikstras, Heuristics
- Render output path on Map and provide summary


--------------------------------------------------------

### Architecture

1. Decoupled approach
  - Web UI Server
  - Back end service


2. Combined approach
  - Entire Web framework

--------------------------------------------------------
