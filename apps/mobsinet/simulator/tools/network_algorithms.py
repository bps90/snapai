from ..network_simulator import simulation
from networkx.algorithms import all_pairs_node_connectivity


class NetworkAlgorithms:
    @staticmethod
    def compute_connectivity_path_length_to_all_pairs():
        return all_pairs_node_connectivity(simulation.graph)

    @staticmethod
    def round_algorithms():
        return NetworkAlgorithms.compute_connectivity_path_length_to_all_pairs()
