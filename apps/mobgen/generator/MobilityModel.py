from abc import abstractmethod, ABC
from .Node import Node
from typing import List
from .Position import Position
from .Scenario import Scenario

class MobilityModel(ABC):
    def __init__(self, nodes: List[Node], scenario: Scenario):
        self.nodes = nodes
        self.scenario = scenario
        self._initednodes = False
        self._initNodes()
        self._initednodes = True

    @abstractmethod
    def getNextPosition(self, node: Node) -> Position:
        pass

    @abstractmethod
    def _initNodes(self) -> None:
        pass