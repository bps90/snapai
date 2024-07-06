from ..Scenario import Scenario

class TwoDimensionalScenario(Scenario):
    def __init__(self, size: tuple[int, int]):
        self.dimensions = 2
        self.size = (size[0], size[1], 0)