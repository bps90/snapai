from typing import TYPE_CHECKING
from .abc_message import AbcMessage
from typing import Literal

if TYPE_CHECKING:
    from .abc_node import AbcNode



class Packet:
    
    def __init__(self, message: 'AbcMessage'):
        self.message = message
        self.origin: 'AbcNode' 
        self.destination: 'AbcNode' 
        self.type: Literal["UNICAST", "MULTICAST", "DUMMY"]
        self.positive_delivery: bool 
        self.arriving_time: int = 0
        self.sending_time: int = 0
        self.intensity: float = 0
        

    def set_message(self, message: 'AbcMessage'):
        self.message = message

    def deny_delivery(self):
        """Deny the delivery of the packet."""

        self.positive_delivery = False

