from ..models.nodes.abc_packet import AbcPacket
from ..network_simulator import simulation


class InboxPacketBuffer(list['AbcPacket']):

    def __init__(self):
        self.arriving_packets: list['AbcPacket'] = []

    def update_message_buffer(self):
        self.arriving_packets.clear()

        for packet in self:
            if (packet.arriving_time <= simulation.global_time):
                simulation.packets_in_the_air.remove(packet)

                self.remove(packet)

                if (packet.positive_delivery):
                    self.arriving_packets.append(packet)
                else:
                    # TODO: implement nack
                    # packet.origin.add_nack_packet(packet)
                    pass
