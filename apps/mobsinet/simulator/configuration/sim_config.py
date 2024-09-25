import json
from math import pi, sqrt


class SimulationConfig:
    def __init__(self, config_file=None):
        # Default values
        self.PROJECT_DIR = "apps/mobsinet/simulator/defaults/"
        self.simulation_name = "Network Simulation"
        self.simulation_rounds = 1000
        self.num_nodes = 50
        self.dimX = 100
        self.dimY = 100
        self.dimZ = 100
        self.network_parameters = {
            'type': 'random_graph',
            'avg_degree': 4
        }
        self.node_implementation = 'inert_node_implementation'
        self.distribution_model = 'random_dist'
        self.distribution_model_parameters = {
            'orientation': 'horizontal',  # 'horizontal' or 'vertical'
            'line_position': None,
            'number_of_nodes': None,
            'midpoint': (self.dimX / 2, self.dimY / 2),
            'rotation_direction': 'anti-clockwise',
            'radius': None,
        }
        self.mobility_model = 'random_mob'
        self.mobility_model_parameters = {
            # TODO: maybe turn it dependent by the specific mobility model
            'speed_range': [0, sqrt(self.dimX**2 + self.dimY**2)],
            'direction_range': [0, 2 * pi],
            'prioritize_speed': False,
            'travel_distance': None,
            'travel_time': self.simulation_rounds * 0.1  # 10% of the simulation time
        }
        self.connectivity_model = 'no_connectivity'
        self.connectivity_model_parameters = {
            'max_radius': None,
            'min_radius': None,
            'big_radius_probability': None
        }
        self.message_transmission_model_parameters = {
            'constant_transmission_time': 1,
            'random_transmission_min_time': 1,
            'random_transmission_max_time': 10
        }
        self.reliability_model = 'no_reliability'
        self.interference_model = 'no_interference'
        self.message_protocol = 'TCP'
        self.verbose_logging = False

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
        self.set_num_nodes(config_data.get('num_nodes', self.num_nodes))
        self.set_network_dimensions(config_data.get('dimX', self.dimX),
                                    config_data.get('dimY', self.dimY),
                                    config_data.get('dimZ', self.dimZ))
        self.set_network_parameters(config_data.get(
            'network_parameters', self.network_parameters))
        self.set_distribution_model(config_data.get(
            'distribution_model', self.distribution_model))
        self.set_node_implementation(config_data.get(
            'node_implementation', self.node_implementation))
        self.set_connectivity_model(config_data.get(
            'connectivity_model', self.connectivity_model))
        self.set_reliability_model(config_data.get(
            'reliability_model', self.reliability_model))
        self.set_interference_model(config_data.get(
            'interference_model', self.interference_model))
        self.set_mobility_model(config_data.get(
            'mobility_model', self.mobility_model))
        self.set_message_protocol(config_data.get(
            'message_protocol', self.message_protocol))
        self.set_verbose_logging(config_data.get(
            'verbose_logging', self.verbose_logging))

    def set_project_dir(self, dirname):
        self.PROJECT_DIR = dirname

    def set_simulation_name(self, name):
        self.simulation_name = name

    def set_simulation_rounds(self, rounds):
        self.simulation_rounds = rounds

    def set_num_nodes(self, num_nodes):
        self.num_nodes = num_nodes

    def set_network_dimensions(self, dimX, dimY, dimZ):
        self.dimX = dimX
        self.dimY = dimY
        self.dimZ = dimZ

    def set_network_parameters(self, params):
        self.network_parameters = params

    def set_distribution_model(self, model):
        self.distribution_model = model

    def set_mobility_model(self, model):
        self.mobility_model = model

    def set_node_implementation(self, implementation):
        self.node_implementation = implementation

    def set_connectivity_model(self, model):
        self.connectivity_model = model

    def set_reliability_model(self, model):
        self.reliability_model = model

    def set_interference_model(self, model):
        self.interference_model = model

    def set_message_protocol(self, protocol):
        self.message_protocol = protocol

    def set_verbose_logging(self, verbose):
        self.verbose_logging = verbose

    def get_project_dir(self):
        return self.PROJECT_DIR

    def get_simulation_name(self):
        return self.simulation_name

    def get_simulation_rounds(self):
        return self.simulation_rounds

    def get_num_nodes(self):
        return self.num_nodes

    def get_network_dimensions(self):
        return self.dimX, self.dimY, self.dimZ

    def get_network_parameters(self):
        return self.network_parameters

    def get_distribution_model(self):
        return self.distribution_model

    def get_mobility_model(self):
        return self.mobility_model

    def get_node_implementation(self):
        return self.node_implementation

    def get_connectivity_model(self):
        return self.connectivity_model

    def get_reliability_model(self):
        return self.reliability_model

    def get_interference_model(self):
        return self.interference_model

    def get_message_protocol(self):
        return self.message_protocol

    def get_verbose_logging(self):
        return self.verbose_logging

    def print_config(self):
        print(f"Simulation Name: {self.get_simulation_name()}")
        print(f"Simulation Rounds: {self.get_simulation_rounds()}")
        print(f"Number of Nodes: {self.get_num_nodes()}")
        print(
            f"Network Dimensions(dimX, dimY, dimZ): {self.get_network_dimensions()}")
        print(f"Network Parameters: {self.get_network_parameters()}")
        print(f"Distribution Model: {self.get_distribution_model()}")
        print(f"Mobility Model: {self.get_mobility_model()}")
        print(f"Node Implementation: {self.get_node_implementation()}")
        print(f"Connectivity Model: {self.get_connectivity_model()}")
        print(f"Reliability Model: {self.get_reliability_model()}")
        print(f"Interference Model: {self.get_interference_model()}")
        print(f"Message Protocol: {self.get_message_protocol()}")
        print(f"Verbose Logging: {self.get_verbose_logging()}")


config_file_path = 'apps/mobsinet/simulator/configuration/simulation_config.json'
sim_config_env = SimulationConfig(config_file_path)

# usage
if __name__ == "__main__":
    # Example usage:
    config_file_path = 'apps/mobsinet/simulator/configuration/simulation_config.json'
    # Example JSON content in simulation_config.json:
    # {
    #     "simulation_name": "My Network Simulation",
    #     "simulation_rounds": 2000,
    #     "num_nodes": 100,
    #     "dimX": 200,
    #     "dimY": 200,
    #     "dimZ": 100,
    #     "network_parameters": {"type": "random_graph", "avg_degree": 6}
    # }
    config = SimulationConfig(config_file_path)
    config.print_config()
