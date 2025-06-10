from ...models.nodes.abc_node import AbcNode
from ...tools.position import Position
from ...models.abc_mobility_model import AbcMobilityModel
from random import random
from ...configuration.sim_config import SimulationConfig
from typing import Optional


class RandomMob(AbcMobilityModel):
    """A random mobility model."""

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass

    def get_next_position(self, node: Optional[AbcNode] = None) -> Position:
        """
        Generate a random position within the given dimensions.

        Returns
        -------
        Position: The randomly generated position.
        """

        xcord = random() * SimulationConfig.dim_x
        ycord = random() * SimulationConfig.dim_y
        zcord = random() * SimulationConfig.dim_z if SimulationConfig.dim_z > 0 else 0

        return Position(xcord, ycord, zcord)


model = RandomMob
