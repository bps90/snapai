from abc import ABC, abstractmethod

from apps.mobsinet.simulator.models.nodes.abc_message import AbcMessage


class AbcPacket(ABC):

    def __init__(self, message: AbcMessage = None):
        self.message: AbcMessage = message
        self.positiveDelivery: bool = True

        pass

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
