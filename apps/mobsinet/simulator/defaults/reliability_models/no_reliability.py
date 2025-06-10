from ...models.nodes.packet import Packet
from ...models.abc_reliability_model import AbcReliabilityModel


class NoReliability(AbcReliabilityModel):

    def reaches_destination(self, packet: Packet):
        """Determines if the packet will reach the destination.
        In this model, the packet will never reach the destination.

        Parameters
        ----------
        packet : AbcPacket
            The packet object.

        Returns
        -------
        bool
            `False` everywhere.
        """

        return False

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass


model = NoReliability
