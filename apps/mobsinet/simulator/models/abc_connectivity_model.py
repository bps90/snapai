from abc import abstractmethod

from apps.mobsinet.simulator.models.nodes.abc_node_implementation import AbcNodeImplementation
from .abc_model import AbcModel


class AbcConnectivityModel(AbcModel):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def is_connected(self, node_a: AbcNodeImplementation, node_b: AbcNodeImplementation) -> bool:
        """Check if the nodes are connected."""
        pass
