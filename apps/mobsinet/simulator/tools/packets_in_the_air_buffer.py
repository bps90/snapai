from apps.mobsinet.simulator.models.nodes.abc_packet import AbcPacket


class PacketsInTheAirBuffer(object):
    def __init__(self) -> None:
        self.active_packets: list[AbcPacket] = []
        self.passive_packets: list[AbcPacket] = []

    def test_interference(self):
        for packet in self.active_packets:
            self.__check_positive_delivery(packet)

        for packet in self.passive_packets:
            self.__check_positive_delivery(packet)

    def __check_positive_delivery(self, packet: AbcPacket):
        if packet.positiveDelivery:
            packet.positiveDelivery = not packet.destination.interference_model.is_disturbed(
                packet)
