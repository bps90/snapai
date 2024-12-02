from abc import ABC
from copy import deepcopy

class AbcModel(ABC):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'{self.__class__.__name__}: {self.name}'
    
    def clone(self):
        return deepcopy(self)