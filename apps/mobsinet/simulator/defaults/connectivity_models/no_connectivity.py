from typing import TYPE_CHECKING
from ...models.abc_connectivity_model import AbcConnectivityModel

if TYPE_CHECKING:
    from ...models.nodes.abc_node_implementation import AbcNodeImplementation


class NoConnectivity(AbcConnectivityModel):
    def __init__(self):
        super().__init__('NoConnectivity')

    def is_connected(self, node_a: 'AbcNodeImplementation', node_b: 'AbcNodeImplementation') -> bool:
        """Check if the nodes are connected."""
        return False


model = NoConnectivity
