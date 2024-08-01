from abc import abstractmethod

from apps.mobsinet.simulator.models.nodes.abc_node_behavior import AbcNodeBehavior
from .abc_model import AbcModel


class AbcConnectivityModel(AbcModel):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def is_connected(self, node_a: AbcNodeBehavior, node_b: AbcNodeBehavior) -> bool:
        """Check if the nodes are connected."""
        pass
