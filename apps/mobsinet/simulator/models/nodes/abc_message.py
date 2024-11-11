from abc import ABC, abstractmethod


class AbcMessage(ABC):
    def __init__(self):
        self.content: str = None

    def __str__(self):
        return self.content

    @abstractmethod
    def clone(self):
        """Create a copy of the object.

        Returns
        -------
        AbcMessage
            A copy of the object.
        """
        # TODO: implement
        pass
