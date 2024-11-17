from abc import abstractmethod

from .nodes.packet import Packet
from .abc_model import AbcModel


class AbcReliabilityModel(AbcModel):

    @abstractmethod
    def reaches_destination(self, packet: Packet) -> bool:
        """Determines if the packet will reach the destination.

        Parameters
        ----------
        packet : Packet
            The packet object.

        Returns
        -------
        bool
            `True` if the packet will reach the destination, `False` otherwise.
        """

        pass
