# EleNA : Elevation based Navigation

Given below is the interface of our application

![Plot 1](https://github.com/abhikdeb/cs520-project/blob/dev/EleNa/images/user_interface.png)

### Index

1. [Components](#components)
2. [Architecture](#architecture)
3. [Evaluation](#evaluation)

### Components

Given below is a description of different components of our system

![Plot 2](https://github.com/abhikdeb/cs520-project/blob/dev/EleNa/images/components.png)

--------------------------------------------------------

### Architecture

Given below is the high-level architecture of our approach

![Plot 3](https://github.com/abhikdeb/cs520-project/blob/dev/EleNa/images/architecture.png)

--------------------------------------------------------

### Evaluation
#### Quantitative evaluation
[This](https://github.com/abhikdeb/cs520-project/blob/e3c0245709bdfb7268acf376be080052d0709600/EleNa/src/test/test_x_percent.py#L1) is the primary evaluation module.
The evaluation primarily does the following:
- Instantiates Google Directions Service for querying ground-truth
- Randomly samples 50-100 data points (both source and destination) from OSMNX's Amherst map
- For each pair of source and destination:
  - Computes EleNa route for maximization task (using 200% as the maximum deviation from ground-truth)
  - Computes EleNa route for minimization task (using 200% as the maximum deviation from ground-truth)
  - Queries ground-truth using Google Directions service
  
- Verifies that the routes returned by EleNa (for both minimization/maximization tasks) are within x% of the ground-truth, for each of the data-points
- Generates plots (using matplotlib.pyplot) for:
  - Elevation gain in routes computed by EleNa (for both minimization/maximization tasks) against the elevation in the ground-truth route
  - percentage deviation of distance in routes computed by EleNa compared to ground-truth

Here are the plots following the evaluation of EleNa:
![Plot 4](https://github.com/abhikdeb/cs520-project/blob/dev/EleNa/images/elevation_plot.png)
![Plot 5](https://github.com/abhikdeb/cs520-project/blob/dev/EleNa/images/percentage_deviation_plot.png)

The first plot shows the results for 50 data-points (both maximization and minimization task) - we see that EleNa performs quite well in both the maximization and minimization tasks. For maximization task, routes computed by EleNa result in an average elevation gain of ~8 meters. However, EleNa seems to perform, on average, better in the elevation minimizsation task, with ~15 meters reduction in elevation compared to the ground-truth.

The second plot shows the percentage deviation of distance in EleNa routes compared to the ground-truth, for the same 50 data-points that we used in the first plot, but with a constraint of x=150%. It is clear from the plot that routes computed by EleNa do not exceed 150% of the ground truth distance, for both the maximization and minimization task.

#### Visual evaluation
The above module aids with a "qualitative" evalution of EleNa. However, a picture is worth a thousand words. For this reason, we decided to render the ground-truth path (queried using Google's Directions Service) alongside EleNa routes on the primary UI. For this purpose, we wrote the [API](https://github.com/abhikdeb/cs520-project/blob/648c53e664d33eeb69cd0d3e4a9cd6f352466e1a/EleNa/src/app/data_model/shortest_path.py#L117) that computes the waypoints for the ground-truth route between any two points in the map. These waypoints are then rendered on the map in the main UI of EleNa, aiding the user to "visually" evaluate how EleNa performs.
