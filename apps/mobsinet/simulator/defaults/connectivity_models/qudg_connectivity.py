import random
from ...configuration.sim_config import config
from ...models.nodes.abc_node_implementation import AbcNodeImplementation
from ...models.abc_connectivity_model import AbcConnectivityModel

parameters = config.connectivity_model_parameters


class QUDGConnectivity(AbcConnectivityModel):
    def __init__(self):
        super().__init__('QUDGConnectivity')

        self.min_radius = parameters['min_radius']
        self.max_radius = parameters['max_radius']
        self.big_radius_probability = parameters['big_radius_probability']

    def is_connected(self, node_a: AbcNodeImplementation, node_b: AbcNodeImplementation) -> bool:
        """Check if the nodes are connected.

        Nodes are connected if their distance 
        is less than or equal to the minimum radius 
        or if the probability that the nodes 
        are connected with a big radius is positive.

        Raises
        ------
        ValueError
            If the maximum or minimum radius is not set.

            If the big radius probability is not set.
        """

        if (self.max_radius is None or self.min_radius is None):
            raise ValueError('The maximum or minimum radius is not set.')

        if (self.big_radius_probability is None):
            raise ValueError('The big radius probability is not set.')

        distance_between_nodes = node_a.position.euclidean_distance(
            node_b.position)

        if (distance_between_nodes <= self.min_radius):
            return True
        elif (distance_between_nodes <= self.max_radius):
            return True if (random.random() < self.big_radius_probability) else False

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

    def set_min_radius(self, radius: int):
        """Set the minimum radius that the nodes can be connected.

        Parameters
        ----------
        radius : int
            The minimum radius in unit of length.

        Raises
        ------
        ValueError
            If the radius is negative.
        """

        if radius < 0:
            raise ValueError('The radius must be positive.')

        self.min_radius = radius

    def set_big_radius_probability(self, probability: float):
        """Set the probability that the nodes are connected with a big radius.

        Parameters
        ----------
        probability : float
            The probability that the nodes are connected with a big radius.

            The value must be between 0 and 1.

        Raises
        ------
        ValueError
            If the probability is not between 0 and 1.
        """

        if (probability < 0 or probability > 1):
            raise ValueError('The probability must be between 0 and 1.')

        self.big_radius_probability = probability


model = QUDGConnectivity
