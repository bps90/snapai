from math import cos, sin, sqrt, pi
from typing import Tuple
from networkx import DiGraph, Graph, draw, draw_networkx_edge_labels, draw_networkx_labels, get_edge_attributes, get_node_attributes
from ...configuration.sim_config import config
from ..connectivity_models.no_connectivity import NoConnectivity
from ..interference_models.no_interference import NoInterference
from ..nodes.inert_node import InertNode
from ..reliability_models.no_reliability import NoReliability
from ...models.abc_mobility_model import AbcMobilityModel
from ...models.nodes.abc_node import AbcNode
from ...tools.position import Position
from random import randint, random
import matplotlib.pyplot as plt
import math

config.mobility_model_parameters = config.mobility_model_parameters


class RandomWaypoint(AbcMobilityModel):

    def __init__(self):
        super().__init__('RandomWaypoint')

        self._next_destination = None
        self._move_vector = None
        self._remaining_waiting_time = 0
        self._remaining_moves = 0
        self.speed_range: list[float |
                               int] = config.mobility_model_parameters['speed_range']
        self.waiting_time_range: list[float |
                                      int] = config.mobility_model_parameters['waiting_time_range']

    def get_next_position(self, node: AbcNode) -> Position:
        """Get the next position in the trajectory to random waypoints.

        Parâmeters
        ----------
        node : AbcNode
            The node to calculates next position.

        Returns
        -------
        Position
            The next position in the trajectory to random waypoints.
        """

        current_position = node.position
        next_position = None

        if (self._remaining_waiting_time > 0):
            self._remaining_waiting_time -= 1
            return current_position

        if (self._remaining_moves == 0):
            speed = random() * \
                (self.speed_range[1] - self.speed_range[0]) + \
                self.speed_range[0]

            self.next_destination = self.get_next_waypoint()

            distance = current_position.euclidean_distance(
                self.next_destination)
            rounds = distance / speed
            self._remaining_moves = math.ceil(rounds)

            self._move_vector = (
                (self.next_destination.x - current_position.x) / rounds,
                (self.next_destination.y - current_position.y) / rounds,
                (self.next_destination.z - current_position.z) / rounds
            )

        if (self._remaining_moves <= 1):
            next_position = self.next_destination.copy()
            self._remaining_waiting_time = randint(
                self.waiting_time_range[0], self.waiting_time_range[1])
            self._remaining_moves = 0
        else:
            next_position = Position(
                current_position.x + self._move_vector[0],
                current_position.y + self._move_vector[1],
                current_position.z + self._move_vector[2]
            )
            self._remaining_moves -= 1

        return next_position

    def get_next_waypoint(self) -> Position:
        """Get a random waypoint.

        Returns
        -------
        Position
            The random waypoint.
        """

        return Position(
            randint(0, config.dimX),
            randint(0, config.dimY),
            randint(0, config.dimZ) if config.dimZ else 0
        )

    def set_speed_range(self, min_speed: float | int, max_speed: float | int):
        """Set the speed range for random waypoint.

        Parameters
        ----------
        min_speed : float | int
            The minimum speed in unit of length per time step.
        max_speed : float | int
            The maximum speed in unit of length per time step.
        """

        self.speed_range = [min_speed, max_speed]
        self._new_random_attributes()

    def set_waiting_time_range(self, min: float | int, max: float | int):
        """Set the waiting time range for random waypoint.

        Parameters
        ----------
        min : float | int
            The minimum waiting time in time steps.
        max : float | int
            The maximum waiting time in time steps.
        """

        self.waiting_time_range = [min, max]
        self._new_random_attributes()


model = RandomWaypoint
