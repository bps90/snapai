from ..Scenario import Scenario

class ThreeDimensionalScenario(Scenario):
    def __init__(self, size: tuple[int, int, int]):
        self.dimensions = 3
        self.size = size