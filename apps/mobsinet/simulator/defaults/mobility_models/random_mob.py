from ...models.nodes.abc_node_implementation import AbcNodeImplementation
from ...tools.position import Position
from ...models.abc_mobility_model import AbcMobilityModel
from random import randint
from ...configuration.sim_config import sim_config_env


class RandomMob(AbcMobilityModel):
    """A random mobility model."""

    def __init__(self):
        super().__init__('RandomMob')

    def get_next_position(self, node_implementation: AbcNodeImplementation = None) -> Position:
        """
        Generate a random position within the given dimensions.

        Returns
        -------
        Position: The randomly generated position.
        """

        xcord = randint(0, sim_config_env.dimX)
        ycord = randint(0, sim_config_env.dimY)
        zcord = randint(0, sim_config_env.dimZ)

        return Position(xcord, ycord, zcord)


model = RandomMob
