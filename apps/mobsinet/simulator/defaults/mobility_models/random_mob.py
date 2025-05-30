from ...models.nodes.abc_node import AbcNode
from ...tools.position import Position
from ...models.abc_mobility_model import AbcMobilityModel
from random import random
from ...configuration.sim_config import config


class RandomMob(AbcMobilityModel):
    """A random mobility model."""

    def __init__(self):
        super().__init__('RandomMob')

    def get_next_position(self, node: AbcNode = None) -> Position:
        """
        Generate a random position within the given dimensions.

        Returns
        -------
        Position: The randomly generated position.
        """

        xcord = random() * config.dimX
        ycord = random() * config.dimY
        zcord = random() * config.dimZ if config.dimZ > 0 else 0

        return Position(xcord, ycord, zcord)


model = RandomMob
