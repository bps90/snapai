# GENERATED WITH HELP FROM CHATGPT

from ..models.nodes.packet import Packet


class Inbox:
    def __init__(self, packet_list: list['Packet']=None, single_packet: 'Packet' =None):
        """
        Initializes the inbox with either a list of packets or a single packet.
        """
        self.packet_list = packet_list if packet_list is not None else []
        self.single_packet = single_packet
        self.active_packet: 'Packet' = None
        self.packet_iter = iter(self.packet_list) if self.packet_list else None

    def remove(self):
        """
        Removes the message that was returned by the last call to next().
        """
        self.active_packet = None
        if self.packet_iter:
            # Python iterators don't have a direct remove, so we manipulate the list instead
            self.packet_list.remove(self.active_packet)
            self.packet_iter = iter(self.packet_list)
        else:
            self.single_packet = None

    def reset(self):
        """
        Resets the state of this iterator.
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
        Returns the sender of the message returned by the last call to next().
        """
        if self.active_packet:
            return self.active_packet.origin
        else:
            raise ValueError("No active packet to get the sender from.")

    def get_receiver(self):
        """
        Returns the receiver of the message returned by the last call to next().
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

    def get_incoming_edge(self):
        """
        Returns the edge over which the current message was received.
        """
        if self.active_packet:
            return self.active_packet.edge
        else:
            raise ValueError("No active packet to get incoming edge from.")

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
        self.packet_iter = None
        self.single_packet = packet
        return self

    def free_packets(self):
        """
        Frees all packets in the inbox, making them available for reuse.
        """
        self.active_packet = None
        if self.packet_list:
            for packet in self.packet_list:
                Packet.free(packet)
            self.packet_list.clear()
        else:
            if self.single_packet:
                Packet.free(self.single_packet)
                self.single_packet = None
