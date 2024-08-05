from math import cos, pi, sin
from typing import Literal, Tuple

from matplotlib import pyplot as plt
from networkx import Graph, draw, get_node_attributes
from apps.mobsinet.simulator.models.abc_distribution_model import AbcDistributionModel
from apps.mobsinet.simulator.tools.position import Position
from ...configuration.sim_config import sim_config_env

parameters = sim_config_env.distribution_model_parameters


class CircularDist(AbcDistributionModel):
    def __init__(self) -> None:
        super().__init__('CircularDist')

        self.radius = parameters['radius']
        self.rotation_direction = parameters['rotation_direction']
        self.midpoint = parameters['midpoint']
        self.number_of_nodes = parameters['number_of_nodes']

        self._radians = 0

    def get_position(self) -> Position:
        """Get the next position for the node in the distribution.

        Raises
        ------
        ValueError
            If the radius, rotation direction or midpoint is not set.

            If the radius is too large for the midpoint.

        Returns
        -------
        Position
            The next position for the node in the distribution.
        """

        if (self.radius is None):
            raise ValueError('The radius is not set.')

        if (self.rotation_direction is None):
            raise ValueError('The rotation direction is not set.')

        if (self.midpoint is None):
            raise ValueError('The midpoint is not set.')

        if (self.midpoint[0] - self.radius < 0 or self.midpoint[0] + self.radius > sim_config_env.dimX or self.midpoint[1] - self.radius < 0 or self.midpoint[1] + self.radius > sim_config_env.dimY):
            raise ValueError('The radius is too large for the midpoint.')

        new_coordinates = self._get_new_coordinates()

        self._radians += 2 * pi / self.number_of_nodes

        position = Position(*new_coordinates)

        return position

    def _get_new_coordinates(self) -> Tuple[float, float, float]:
        """(private) Get the next coordinates for the node in the distribution."""

        return (
            self.midpoint[0] + self.radius * cos(self._radians),
            self.midpoint[1] + self.radius * (sin(
                self._radians) if self.rotation_direction == 'anti-clockwise' else -sin(self._radians)),
            0
        )

    def set_number_of_nodes(self, number_of_nodes: int):
        """Set the number of nodes that will be distributed.

        Also calculates the separation between nodes.
        """

        self.number_of_nodes = number_of_nodes

        self._radians = 0

    def set_rotation_direction(self, rotation_direction: Literal['anti-clockwise', 'clockwise']):
        """Set the rotation direction of the nodes.

        Parameters
        ----------
        rotation_direction : str
            The rotation direction. Either 'anti-clockwise' or 'clockwise'.
        """

        self.rotation_direction = rotation_direction

    def set_radius(self, radius: float):
        """Set the radius of the circle.

        Parameters
        ----------
        radius : float
            The radius in unit of length.

        Raises
        ------
        ValueError
            If the radius is negative.
        """

        if (radius < 0):
            raise ValueError('The radius must be positive.')

        self.radius = radius

    def set_midpoint(self, midpoint: Position):
        """Set the midpoint of the circle.

        Parameters
        ----------
        midpoint : Position
            The midpoint of the circle.
        """

        self.midpoint = midpoint.get_coordinates()


if __name__ == '__main__':
    circular_dist = CircularDist()

    circular_dist.set_radius(50)
    circular_dist.set_number_of_nodes(100)
    circular_dist.set_rotation_direction('anti-clockwise')
    circular_dist.set_midpoint(Position(50, 50))

    graph = Graph()

    iteractions = 85

    for i in range(iteractions):
        position = circular_dist.get_position()

        graph.add_node(i, position=position.get_coordinates()[0:2])

        print(position)

    draw(graph, pos=get_node_attributes(graph, 'position'))
    plt.axis('equal')

    plt.show()
