from apps.mobsinet.simulator.models.nodes.abc_packet import AbcPacket
from ...models.abc_reliability_model import AbcReliabilityModel


class NoReliability(AbcReliabilityModel):

    def __init__(self):
        super().__init__('NoReliability')

    def reaches_destination(self, packet: AbcPacket):
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


model = NoReliability
