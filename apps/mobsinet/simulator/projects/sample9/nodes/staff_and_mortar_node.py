from .s9_node import S9Node
from ....tools.color import Color


class StaffAndMortarNode(S9Node):
    def __init__(self,
                 id,
                 company_id,
                 platoon_id,
                 platoon_type,
                 function,
                 type,
                 command,
                 position=None,
                 mobility_model=None,
                 connectivity_model=None,
                 interference_model=None,
                 reliability_model=None):
        super().__init__(id, company_id, platoon_id, platoon_type, function, type, command,
                         position, mobility_model, connectivity_model, interference_model, reliability_model)
        self.node_color = Color(0, 162, 255)


model = StaffAndMortarNode
