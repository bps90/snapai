from abc import ABC


class AbcMessage(ABC):
    def __init__(self):
        self.content: str = None

    def __str__(self):
        return self.content
