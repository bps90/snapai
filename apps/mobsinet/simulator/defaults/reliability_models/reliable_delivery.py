from apps.mobsinet.simulator.models.nodes.abc_packet import AbcPacket
from ...models.abc_reliability_model import AbcReliabilityModel


class ReliableDelivery(AbcReliabilityModel):

    def __init__(self):
        super().__init__('ReliableDelivery')

    def reaches_destination(self, packet: AbcPacket):
        return True


model = ReliableDelivery
