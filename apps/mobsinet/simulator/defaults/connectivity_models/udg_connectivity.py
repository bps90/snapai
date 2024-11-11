from ...models.nodes.abc_node import AbcNode
from ...models.abc_connectivity_model import AbcConnectivityModel
from ...configuration.sim_config import config

parameters = config.connectivity_model_parameters


class UDGConnectivity(AbcConnectivityModel):
    def __init__(self):
        super().__init__('UDGConnectivity')

        self.max_radius = parameters['max_radius']

    def is_connected(self, node_a: AbcNode, node_b: AbcNode) -> bool:
        """Check if the nodes are connected.
        Nodes are connected if their distance is less than or equal to the maximum radius.

        Raises
        ------
        ValueError
            If the maximum radius is not set.
        """

        if (self.max_radius is None):
            raise ValueError('The maximum radius is not set.')

        distance_between_nodes = node_a.position.euclidean_distance(
            node_b.position)

        if (distance_between_nodes <= self.max_radius):
            return True

        return False

    def set_max_radius(self, radius: int):
        """Set the maximum radius that the nodes can be connected.

        Parameters
        ----------
        radius : int
            The maximum radius in unit of length.

        Raises
        ------
        ValueError
            If the radius is negative.
        """

        if radius < 0:
            raise ValueError('The radius must be positive.')

        self.max_radius = radius


model = UDGConnectivity
