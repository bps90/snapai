import random
from ...models.nodes.abc_node import AbcNode
from ...models.abc_connectivity_model import AbcConnectivityModel
from typing import TypedDict
# TODO: mudar isso para dentro da classe em todos os lugares que declare essa variável


class QUDGConnectivityParameters(TypedDict):
    min_radius: float
    max_radius: float
    big_radius_probability: float


class QUDGConnectivity(AbcConnectivityModel):
    def __init__(self, parameters: QUDGConnectivityParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)

        self.set_parameters(parameters)

    def check_parameters(self, parameters) -> bool:
        if ('min_radius' not in parameters or
            parameters['min_radius'] is None or
            parameters['min_radius'] < 0 or
                (type(parameters['min_radius']) != float and type(parameters['min_radius']) != int)):
            return False

        if ('max_radius' not in parameters or
            parameters['max_radius'] is None or
            parameters['max_radius'] < 0 or
            (type(parameters['max_radius']) != float and type(parameters['max_radius']) != int) or
                parameters['max_radius'] < parameters['min_radius']):
            return False

        if ('big_radius_probability' not in parameters or
            parameters['big_radius_probability'] is None or
            parameters['big_radius_probability'] < 0 or
                parameters['big_radius_probability'] > 1):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: QUDGConnectivityParameters = parameters
        self.min_radius: float = parsed_parameters['min_radius']
        self.max_radius: float = parsed_parameters['max_radius']
        self.big_radius_probability: float = parsed_parameters['big_radius_probability']

    def is_connected(self, node_a: AbcNode, node_b: AbcNode) -> bool:
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
