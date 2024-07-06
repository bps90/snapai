from abc import ABC

class Scenario(ABC):
    def __init__(self):
        self.dimensions: int
        self.size: tuple[int, int, int]
