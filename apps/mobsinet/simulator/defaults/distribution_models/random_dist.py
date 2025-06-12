import random

from ...tools.position import Position
from ...models.abc_distribution_model import AbcDistributionModel
from ...configuration.sim_config import SimulationConfig

# SEED such seed could be configured from config file to reproduce simulation.
# seed_value = 10
# random.seed(seed_value)


class RandomDist(AbcDistributionModel):
    """A random Distribution Model."""

    def get_position(self) -> Position:
        """
        Generate a random position within the given dimensions.

        Returns
        -------
        Position: The randomly generated position.
        """

        p = Position(x=random.random() * SimulationConfig.dim_x,
                     y=random.random() * SimulationConfig.dim_y,
                     z=random.random() * SimulationConfig.dim_z if SimulationConfig.dim_z > 0 else 0)

        return p

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass


model = RandomDist
