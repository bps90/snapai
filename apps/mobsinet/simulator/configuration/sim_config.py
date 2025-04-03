import json
from math import pi, sqrt


class SimulationConfig:
    def __init__(self, config_file=None):
        # Default values
        self.PROJECT_DIR = "apps/mobsinet/simulator/projects/"
        self.simulation_name = "Network Simulation"
        self.simulation_rounds = 1000
        self.simulation_refresh_rate = 1
        self.nack_messages_enabled = True
        self.num_nodes = 50
        self.node_color = '#000000'
        self.node_size = 1,
        self.dimX = 100
        self.dimY = 100
        self.dimZ = 100
        self.network_parameters = {
            'type': 'random_graph',
            'avg_degree': 4
        }
        self.node = 'inert_node'
        self.distribution_model = 'random_dist'
        self.distribution_model_parameters = {
            'orientation': 'horizontal',  # 'horizontal' or 'vertical'
            'line_position': None,
            'number_of_nodes': 100,
            'midpoint': (self.dimX / 2, self.dimY / 2),
            'rotation_direction': 'anti-clockwise',
            'radius': None,
        }
        self.mobility_model = 'random_mob'
        self.mobility_model_parameters = {
            # TODO: maybe turn it dependent by the specific mobility model
            'speed_range': [0, sqrt(self.dimX**2 + self.dimY**2)],
            'direction_range': [0, 2 * pi],
            'waiting_time_range': [0, 10],
            'move_time_range': [0, 10],
            'prioritize_speed': False,
            'travel_distance': None,
            'travel_time': self.simulation_rounds * 0.1  # 10% of the simulation time
        }
        self.connectivity_model = 'no_connectivity'
        self.connectivity_model_parameters = {
            # 10% da medida da menor dimensão do mapa
            'max_radius': self.dimX * 0.1 if self.dimX < self.dimY else self.dimY * 0.1,
            # 3% da medida da menor dimensão do mapa
            'min_radius': self.dimX * 0.03 if self.dimX < self.dimY else self.dimY * 0.03,
            'big_radius_probability': 0.5  # 50%
        }
        self.message_transmission_model = 'constant_time'
        self.message_transmission_model_parameters = {
            'constant_transmission_time': 1,
            'random_transmission_min_time': 1,
            'random_transmission_max_time': 10
        }
        self.reliability_model = 'no_reliability'
        self.reliability_model_parameters = {}
        self.interference_model = 'no_interference'
        self.interference_model_parameters = {
            'intensity': 50
        }
        self.message_protocol = 'TCP'
        self.verbose_logging = False
        self.asynchronous = False

        if config_file:
            self.load_from_file(config_file)

    def load_from_file(self, config_file):
        """
        Loads configuration data from a file and updates the simulation configuration parameters accordingly.

        Parameters
        ----------
        config_file : str
            The file path of the configuration file.
        """

        with open(config_file, 'r') as f:
            config_data = json.load(f)

        self.set_project_dir(config_data.get('PROJECT_DIR', self.PROJECT_DIR))
        self.set_simulation_name(config_data.get(
            'simulation_name', self.simulation_name))
        self.set_simulation_rounds(config_data.get(
            'simulation_rounds', self.simulation_rounds))
        self.set_simulation_refresh_rate(config_data.get(
            'simulation_refresh_rate', self.simulation_refresh_rate))
        self.set_nack_messages_enabled(config_data.get(
            'nack_messages_enabled', self.nack_messages_enabled))
        self.set_num_nodes(config_data.get('num_nodes', self.num_nodes))
        self.set_node_color(config_data.get('node_color', self.node_color))
        self.set_node_size(config_data.get('node_size', self.node_size))
        self.set_network_dimensions(config_data.get('dimX', self.dimX),
                                    config_data.get('dimY', self.dimY),
                                    config_data.get('dimZ', self.dimZ))
        self.set_network_parameters(config_data.get(
            'network_parameters', self.network_parameters))
        self.set_node(config_data.get('node', self.node))
        self.set_distribution_model(config_data.get(
            'distribution_model', self.distribution_model))
        self.set_distribution_model_parameters(config_data.get(
            'distribution_model_parameters', self.distribution_model_parameters))
        self.set_mobility_model(config_data.get(
            'mobility_model', self.mobility_model))
        self.set_mobility_model_parameters(config_data.get(
            'mobility_model_parameters', self.mobility_model_parameters))
        self.set_connectivity_model(config_data.get(
            'connectivity_model', self.connectivity_model))
        self.set_connectivity_model_parameters(config_data.get(
            'connectivity_model_parameters', self.connectivity_model_parameters))
        self.set_message_transmission_model(config_data.get(
            'message_transmission_model', self.message_transmission_model))
        self.set_message_transmission_model_parameters(config_data.get(
            'message_transmission_model_parameters', self.message_transmission_model_parameters))
        self.set_reliability_model(config_data.get(
            'reliability_model', self.reliability_model))
        self.set_reliability_model_parameters(config_data.get(
            'reliability_model_parameters', self.reliability_model_parameters))
        self.set_interference_model(config_data.get(
            'interference_model', self.interference_model))
        self.set_interference_model_parameters(config_data.get(
            'interference_model_parameters', self.interference_model_parameters))
        self.set_message_protocol(config_data.get(
            'message_protocol', self.message_protocol))
        self.set_verbose_logging(config_data.get(
            'verbose_logging', self.verbose_logging))
        self.set_asynchronous(config_data.get(
            'asynchronous', self.asynchronous))

    def set_project_dir(self, dirname):
        self.PROJECT_DIR = dirname

    def set_simulation_name(self, name):
        self.simulation_name = name

    def set_simulation_rounds(self, rounds):
        self.simulation_rounds = rounds

    def set_simulation_refresh_rate(self, refresh_rate):
        self.simulation_refresh_rate = refresh_rate

    def set_nack_messages_enabled(self, enabled):
        self.nack_messages_enabled = enabled

    def set_num_nodes(self, num_nodes):
        self.num_nodes = num_nodes

    def set_node_color(self, color):
        self.node_color = color

    def set_node_size(self, size):
        self.node_size = size

    def set_network_dimensions(self, dimX, dimY, dimZ):
        self.dimX = dimX
        self.dimY = dimY
        self.dimZ = dimZ

    def set_network_parameters(self, params):
        self.network_parameters = params

    def set_distribution_model(self, model):
        self.distribution_model = model

    def set_distribution_model_parameters(self, params):
        self.distribution_model_parameters = params

    def set_mobility_model(self, model):
        self.mobility_model = model

    def set_mobility_model_parameters(self, params):
        self.mobility_model_parameters = params

    def set_node(self, node):
        self.node = node

    def set_connectivity_model(self, model):
        self.connectivity_model = model

    def set_connectivity_model_parameters(self, params):
        self.connectivity_model_parameters = params

    def set_message_transmission_model(self, model):
        self.message_transmission_model = model

    def set_message_transmission_model_parameters(self, params):
        self.message_transmission_model_parameters = params

    def set_reliability_model(self, model):
        self.reliability_model = model

    def set_reliability_model_parameters(self, params):
        self.reliability_model_parameters = params

    def set_interference_model(self, model):
        self.interference_model = model

    def set_interference_model_parameters(self, params):
        self.interference_model_parameters = params

    def set_message_protocol(self, protocol):
        self.message_protocol = protocol

    def set_verbose_logging(self, verbose):
        self.verbose_logging = verbose

    def set_asynchronous(self, async_mode):
        self.asynchronous = async_mode

    def print_config(self):
        print("Simulation Configuration:")
        print(f"Simulation Name: {self.simulation_name}")
        print(f"Simulation Rounds: {self.simulation_rounds}")
        print(f"Simulation Refresh Rate: {self.simulation_refresh_rate}")
        print(f"Nack Messages Enabled: {self.nack_messages_enabled}")
        print(f"Number of Nodes: {self.num_nodes}")
        print(f"Network Dimensions: {self.dimX} x {self.dimY} x {self.dimZ}")
        print(f"Network Parameters: {self.network_parameters}")
        print(f"Node: {self.node}")
        print(f"Distribution Model: {self.distribution_model}")
        print(
            f"Distribution Model Parameters: {self.distribution_model_parameters}")
        print(f"Mobility Model: {self.mobility_model}")
        print(f"Mobility Model Parameters: {self.mobility_model_parameters}")
        print(f"Connectivity Model: {self.connectivity_model}")
        print(
            f"Connectivity Model Parameters: {self.connectivity_model_parameters}")
        print(f"Message Transmission Model: {self.message_transmission_model}")
        print(
            f"Message Transmission Model Parameters: {self.message_transmission_model_parameters}")
        print(f"Reliability Model: {self.reliability_model}")
        print(
            f"Reliability Model Parameters: {self.reliability_model_parameters}")
        print(f"Interference Model: {self.interference_model}")
        print(
            f"Interference Model Parameters: {self.interference_model_parameters}")
        print(f"Message Protocol: {self.message_protocol}")
        print(f"Verbose Logging: {self.verbose_logging}")
        print(f"Asynchronous: {self.asynchronous}")
        print(f"Node Color: {self.node_color}")


config = SimulationConfig()
