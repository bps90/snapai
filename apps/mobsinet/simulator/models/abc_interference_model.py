from abc import abstractmethod

from .nodes.packet import Packet
from .abc_model import AbcModel


class AbcInterferenceModel(AbcModel):

    @abstractmethod
    def is_disturbed(self, packet: Packet) -> bool:
        """Checks if the interference model dirtubed the packet.

        Parameters
        ----------
        packet : AbcPacket
            The packet to check.

        Returns
        -------
        bool
            True if the interference model dirtubed the packet, False otherwise.

        """

