# EleNA : Elevation based Navigation


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
|PDoc3|0.9.1|`pdoc3`|


Setup a new environment using the conda/venv package managers.
We show how to create an environment using conda:

```shell script
conda create --name elena python=3.8.6
```

This environment can now be activated by:
```shell script
conda activate elena
```

Install the following packages:
- [osmnx](https://osmnx.readthedocs.io/en/stable/#installation)
- [googlemaps](https://pypi.org/project/googlemaps/)
- [scipy](https://pypi.org/project/scipy/)
- [flask](https://pypi.org/project/Flask/)
- [flask-googlemaps](https://flask-googlemaps.com/installation/)
- [flask-wtf](https://flask-wtf.readthedocs.io/en/stable/install.html)

### Running the app

---

Before running the app, make sure the `PYTHONPATH` is set to the root directory of the project.

Access [this](EleNa/scripts) folder for triggering the scripts to run the Flask API.
From the root folder of the repository, run:

```shell script
cd EleNa/scripts
```

For Linux/Unix systems, 

```shell script
./RunElenaApp.sh
``` 

For Windows systems,

```shell script
./RunElenaApp.bat
```

Then follow the on-screen instructions to open the specified URL on a web browser to run the web application.

### Running the Tests

---

PyTest is used to automate the testing process. 
Please read [this](https://docs.pytest.org/en/stable/contents.html#toc) to understand its usage.

From the [src](EleNa/src) folder, execute the following to build and run the tests.

```shell script
pytest
```

### Generating the documentation

---

[PyDoc3](https://pdoc3.github.io/pdoc/) is used to run the documentation service.

The generated documentation of the code can be accessed [here](EleNa/docs/README.md) or in [HTML](EleNa/docs/documentation/EleNa/)

Run the below to generate the documentation from the source code.

```shell script
pdoc --html EleNa --output-dir documentation
```

