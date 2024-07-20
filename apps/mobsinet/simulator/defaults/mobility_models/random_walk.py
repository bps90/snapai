from math import cos, sin, sqrt
from turtle import position
from typing import Tuple
from networkx import DiGraph, Graph, draw, draw_networkx_edge_labels, draw_networkx_nodes, get_edge_attributes, get_node_attributes
from numpy import Infinity, pi

from apps.mobsinet.simulator.configuration.sim_config import sim_config_env
from apps.mobsinet.simulator.defaults.connectivity_models.no_connectivity import NoConnectivity
from apps.mobsinet.simulator.defaults.interference_models.no_interference import NoInterference
from apps.mobsinet.simulator.defaults.nodes.inert_node_behavior import InertNodeBehavior
from apps.mobsinet.simulator.defaults.reliability_models.no_reliability import NoReliability
from ...models.abc_mobility_model import AbcMobilityModel
from ...models.nodes.abc_node_behavior import AbcNodeBehavior
from ...tools.position import Position
from random import random
import matplotlib.pyplot as plt

parameters = sim_config_env.mobility_model_parameters


class RandomWalk(AbcMobilityModel):

    def __init__(self):
        super().__init__('RandomWalk')

        self.speed_range: list[float | int] = parameters['speed_range']
        self.direction_range: list[float | int] = parameters['direction_range']
        self.travel_distance: float = parameters['travel_distance']
        self.travel_time: float = parameters['travel_time']
        self.prioritize_speed: bool = parameters['prioritize_speed']

        self._current_speed = 0  # unit of length per time step
        self._current_direction = 0  # radians
        self._remaining_time = self.travel_time if self.travel_time else Infinity
        self._remaining_distance = self.travel_distance if self.travel_distance else Infinity

    def get_next_position(self, node_behavior: AbcNodeBehavior) -> Position:
        """Get the next position based on random directions and speeds.

        Parâmeters
        ----------
        node_behavior : AbcNodeBehavior
            The node behavior to calculates next position.

        Raises
        ------
        ValueError
            If `travel_distance` or `travel_time` is not set.

        Notes
        -----
        If `prioritize_speed` is `True`, when calculates 
        the next position it maybe exceed the chosen 
        distance to maintain the previously chosen speed.
        If `False`, the speed in the last step in one 
        direction may be less than the speed of the
        rest of the trip.
        """

        if (not self.travel_distance and not self.travel_time):
            raise ValueError('travel_distance or travel_time must be set')

        current_position = node_behavior.position

        # verify remaining time and distance
        if (self._remaining_distance <= 0 or self._remaining_time <= 0):
            self._new_random_attributes()

        # calculates next position
        current_coordinates = current_position.get_coordinates()

        print(
            f'remaining time: {self._remaining_time}, remaining distance: {self._remaining_distance}')

        used_speed = self._current_speed if self.prioritize_speed else min(
            self._remaining_distance, self._current_speed)

        direction_vector = self._get_direction_vector(
            used_speed, self._current_direction)

        position = Position(
            current_coordinates[0] + direction_vector[0],
            current_coordinates[1] + direction_vector[1],
            current_coordinates[2] + direction_vector[2]
        )

        # updates variables
        if (self._remaining_time is not None):
            self._remaining_time -= 1
        if (self._remaining_distance is not None):
            self._remaining_distance -= used_speed

        return position

    def _new_random_attributes(self):
        """(private) Sets new random values for `current_speed` and `current_direction`."""

        min_speed, max_speed = self.speed_range
        min_direction, max_direction = self.direction_range

        self._current_speed = (
            random() * (max_speed - min_speed)) + min_speed
        self._current_direction = (
            random() * (max_direction - min_direction)) + min_direction

        # REMOVE IT AFTER TESTING
        print(
            f'Speed: {self._current_speed}, Direction: {self._current_direction}')

        self._remaining_distance = self.travel_distance if self.travel_distance else Infinity
        self._remaining_time = self.travel_time if self.travel_time else Infinity

    def _get_direction_vector(self, speed: float, direction: float) -> Tuple[float, float, float]:
        """Get the direction vector that can be used to calculate next position.

        Parameters
        ----------
        speed : float
            The speed in unit of length per time step.
        direction : float
            The direction in radians.

        Returns
        -------
        Tuple[float, float, float]
            NOTE: The last element is always 0.
        """

        unit_vector = self._get_unit_vector(direction)

        return (
            speed * unit_vector[0],
            speed * unit_vector[1],
            0
        )

    def _get_unit_vector(self, direction: float) -> Tuple[float, float, float]:
        """Get the unit vector that points to the indicated direction.

        Parameters
        ----------
        direction : float
            The direction in radians.

        Returns
        -------
        Tuple[float, float, float]
            NOTE: The last element is always 0.
        """

        return (
            cos(direction),
            sin(direction),
            0
        )

    def set_speed_range(self, min_speed: float | int, max_speed: float | int):
        """Set the speed range for random walk.

        Parameters
        ----------
        min_speed : float | int
            The minimum speed in unit of length per time step.
        max_speed : float | int
            The maximum speed in unit of length per time step.
        """

        self.speed_range = [min_speed, max_speed]
        self._new_random_attributes()

    def set_direction_range(self, min_direction: float | int, max_direction: float | int):
        """Set the direction range for random walk.

        Parameters
        ----------
        min_direction : float | int
            The minimum direction in radians.
        max_direction : float | int
            The maximum direction in radians.
        """

        self.direction_range = [min_direction, max_direction]
        self._new_random_attributes()

    def set_travel_distance(self, distance: float | int):
        """Set the travel distance that the node should travel with same speed and direction.

        Parameters
        ----------
        distance : float | int
            The travel distance in unit of length.
        """

        self.travel_distance = distance
        self._remaining_distance = distance
        self._new_random_attributes()

    def set_travel_time(self, time: float | int):
        """Set the travel time that the node should travel with same speed and direction.

        Parameters
        ----------
        time : float | int
            The travel time in unit of time step.
        """

        self.travel_time = time
        self._remaining_time = time
        self._new_random_attributes()

    def set_prioritize_speed(self, prioritize_speed: bool):
        """Set whether prioritize speed or not.

        If `prioritize_speed` is `True`, when calculates 
        the next position it maybe exceed the chosen 
        distance to maintain the previously chosen speed.
        If `False`, the speed in the last step in one 
        direction may be less than the speed of the
        rest of the trip.

        Parameters
        ----------
        prioritize_speed : bool
            Whether prioritize speed or not.
        """

        self.prioritize_speed = prioritize_speed


