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

        xcord = random() * \
            (SimulationConfig.dim_x[1] - SimulationConfig.dim_x[0]
             ) + SimulationConfig.dim_x[0]
        ycord = random() * \
            (SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0]
             ) + SimulationConfig.dim_y[0]
        zcord = (random() * (SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0]) +
                 SimulationConfig.dim_y[0]) if (SimulationConfig.dim_z[1] - SimulationConfig.dim_z[0]) > 0 else 0

        return Position(xcord, ycord, zcord)


model = RandomMob
