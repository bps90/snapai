from abc import abstractmethod

from ..tools.position import Position
from .abc_model import AbcModel
from typing import Any


class AbcDistributionModel(AbcModel):
    @abstractmethod
    def get_position(self) -> Position:
        """(abstract) This method should return a Position object that 
        represents the first position of the node."""
