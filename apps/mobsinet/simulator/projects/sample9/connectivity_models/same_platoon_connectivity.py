from ....models.abc_connectivity_model import AbcConnectivityModel
from ..nodes.s9_node import S9Node


class SamePlatoonConnectivity(AbcConnectivityModel):
    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass

    def is_connected(self, node_a, node_b) -> bool:
        """Check if the nodes are connected.

        Parameters
        ----------
        node_a : AbcNode
            The first node.
        node_b : AbcNode
            The second node.
        """
        if (not isinstance(node_a, S9Node) or not isinstance(node_b, S9Node)):
            return False
        return node_a.platoon_id == node_b.platoon_id


model = SamePlatoonConnectivity
