from ...models.nodes.packet import Packet
from ...models.abc_reliability_model import AbcReliabilityModel


class ReliableDelivery(AbcReliabilityModel):

    def __init__(self):
        super().__init__('ReliableDelivery')

    def reaches_destination(self, packet: Packet):
        """Determines if the packet will reach the destination.
        In this model, the packet will always reach the destination.

        Parameters
        ----------
        packet : AbcPacket
            The packet object.

        Returns
        -------
        bool
            `True` everywhere.
        """

        return True


model = ReliableDelivery
