import threading
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .abc_message import AbcMessage

if TYPE_CHECKING:
    from .abc_node import AbcNode


class Packet(ABC):
    
    def __init__(self,
                 message: 'AbcMessage',
                 origin: 'AbcNode',
                 destination: 'AbcNode',
                 type: str):
        self.message = message
        self.origin = origin
        self.destination = destination
        self.type = type
        # self.edge: 'EdgeImplementation' = None
        self.positive_delivery: bool = True
        self.arriving_time: int = 0
        self.sending_time: int = 0
        
        Packet.issued_packets.add(self)
        Packet.num_packets_on_the_fly += 1

    def set_message(self, message: 'AbcMessage'):
        self.message = message

    def denyDelivery(self):
        """Deny the delivery of the packet."""

        self.positive_delivery = False

    @abstractmethod
    def clone(self):
        """Create a copy of the object.

        Returns
        -------
        AbcPacket
            A copy of the object.
        """
        # TODO: implement
        pass
