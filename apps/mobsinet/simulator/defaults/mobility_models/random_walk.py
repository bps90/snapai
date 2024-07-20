from math import cos, sin, sqrt
from turtle import position
from typing import Tuple
from networkx import DiGraph, Graph, draw, draw_networkx_edge_labels, draw_networkx_nodes, get_edge_attributes, get_node_attributes
from numpy import Infinity, pi, rad2deg

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

        # REMOVE IT AFTER TESTING
        print(
            f'remaining time: {self._remaining_time}, remaining distance: {self._remaining_distance}')

        used_speed = self._current_speed if self.prioritize_speed else min(
            self._remaining_distance, self._current_speed)

        direction_vector = self._get_direction_vector(
            used_speed, self._current_direction)

        new_coordinates = (
            current_coordinates[0] + direction_vector[0],
            current_coordinates[1] + direction_vector[1],
            current_coordinates[2] + direction_vector[2]
        )

        # verify if next position is in the graph
        new_coordinates = self._check_boundary(
            current_coordinates,
            new_coordinates)

        # updates variables
        if (self._remaining_time is not None):
            self._remaining_time -= 1
        if (self._remaining_distance is not None):
            self._remaining_distance -= used_speed

        position = Position(*new_coordinates)

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
            f'Speed: {self._current_speed}, Direction: {rad2deg(self._current_direction)}')

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

    def _check_boundary(self,
                        old_coordinates: Tuple[float, float, float],
                        new_coordinates: Tuple[float, float, float]):
        """(private) Bounces the node off the boundary.

        Parameters
        ----------
        old_coordinates : Tuple[float, float, float]
            The old coordinates of the node.
        new_coordinates : Tuple[float, float, float]
            The calculated new coordinates to check and adjust.
        """

        coordinates = self._check_left_boundary(
            old_coordinates, new_coordinates)
        coordinates = self._check_right_boundary(
            old_coordinates, coordinates)
        coordinates = self._check_top_boundary(
            old_coordinates, coordinates)
        coordinates = self._check_bottom_boundary(
            old_coordinates, coordinates)

        return coordinates

    def _check_left_boundary(self,
                             old_coordinates: Tuple[float, float, float],
                             new_coordinates: Tuple[float, float, float]):
        """(private) Bounces the node off the left boundary.

        Parameters
        ----------
        old_coordinates : Tuple[float, float, float]
            The old coordinates of the node.
        new_coordinates : Tuple[float, float, float]
            The calculated new coordinates to check and adjust.

        """

        if (new_coordinates[0] < 0):
            unit_vector = self._get_unit_vector(self._current_direction)
            current_speed = sqrt(
                (new_coordinates[0] - old_coordinates[0])**2 +
                (new_coordinates[1] - old_coordinates[1])**2
            )

            self._current_direction = -self._current_direction + pi

            traveled_distance_to_boundary = - \
                old_coordinates[0] / \
                unit_vector[0]
            remaining_distance = current_speed - \
                traveled_distance_to_boundary

            direction_vector = self._get_direction_vector(
                remaining_distance, self._current_direction)

            limit_point = (0,
                           traveled_distance_to_boundary *
                           unit_vector[1] + old_coordinates[1],
                           0)

            coordinates = (
                limit_point[0] + direction_vector[0],
                limit_point[1] + direction_vector[1],
                limit_point[2] + direction_vector[2]
            )

            # REMOVE IT AFTER TESTING
            print('Bateu borda esquerda', 'direction: ', rad2deg(self._current_direction), 'travel_distance_to_boundary: ',
                  traveled_distance_to_boundary, 'limit_point: ', limit_point, 'coordinates: ', coordinates, sep='\n')

            return self._check_boundary(limit_point, coordinates)
        else:
            return new_coordinates

    def _check_right_boundary(self,
                              old_coordinates: Tuple[float, float, float],
                              new_coordinates: Tuple[float, float, float]):
        """(private) Bounces the node off the right boundary.

        Parameters
        ----------
        old_coordinates : Tuple[float, float, float]
            The old coordinates of the node.
        new_coordinates : Tuple[float, float, float]
            The calculated new coordinates to check and adjust.

        """

        if (new_coordinates[0] > sim_config_env.dimX):

            unit_vector = self._get_unit_vector(self._current_direction)
            current_speed = sqrt(
                (new_coordinates[0] - old_coordinates[0])**2 +
                (new_coordinates[1] - old_coordinates[1])**2
            )

            self._current_direction = -self._current_direction + pi

            traveled_distance_to_boundary = sim_config_env.dimX - \
                old_coordinates[0] / \
                unit_vector[0]
            remaining_distance = current_speed - \
                traveled_distance_to_boundary

            direction_vector = self._get_direction_vector(
                remaining_distance, self._current_direction)

            limit_point = (sim_config_env.dimX,
                           traveled_distance_to_boundary *
                           unit_vector[1] + old_coordinates[1],
                           0)

            coordinates = (
                limit_point[0] + direction_vector[0],
                limit_point[1] + direction_vector[1],
                limit_point[2] + direction_vector[2]
            )

            # REMOVE IT AFTER TESTING
            print('Bateu borda direita', 'direction: ', rad2deg(self._current_direction), 'travel_distance_to_boundary: ',
                  traveled_distance_to_boundary, 'limit_point: ', limit_point, 'coordinates: ', coordinates, sep='\n')

            return self._check_boundary(limit_point, coordinates)
        else:
            return new_coordinates

    def _check_top_boundary(self,
                            old_coordinates: Tuple[float, float, float],
                            new_coordinates: Tuple[float, float, float]):
        """(private) Bounces the node off the top boundary.

        Parameters
        ----------
        old_coordinates : Tuple[float, float, float]
            The old coordinates of the node.
        new_coordinates : Tuple[float, float, float]
            The calculated new coordinates to check and adjust.

        """

        if (new_coordinates[1] > sim_config_env.dimY):

            unit_vector = self._get_unit_vector(self._current_direction)
            current_speed = sqrt(
                (new_coordinates[0] - old_coordinates[0])**2 +
                (new_coordinates[1] - old_coordinates[1])**2
            )

            self._current_direction = -self._current_direction

            traveled_distance_to_boundary = sim_config_env.dimY - \
                old_coordinates[1] / \
                unit_vector[1]
            remaining_distance = current_speed - \
                traveled_distance_to_boundary

            direction_vector = self._get_direction_vector(
                remaining_distance, self._current_direction)

            limit_point = (traveled_distance_to_boundary *
                           unit_vector[0] + old_coordinates[0],
                           sim_config_env.dimY,
                           0)

            coordinates = (
                limit_point[0] + direction_vector[0],
                limit_point[1] + direction_vector[1],
                limit_point[2] + direction_vector[2]
            )

            # REMOVE IT AFTER TESTING
            print('Bateu borda topo', 'direction: ', rad2deg(self._current_direction), 'travel_distance_to_boundary: ',
                  traveled_distance_to_boundary, 'limit_point: ', limit_point, 'coordinates: ', coordinates, sep='\n')

            return self._check_boundary(limit_point, coordinates)
        else:
            return new_coordinates

    def _check_bottom_boundary(self,
                               old_coordinates: Tuple[float, float, float],
                               new_coordinates: Tuple[float, float, float]):
        """(private) Bounces the node off the bottom boundary.

        Parameters
        ----------
        old_coordinates : Tuple[float, float, float]
            The old coordinates of the node.
        new_coordinates : Tuple[float, float, float]
            The calculated new coordinates to check and adjust.

        """

        if (new_coordinates[1] < 0):

            unit_vector = self._get_unit_vector(self._current_direction)
            current_speed = sqrt(
                (new_coordinates[0] - old_coordinates[0])**2 +
                (new_coordinates[1] - old_coordinates[1])**2
            )

            self._current_direction = -self._current_direction

            traveled_distance_to_boundary = - \
                old_coordinates[1] / \
                unit_vector[1]
            remaining_distance = current_speed - \
                traveled_distance_to_boundary

            direction_vector = self._get_direction_vector(
                remaining_distance, self._current_direction)

            limit_point = (traveled_distance_to_boundary *
                           unit_vector[0] + old_coordinates[0],
                           0,
                           0)

            coordinates = (
                limit_point[0] + direction_vector[0],
                limit_point[1] + direction_vector[1],
                limit_point[2] + direction_vector[2]
            )

            # REMOVE IT AFTER TESTING
            print('Bateu borda baixo', 'direction: ', rad2deg(self._current_direction), 'travel_distance_to_boundary: ',
                  traveled_distance_to_boundary, 'limit_point: ', limit_point, 'coordinates: ', coordinates, sep='\n')

            return self._check_boundary(limit_point, coordinates)
        else:
            return new_coordinates

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


if __name__ == '__main__':
    random_walk = RandomWalk()

    random_walk.set_travel_time(5)

    node_behavior = InertNodeBehavior(
        1,
        Position(),
        random_walk,
        NoConnectivity(),
        NoInterference(),
        NoReliability()
    )

    trace_graph = DiGraph()

    trace_file = open('trace.csv', 'w')

    trace_file.write('t, x, y, z\n')

    for step in range(50):

        print('\n', step, node_behavior.get_coordinates())

        trace_graph.add_node(
            step, position=node_behavior.get_coordinates()[0:2], color='#303070')

        if step > 0:
            trace_graph.add_edge(step - 1, step, distance="{:.1f}".format(sqrt(
                (node_behavior.get_coordinates()[0] - trace_graph.nodes[step - 1]['position'][0])**2 +
                (node_behavior.get_coordinates()[
                 1] - trace_graph.nodes[step - 1]['position'][1])**2
            )))

        trace_file.write('{}, {}, {}, {}\n'.format(
            step,
            node_behavior.get_coordinates()[0],
            node_behavior.get_coordinates()[1],
            node_behavior.get_coordinates()[2]
        ))

        node_behavior.set_position(
            node_behavior.mobility_model.get_next_position(node_behavior))

    trace_file.close()

    border = Graph()
    border.add_node('A', position=(0, 0))
    border.add_node('B', position=(sim_config_env.dimX, 0))
    border.add_node('D', position=(0, sim_config_env.dimY))
    border.add_node('C', position=(sim_config_env.dimX, sim_config_env.dimY))
    border.add_edge('A', 'B')
    border.add_edge('B', 'C')
    border.add_edge('C', 'D')
    border.add_edge('D', 'A')

    draw(border,  pos=get_node_attributes(
        border, 'position'), node_size=0)


    draw(trace_graph, pos=get_node_attributes(
        trace_graph, 'position'), node_size=80, with_labels=True, font_size=7, font_color="white", node_color=[trace_graph.nodes[node]['color'] for node in trace_graph.nodes])
    draw_networkx_edge_labels(trace_graph, pos=get_node_attributes(
        trace_graph, 'position'), edge_labels=get_edge_attributes(
            trace_graph, 'distance'), font_size=7, font_family='sans-serif')
    plt.gca().set_frame_on(True)

    plt.show()
