from abc import abstractmethod

from .nodes.abc_packet import AbcPacket
from .abc_model import AbcModel


class AbcReliabilityModel(AbcModel):

    @abstractmethod
    def reaches_destination(self, packet: AbcPacket) -> bool:
        """Determines if the packet will reach the destination.

        Parameters
        ----------
        packet : AbcPacket
            The packet object.

        Returns
        -------
        bool
            `True` if the packet will reach the destination, `False` otherwise.
        """

        pass
