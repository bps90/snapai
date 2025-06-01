# GENERATED WITH HELP FROM CHATGPT

from ..models.nodes.packet import Packet
from typing import Union


class Inbox:
    def __init__(self, packets: Union['Packet', list['Packet']] = None):
        """
        Initializes the inbox with either a list of packets or a single packet.
        """
        self.packet_list: list['Packet'] = None
        self.active_packet: 'Packet' = None
        self.single_packet: 'Packet' = None
        self.reset_for_list(packets) if type(
            packets) is list else self.reset_for_packet(packets)

    def reset(self):
        """
        Resets the state of this Inbox.
        """
        if self.packet_list:
            self.reset_for_list(self.packet_list)
        else:
            self.reset_for_packet(self.single_packet)

    def size(self):
        """
        Returns the number of messages held in this inbox.
        """
        if self.packet_list:
            return len(self.packet_list)
        elif self.single_packet:
            return 1
        else:
            return 0

    # Meta information about the last packet returned by next()
    def get_sender(self):
        """
        Returns the sender of the message of the active packet.
        """
        if self.active_packet:
            return self.active_packet.origin
        else:
            raise ValueError("No active packet to get the sender from.")

    def get_receiver(self):
        """
        Returns the receiver of the message of the active packet.
        """
        if self.active_packet:
            return self.active_packet.destination
        else:
            raise ValueError("No active packet to get the receiver from.")

    def get_arriving_time(self):
        """
        Returns the time when the message arrived.
        """
        if self.active_packet:
            return self.active_packet.arriving_time
        else:
            raise ValueError("No active packet to get arriving time from.")

    def get_intensity(self):
        """
        Returns the intensity of the message.
        """
        if self.active_packet:
            return self.active_packet.intensity
        else:
            raise ValueError("No active packet to get intensity from.")

    def get_sending_time(self):
        """
        Returns the time the message was sent.
        """
        if self.active_packet:
            return self.active_packet.sending_time
        else:
            raise ValueError("No active packet to get sending time from.")

    # Internal methods

    def reset_for_list(self, packet_list):
        """
        Resets this inbox to contain the given list of packets.
        """
        self.packet_list = packet_list
        self.active_packet = None
        self.single_packet = None
        return self

    def reset_for_packet(self, packet):
        """
        Resets the inbox to contain a single packet.
        """
        self.packet_list = None
        self.active_packet = None
        self.single_packet = packet
        return self

    def free_packets(self):
        """
        Frees all packets in the inbox.
        """
        self.active_packet = None
        self.single_packet = None

        if self.packet_list:
            self.packet_list.clear()
