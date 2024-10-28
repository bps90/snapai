from ..models.nodes.packet import Packet


class PacketsInTheAirBuffer(object):
    def __init__(self) -> None:
        self.active_packets: list[Packet] = []
        self.passive_packets: list[Packet] = []

    def test_interference(self):
        for packet in self.active_packets:
            self.__check_positive_delivery(packet)

        for packet in self.passive_packets:
            self.__check_positive_delivery(packet)

    def __check_positive_delivery(self, packet: Packet):
        if packet.positive_delivery:
            packet.positive_delivery = not packet.destination.interference_model.is_disturbed(
                packet)

    def remove(self, packet: Packet):
        try:
            self.active_packets.remove(packet)
        except ValueError:
            self.passive_packets.remove(packet)
