from ...models.nodes.abc_node import AbcNode
from ...tools.position import Position
from ...models.abc_mobility_model import AbcMobilityModel


class NoMobility(AbcMobilityModel):
    """A mobility model with no mobility."""

    def get_next_position(self, node: AbcNode) -> Position:
        """
        Returns
        -------
        Position: The same position as the current position.
        """

        return node.position

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass


model = NoMobility
