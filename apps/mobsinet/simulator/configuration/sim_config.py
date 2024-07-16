import json

class SimulationConfig:
    def __init__(self, config_file=None):
        # Default values
        self.PROJECT_DIR = "apps/mobsinet/simulator/defaults/"
        self.simulation_name = "Network Simulation"
        self.simulation_steps = 1000
        self.num_nodes = 50
        self.dimX = 100
        self.dimY = 100
        self.dimZ = 100
        self.network_parameters = {
            'type': 'random_graph',
            'avg_degree': 4
        }
        self.node_behavior = 'inert_node_behavior'
        self.distribution_model = 'random_dist'
        self.mobility_model = 'random_mob'
        self.connectivity_model = 'no_connectivity'
        self.reliability_model = 'no_reliability'
        self.interference_model = 'no_interference'
        self.message_protocol = 'TCP'
        self.verbose_logging = False
        
        if config_file:
            self.load_from_file(config_file)

    def load_from_file(self, config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        self.set_simulation_name(config_data.get('simulation_name', self.simulation_name))
        self.set_simulation_steps(config_data.get('simulation_steps', self.simulation_steps))
        self.set_num_nodes(config_data.get('num_nodes', self.num_nodes))
        self.set_network_dimensions(config_data.get('dimX', self.dimX),
                                    config_data.get('dimY', self.dimY),
                                    config_data.get('dimZ', self.dimZ))
        self.set_network_parameters(config_data.get('network_parameters', self.network_parameters))
        self.set_mobility_model(config_data.get('mobility_model', self.mobility_model))
        self.set_message_protocol(config_data.get('message_protocol', self.message_protocol))
        self.set_verbose_logging(config_data.get('verbose_logging', self.verbose_logging))

    def set_project_dir(self, dirname):
        self.PROJECT_DIR = dirname 
    
    def set_simulation_name(self, name):
        self.simulation_name = name

    def set_simulation_steps(self, steps):
        self.simulation_steps = steps

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

    def set_message_protocol(self, protocol):
        self.message_protocol = protocol

    def set_verbose_logging(self, verbose):
        self.verbose_logging = verbose

    def get_project_dir(self):
        return self.PROJECT_DIR

    def get_simulation_name(self):
        return self.simulation_name

    def get_simulation_steps(self):
        return self.simulation_steps

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

    def get_message_protocol(self):
        return self.message_protocol

    def get_verbose_logging(self):
        return self.verbose_logging

    def print_config(self):
        print(f"Simulation Name: {self.get_simulation_name()}")
        print(f"Simulation Steps: {self.get_simulation_steps()}")
        print(f"Number of Nodes: {self.get_num_nodes()}")
        print(f"Network Dimensions (dimX, dimY, dimZ): {self.get_network_dimensions()}")
        print(f"Network Parameters: {self.get_network_parameters()}")
        print(f"Distribution Model: {self.get_distribution_model()}")
        print(f"Mobility Model: {self.get_mobility_model()}")
        print(f"Message Protocol: {self.get_message_protocol()}")
        print(f"Verbose Logging: {self.get_verbose_logging()}")


sim_config_env = SimulationConfig()

#usage
if __name__ == "__main__":
    # Example usage:
    config_file_path = 'apps/mobsinet/simulator/configuration/simulation_config.json'
    # Example JSON content in simulation_config.json:
    # {
    #     "simulation_name": "My Network Simulation",
    #     "simulation_steps": 2000,
    #     "num_nodes": 100,
    #     "dimX": 200,
    #     "dimY": 200,
    #     "dimZ": 100,
    #     "network_parameters": {"type": "random_graph", "avg_degree": 6}
    # }
    config = SimulationConfig(config_file_path)
    config.print_config()
