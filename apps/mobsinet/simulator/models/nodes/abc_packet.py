from abc import ABC, abstractmethod

from apps.mobsinet.simulator.models.nodes.abc_message import AbcMessage
from apps.mobsinet.simulator.models.nodes.abc_node_implementation import AbcNodeImplementation


class AbcPacket(ABC):

    def __init__(self,
                 message: AbcMessage,
                 origin: AbcNodeImplementation,
                 destination: AbcNodeImplementation):
        self.message = message
        self.origin = origin
        self.destination = destination
        self.positiveDelivery: bool = True

    def set_message(self, message: AbcMessage):
        self.message = message

    def denyDelivery(self):
        """Deny the delivery of the packet."""

        self.positiveDelivery = False

    @abstractmethod
    def clone(self):
        """Create a copy of the object.

        Returns
        -------
        AbcPacket
            A copy of the object.
        """
        pass
