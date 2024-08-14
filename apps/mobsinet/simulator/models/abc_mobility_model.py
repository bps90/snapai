from abc import abstractmethod


from ..tools.position import Position
from .abc_model import AbcModel


class AbcMobilityModel(AbcModel):

    def __init__(self, name: str):
        super().__init__(name)

    @abstractmethod
    def get_next_position(self, node_implementation) -> Position:
        """(abstract) This method should return the next position for the node.

        Parameters
        ----------
        node_implementation : AbcNodeImplementation
            The node implementation object.
        """

        pass
