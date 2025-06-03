# SnapAI: A Simulator for Network Algorithms and Protocols in Python

This is a simulator for network algorithms and protocols in Python. It is a web application that allows the user to create and run simulations of network algorithms and protocols. The simulator is built using Django and JavaScript. The simulator is designed to be modular, allowing the user to create new models for nodes, mobility, distribution, connectivity, message transmission, reliability, and interference. The simulator also allows the user to create new projects with custom node implementations and models. The simulator includes a graph visualization tool that allows the user to visualize the network topology and the messages transmitted between nodes. The simulator also includes tools for analyzing the network, such as shortest path algorithms and node embedding algorithms.

# Table of Contents

- [SnapAI: A Simulator for Network Algorithms and Protocols in Python](#snapai-a-simulator-for-network-algorithms-and-protocols-in-python)
- [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Creating projects](#creating-projects)
  - [Executing projects](#executing-projects)
    - [Adding new batches of nodes to the simulation](#adding-new-batches-of-nodes-to-the-simulation)
    - [Executing shortest path algorithm](#executing-shortest-path-algorithm)
    - [Executing Node2Vec algorithm](#executing-node2vec-algorithm)
    - [Commands to export dependencies](#commands-to-export-dependencies)

## Getting Started

> You can see a more detailed tutorial in the [installation.md](installation.md) file.
> This section will guide you through the steps to set up the simulator on your local machine.

1. Requirements:
You need to have a modern browser (Chrome, Firefox, Edge, Opera, ...) and python installed on your computer. You can download python from [here](https://www.python.org/downloads/).

2. Install conda
You can install anaconda or miniconda. We will use miniconda.
*Maybe you will need to install conda in your PATH variable, you can do it with the following command:*
```bash
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

3. Create a new environment
```bash
$ conda env create -f env.yml
```
```bash
$ conda activate mobenv
```

4. Making migrations
```bash
$ python manage.py makemigrations
```
```bash
$ python manage.py migrate
```

5. Run server
```bash
$ python manage.py runserver
```

6. Open browser and go to [http://localhost:8000/mobsinet/graph/](http://localhost:8000/mobsinet/graph/)

## Creating projects

1. Create a new folder in the projects directory
2. Create a config.json file in the new folder
```json
{
    "project": "project_name_here",
    "simulation_rounds": 100,
    "simulation_name": "NameOfTheSimulation",
    "simulation_refresh_rate": 0,
    "num_nodes": 30,
    "node_size": 5,
    "node": "project_name:node_implementation",
    "minDimX": 0,
    "minDimY": 0,
    "dimX": 10000,
    "dimY": 10000,
    "network_parameters": {
        "type": "random_graph",
        "avg_degree": 2
    },
    "distribution_model": "random_dist",
    "distribution_model_parameters": {
        "orientation": "horizontal",
        "line_position": 0,
        "number_of_nodes": 500,
        "midpoint": [
            9500,
            500
        ],
        "rotation_direction": "anti-clockwise",
        "radius": 0,
        "trace_file": null,
        "is_lat_long": true,
        "should_padding": true,
        "addapt_to_dimensions": true
    },
    "mobility_model": "random_walk",
    "mobility_model_parameters": {
        "speed_range": [
            0.03,
            0.03
        ],
        "direction_range": [
            0,
            5.283185307179586
        ],
        "travel_distance": 100000000000,
        "travel_time": 50000000000000,
        "prioritize_speed": true,
        "trace_file": null,
        "waiting_time_range": 30,
        "move_time_range": 1000,
        "waypoint_radius_range": [
            2,
            50
        ],
        "is_lat_long": true,
        "should_padding": true,
        "addapt_to_dimensions": true
    },
    "connectivity_model": "qudg_connectivity",
    "connectivity_model_parameters": {
        "max_radius": 500,
        "min_radius": 200,
        "big_radius_probability": 0.5
    },
    "reliability_model": "reliable_delivery",
    "interference_model": "no_interference",
    "message_transmission_model": "constant_time",
    "message_transmission_model_parameters": {
        "constant_transmission_time": 1,
        "random_transmission_min_time": 1,
        "random_transmission_max_time": 10
    },
    "nack_messages_enabled": false,
    "interference_model_parameters": {
        "intensity": 90
    },
    "asynchronous": false,
    "save_trace": true,
    "node_color": "#0000aa",
    "connectivity_enabled": true
}
```
3. Create a node implementation in your project (optional)
You must create a `nodes` folder in your project folder and create a python file with the node implementation. The node implementation must inherit from the `AbcNode` class. You can see the available methods in the `AbcNode` class. Here is an example of a node implementation:
```python
from ....models.nodes.abc_node import AbcNode

# Useful imports
from ....global_vars import Global
from ....network_simulator import simulation
from ....configuration.sim_config import config


class MyProjectNode(AbcNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.your_node_attribute = None

    def handle_messages(self, inbox):
        # Handle received messages
        pass

    def check_requirements(self):
        # Requirements to init the node in the simulation
        return super().check_requirements()

    def init(self):
        # Initialize the node
        return super().init()

    def on_neighboorhood_change(self):
        # Actions to be taken when the neighborhood changes
        return super().on_neighboorhood_change()

    def post_step(self):
        # Actions to be taken after each step
        return super().post_step()

    def pre_step(self):
        # Actions to be taken before each step
        return super().pre_step()

    # Add other methods here, you can see the available methods in the AbcNode class


node = MyProjectNode # Every node implementation must have a node variable

```
4. Create a new model in your project (optional)
You must create a folder for each type of model in your project folder (`mobility_models`,`distribution_models`, `connectivity_models`, `message_transmission_models`, `reliability_models`, `interference_models`), and create a python file with the model implementation. The model implementation must inherit from the the base class of each model type, (`AbcMobilityModel`, `AbcDistributionModel`, `AbcConnectivityModel`, `AbcMessageTransmissionModel`, `AbcReliabilityModel`, `AbcInterferenceModel`). You can see the available methods in the `AbcModel` class. You can see examples of model implementations in the `apps/mobsinet/simulator/defaults` folder.


## Executing projects

1. With the project installed, you can navigate to the project folder and run the following command:
```bash
$ source activate mobenv
```
```bash
$ python manage.py runserver
```
2. Open browser and go to [http://localhost:8000/mobsinet/graph/](http://localhost:8000/mobsinet/graph/) and select the project you want to run.
![alt text](doc/imgs/image.png "screenshot")

3. Click on the "Initialize" button to initialize the simulation.
4. Configure number of rounds, refresh rate and visualization fps.
5. Click on the "Run" button to start the simulation.
![alt text](doc/imgs/image2.png "screenshot")

### Adding new batches of nodes to the simulation

1. Start a simulation with the desired configuration.
2. Click on button "Show/Hide add nodes form" to open the form.
3. Fill the form with the desired configuration for the new batch of nodes.
4. Click on the "Add to the simulation" button to add the new batch of nodes to the simulation.
5. Click on the "Run" button to start the simulation.
![alt text](doc/imgs/image3.png)

### Executing shortest path algorithm
1. Start a simulation with the desired configuration.
2. Inputs the source and destination nodes.
3. Click on the "Shortest path" button to run the shortest path algorithm.
4. See the result in the output and in the graph.
![alt text](doc/imgs/tutorial-4.jpeg)

### Executing Node2Vec algorithm

1. Start a simulation with the desired configuration.
2. Input the dimensions of the embedding.
3. Click on the "Run Node2Vec algorithm".
4. See the result in the chart.
![alt text](doc/imgs/tutorial-5.jpeg)

---


### Commands to export dependencies
If you modify the environment, you can export the dependencies with the following commands, but we recommend that you modify manually the env.yml file.

```bash
$ conda env export --no-builds | grep -v "^prefix:"  > environment.yml
```
```bash
$ conda env export | grep -v "^prefix:" | sed -E 's/(=.+)//' > environment-noversion.yml
```
```bash
$ conda env export | grep -v "^prefix:" > environment-builds.yml 
```
```yml
name: mobenv
channels:
  - pyg
  - pytorch
  - conda-forge
  - defaults
  # you can add more channels here
dependencies:
  - django=4.2.18
  - networkx=3.4.2
  - node2vec=0.3.0
  - numpy=1.26.4
  - gensim=4.3.2
  - matplotlib=3.10.0
  - scipy=1.12.0
  - utm=0.7.0
  - scikit-learn=1.6.1
  - pytorch=2.3.1
  - dependency_name=version # add your new dependencies like this...
```