# EleNA : Elevation based Navigation
====

### Description

---
Existing navigation systems optimize for the shortest or fastest route. 
However, they do not consider elevation gain. 
Let’s say you are hiking or biking from one location to another. 
You may want to literally go the extra mile if that saves you a couple thousand feet in elevation gain. 
Likewise, you may want to maximize elevation gain if you are looking for an intense yet time-constrained workout.


For more about the architecture and evaluation, read [this](EleNa/README.MD)!


### Setup/Installation Instructions

----

At the time this project was built, the following were the system specifications:

|Tool/Package|Version||
|:---:|:---:|:---:|
|Python |3.8.6||
|Conda |4.9.0||
|Flask|1.1.2|`flask`, `flask-wtf`|
|Werkzeug|1.0.1||
|OpenStreetMap API|0.16.1|`osmnx`|
|GoogleMaps API|4.4.2|`googlemaps`|
|PyTest|6.1.2|`pytest`|


Setup a new environment using the conda/venv package managers.
We show how to create an environment using conda:

```shell script
conda create --name elena python=3.5
```

This environment can now be activated by:
```shell script
conda activate elena
```

Install the required packages from the [requirements file](EleNa/docs/requirements.txt)

```shell script
pip install -r requirements.txt
```

