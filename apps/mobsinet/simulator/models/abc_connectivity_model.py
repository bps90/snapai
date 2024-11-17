from abc import abstractmethod
from typing import  TYPE_CHECKING
from .abc_model import AbcModel

if (TYPE_CHECKING):
    from .nodes.abc_node import AbcNode

class AbcConnectivityModel(AbcModel):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def is_connected(self, node_a: 'AbcNode', node_b: 'AbcNode') -> bool:
        """Check if the nodes are connected.

        Parameters
        ----------
        node_a : AbcNode
            The first node.
        node_b : AbcNode
            The second node.
        """
        pass
