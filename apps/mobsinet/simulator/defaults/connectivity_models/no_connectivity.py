from apps.mobsinet.simulator.models.nodes.abc_node_implementation import AbcNodeImplementation
from ...models.abc_connectivity_model import AbcConnectivityModel


class NoConnectivity(AbcConnectivityModel):
    def __init__(self):
        super().__init__('NoConnectivity')

    def is_connected(self, node_a: AbcNodeImplementation, node_b: AbcNodeImplementation) -> bool:
        """Check if the nodes are connected."""
        return False


model = NoConnectivity
