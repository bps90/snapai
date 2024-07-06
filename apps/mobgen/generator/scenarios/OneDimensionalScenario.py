from ..Scenario import Scenario

class OneDimensionalScenario(Scenario):
    def __init__(self, size: tuple[int]):
        self.dimensions = 1
        self.size = (size[0], 0, 0)