from abc import abstractmethod

from ..models.nodes.abc_node_behavior import AbcNodeBehavior
from ..tools.position import Position
from .abc_model import AbcModel


class AbcDistributionModel(AbcModel):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def get_position(self) -> Position:
        """(abstract) This method should return a Position object that 
        represents the first position of the node."""

        pass
