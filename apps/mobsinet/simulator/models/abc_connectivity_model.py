from abc import abstractmethod

from .abc_model import AbcModel


class AbcConnectivityModel(AbcModel):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def is_connected(self, node_a, node_b) -> bool:
        """Check if the nodes are connected.

        Parameters
        ----------
        node_a : AbcNode
            The first node.
        node_b : AbcNode
            The second node.
        """
        pass
