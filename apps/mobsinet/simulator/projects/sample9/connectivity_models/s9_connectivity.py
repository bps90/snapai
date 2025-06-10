from ....models.abc_connectivity_model import AbcConnectivityModel
from ..nodes.s9_node import S9Node
import random


class S9Connectivity(AbcConnectivityModel):

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass

    def is_connected(self, node_a, node_b):
        if (not isinstance(node_a, S9Node) or not isinstance(node_b, S9Node)):
            return False

        a_channels = set(node_a.comm_channels)
        b_channels = set(node_b.comm_channels)

        if (a_channels.isdisjoint(b_channels)):
            return False

        # Check distance for VHF radio distance
        if (node_a.position.euclidean_distance(node_b.position) <= random.random() * 69000 + 5000):
            return True

        # if (node_a.position.euclidean_distance(node_b.position) <= 2000):
        #     return True

        return False


model = S9Connectivity
