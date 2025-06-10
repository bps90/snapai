from ...models.nodes.abc_node import AbcNode
from ...models.abc_connectivity_model import AbcConnectivityModel
from typing import TypedDict


class UDGConnectivityParameters(TypedDict):
    max_radius: int


class UDGConnectivity(AbcConnectivityModel):
    def __init__(self, parameters: UDGConnectivityParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

    def check_parameters(self, parameters):
        if ('max_radius' not in parameters or
            parameters['max_radius'] is None or
            parameters['max_radius'] < 0 or
                (type(parameters['max_radius']) != float and type(parameters['max_radius']) != int)):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: UDGConnectivityParameters = parameters
        self.max_radius: float = parsed_parameters['max_radius']

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
