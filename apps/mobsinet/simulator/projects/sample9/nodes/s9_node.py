from ....models.nodes.abc_node import AbcNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....tools.position import Position
    from ....models.abc_mobility_model import AbcMobilityModel
    from ....models.abc_connectivity_model import AbcConnectivityModel
    from ....models.abc_interference_model import AbcInterferenceModel
    from ....models.abc_reliability_model import AbcReliabilityModel


class S9Node(AbcNode):
    def __init__(
            self,
            id: int,
            company_id: int,
            platoon_id: int,
            platoon_type: str,
            function: str,
            type: str,
            command: str,
            comm_channels: list,
            position: 'Position',
            mobility_model: 'AbcMobilityModel',
            connectivity_model: 'AbcConnectivityModel',
            interference_model: 'AbcInterferenceModel',
            reliability_model: 'AbcReliabilityModel'):
        super().__init__(
            id,
            mobility_model,
            connectivity_model,
            interference_model,
            reliability_model,
            position=position)
        self.company_id = company_id
        self.platoon_id = platoon_id
        self.platoon_type = platoon_type
        self.function = function
        self.type = type
        self.command = command
        self.comm_channels = comm_channels
        self.size = 3

    def check_requirements(self):
        pass

    def handle_messages(self, inbox):
        pass

    def init(self):
        pass

    def on_neighboorhood_change(self):
        pass

    def post_step(self):
        pass

    def pre_step(self):
        pass


node = S9Node
