from ....models.abc_connectivity_model import AbcConnectivityModel
from ..nodes.s9_node import S9Node


class SameCompanyConnectivity(AbcConnectivityModel):
    def __init__(self):
        super().__init__('SameCompanyConnectivity')

    def is_connected(self, node_a: 'S9Node', node_b: 'S9Node') -> bool:
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
        return node_a.company_id == node_b.company_id


model = SameCompanyConnectivity
