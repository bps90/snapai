from .s9_node import S9Node
from ....tools.color import Color
import random


class IntruderNode(S9Node):
    def __init__(self, id, position, mobility_model, connectivity_model, interference_model, reliability_model, qty_channels=None):
        super().__init__(id, 0, 0, '', 'intruder', '', '', [],
                         position, mobility_model, connectivity_model, interference_model, reliability_model)
        self.node_color = Color(255, 255, 0)

        qty_channels = qty_channels if qty_channels is not None else random.randint(
            2, 5)
        for i in range(qty_channels):
            random_channel = str(random.randint(1, 35))

            self.comm_channels.append(random_channel)
        self.comm_channels.append('0')


node = IntruderNode
