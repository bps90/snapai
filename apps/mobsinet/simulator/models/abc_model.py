from abc import ABC

class AbcModel(ABC):

    def __init__(self, name: str):
        self.name = name