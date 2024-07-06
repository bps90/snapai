from abc import ABC, abstractmethod
from ..tools.position import Position

class AbcDistributionModel(ABC):

    def __init__(self) -> None:
        super().__init__()
    
    
    @abstractmethod
    def get_next_position(self) -> Position:
        pass