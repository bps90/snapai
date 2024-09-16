from copy import copy, deepcopy
from apps.mobsinet.simulator.models.nodes.abc_message import AbcMessage


class NoContentMessage(AbcMessage):
    def __init__(self):
        self.content = None

    def clone(self):
        return deepcopy(self)


message = NoContentMessage
