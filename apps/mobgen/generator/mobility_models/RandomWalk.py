from ..MobilityModel import MobilityModel
from ..Position import Position
from ..Node import Node
from random import random


class RandomWalk(MobilityModel):

    def getNextPosition(self, _: Node):
        return Position(*self.__genRandomPoint())

    def _initNodes(self):
        if (self._initednodes): return

        for node in self.nodes:
            node.initNode(*self.__genRandomPoint())

        self._initednodes = True
    
    def __genRandomPoint(self) -> tuple[float, float, float]:
        return (random() * self.scenario.size[0], random() * self.scenario.size[1], random() * self.scenario.size[2])
