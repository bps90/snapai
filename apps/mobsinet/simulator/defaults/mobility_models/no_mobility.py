from ...models.nodes.abc_node import AbcNode
from ...tools.position import Position
from ...models.abc_mobility_model import AbcMobilityModel


class NoMobility(AbcMobilityModel):
    """A mobility model with no mobility."""

    def __init__(self):
        super().__init__('NoMobility')

    def get_next_position(self, node: AbcNode = None) -> Position:
        """
        Returns
        -------
        Position: The same position as the current position.
        """

        return node.position


model = NoMobility
