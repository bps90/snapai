from abc import ABC

from apps.mobsinet.simulator.models.nodes.abc_message import AbcMessage


class AbcPacket(ABC):

    def __init__(self, message: AbcMessage = None):
        self.message: AbcMessage = message
        self.positiveDelivery: bool = True

        pass

    def set_message(self, message: AbcMessage):
        self.message = message

    def denyDelivery(self):
        self.positiveDelivery = False
