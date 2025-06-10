from .s9_node import S9Node
from ....tools.color import Color


class LogisticsNode(S9Node):
    def __init__(self,
                 id,
                 company_id,
                 platoon_id,
                 platoon_type,
                 function,
                 type,
                 command,
                 comm_channels,
                 position,
                 mobility_model,
                 connectivity_model,
                 interference_model,
                 reliability_model):
        super().__init__(id, company_id, platoon_id, platoon_type, function, type, command, comm_channels,
                         position, mobility_model, connectivity_model, interference_model, reliability_model)
        self.node_color = Color(0, 255, 47)


node = LogisticsNode
