from .event import Event
from ..models.nodes.packet import Packet
from .inbox import Inbox
from .nack_box import NackBox
from ..configuration.sim_config import SimulationConfig
from ..network_simulator import simulation
from .packet_type import PacketType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.nodes.abc_node import AbcNode


class PacketEvent(Event):
    def __init__(self, packet: Packet, time: float):
        super().__init__(time)
        self.packet: Packet = packet
        self.inbox = Inbox(packet)
        self.nack_box = NackBox(packet)

    @classmethod
    def get_new_packet_event(cls, packet: Packet, time: float) -> 'PacketEvent':
        pe = PacketEvent(packet, time)

        return pe

    def handle(self):
        if SimulationConfig.interference_enabled:  # There is interference
            simulation.packets_in_the_air.perform_interference_test_before_remove()
            simulation.packets_in_the_air.remove(self.packet)
        if (simulation.has_edge(self.packet.origin, self.packet.destination)):
            simulation.graph.edges[self.packet.origin,
                                   self.packet.destination]['number_of_packets'] += 1
        if self.packet.positive_delivery:
            self.packet.destination.handle_messages(
                self.inbox.reset_for_packet(self.packet))
        else:
            if SimulationConfig.nack_messages_enabled and self.packet.type == PacketType['UNICAST']:
                self.packet.origin.handle_nack_messages(
                    self.nack_box.reset_for_packet(self.packet))

    def drop(self):
        if SimulationConfig.interference_enabled:  # There is interference
            simulation.packets_in_the_air.remove(self.packet)
        if (simulation.has_edge(self.packet.origin, self.packet.destination)):
            simulation.graph.edges[self.packet.origin,
                                   self.packet.destination]['number_of_packets'] -= 1

    def __str__(self):
        return "PacketEvent"

    def get_event_list_text(self, has_executed: bool) -> str:
        if has_executed:
            return f"Packet at node {self.packet.destination.id} {'(delivered)' if self.packet.positive_delivery else '(dropped)'}"
        else:
            return f"PE (Node:{self.packet.destination.id}, Time:{self.get_execution_time_string(4)})"

    def get_event_list_tooltip_text(self, has_executed: bool) -> str:
        msg_type = self.packet.message.__class__.__name__
        if has_executed:
            return f"The type of the message is: {msg_type}\n" + ("The message was delivered" if self.packet.positive_delivery else "The message was dropped.")
        else:
            return (f"At time {self.time} a message reaches node {self.packet.destination.id}\n"
                    f"The type of the message is: {msg_type}\n" +
                    ("Until now it seems that the message will reach its destination."
                     if self.packet.positive_delivery else
                     "The message has already been disturbed and will not reach its destination."))

    def get_event_node(self) -> 'AbcNode':
        return self.packet.destination

    def is_node_event(self) -> bool:
        return True
