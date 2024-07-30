import random

from apps.mobsinet.simulator.models.nodes.abc_node_behavior import AbcNodeBehavior
from ...tools.position import Position
from ...models.abc_distribution_model import AbcDistributionModel
from ...configuration.sim_config import sim_config_env

# SEED such seed could be configured from config file to reproduce simulation.
# seed_value = 10
# random.seed(seed_value)


class RandomDist(AbcDistributionModel):
    """A random Distribution Model."""

    def __init__(self):
        super().__init__("RandomDist")

    def get_position(self) -> Position:
        """
        Generate a random position within the given dimensions.

        Returns
        -------
        Position: The randomly generated position.
        """

        p = Position(x=random.randrange(0, sim_config_env.dimX),
                     y=random.randrange(0, sim_config_env.dimZ),
                     z=random.randrange(0, sim_config_env.dimZ))

        return p


model = RandomDist

if __name__ == "__main__":
    # Create instances of the class
    dm = RandomDist()
    print(dm.get_position())
