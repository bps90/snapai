import random

from ...tools.position import Position
from ...models.abc_distribution_model import AbcDistributionModel
from ...configuration.sim_config import SimulationConfig


class RandomDist(AbcDistributionModel):
    """A random Distribution Model."""

    def get_position(self) -> Position:
        """
        Generate a random position within the given dimensions.

        Returns
        -------
        Position: The randomly generated position.
        """

        p = Position(x=random.random() * (SimulationConfig.dim_x[1] - SimulationConfig.dim_x[0]) + SimulationConfig.dim_x[0],
                     y=random.random() *
                     (SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0]
                      ) + SimulationConfig.dim_y[0],
                     z=(random.random() * (SimulationConfig.dim_z[1] - SimulationConfig.dim_z[0]) + SimulationConfig.dim_z[0]) if (SimulationConfig.dim_z[1] - SimulationConfig.dim_z[0]) > 0 else 0)

        return p

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass


model = RandomDist
