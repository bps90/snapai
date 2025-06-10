from abc import ABC
from copy import deepcopy
from typing import Optional


class AbcMessage(ABC):
    def __init__(self):
        self.content: Optional[str] = None

    def __str__(self):
        return self.content

    def clone(self):
        """Create a copy of the object.

        Returns
        -------
        AbcMessage
            A copy of the object.
        """

        return deepcopy(self)
