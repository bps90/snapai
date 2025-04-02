from typing import TYPE_CHECKING
from ...models.abc_connectivity_model import AbcConnectivityModel

if TYPE_CHECKING:
    from ...models.nodes.abc_node import AbcNode


class NoConnectivity(AbcConnectivityModel):
    def __init__(self):
        super().__init__('NoConnectivity')

    def is_connected(self, node_a: 'AbcNode', node_b: 'AbcNode') -> bool:
        """Check if the nodes are connected."""
        return False


model = NoConnectivity
