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

config.mobility_model_parameters = config.mobility_model_parameters

# TODO: REMOVE IT AFTER TESTING
colision_digraph = DiGraph()
trace_graph = DiGraph()


def add_colision(
        old_coordinates: Tuple[float, float, float],
        limit_point: Tuple[float, float, float],
        new_coordinates: Tuple[float, float, float],
        coordinates: Tuple[float, float, float],
        traveled_distance_to_boundary: float,
        remaining_distance: float):
    old_node_id = f'{trace_graph.number_of_nodes() - 1.0:.1f}'
    limit_node_id = f'{trace_graph.number_of_nodes() - 0.9:.1f}'
    overmapped_node_id = f'{trace_graph.number_of_nodes() - 0.8:.1f}'
    new_allocated_node_id = f'{
        trace_graph.number_of_nodes() - 0.7:.1f}'

    while (colision_digraph.has_node(old_node_id)):
        old_node_id += '.0'

    while (colision_digraph.has_node(limit_node_id)):
        limit_node_id += '.1'

    while (colision_digraph.has_node(overmapped_node_id)):
        overmapped_node_id += '.2'

    while (colision_digraph.has_node(new_allocated_node_id)):
        new_allocated_node_id += '.3'

    colision_digraph.add_node(
        old_node_id,
        position=old_coordinates[0:2],
        color='#999999')

    colision_digraph.add_node(
        limit_node_id,
        position=limit_point[0:2],
        color='#f000f0')

    colision_digraph.add_node(
        overmapped_node_id,
        position=new_coordinates[0:2],
        color='#f00000')

    colision_digraph.add_node(
        new_allocated_node_id,
        position=coordinates[0:2],
        color='#f000f0')

    colision_digraph.add_edge(
        old_node_id,
        limit_node_id,
        distance=f'{traveled_distance_to_boundary:.1f}')
    colision_digraph.add_edge(
        limit_node_id,
        overmapped_node_id,
        distance=f'{sqrt((new_coordinates[0] - limit_point[0])**2 + (new_coordinates[1] - limit_point[1])**2):.1f}')
    colision_digraph.add_edge(
        limit_node_id,
        new_allocated_node_id,
        distance=f'{remaining_distance:.1f}')


class RandomWalk(AbcMobilityModel):

    def __init__(self):
        super().__init__('RandomWalk')

        self.speed_range: list[float |
                               int] = config.mobility_model_parameters['speed_range']
        self.direction_range: list[float |
                                   int] = config.mobility_model_parameters['direction_range']
        self.travel_distance: float = config.mobility_model_parameters['travel_distance']
        self.travel_time: float = config.mobility_model_parameters['travel_time']
        self.prioritize_speed: bool = config.mobility_model_parameters['prioritize_speed']

        self._current_speed = 0  # unit of length per time step
        self._current_direction = 0  # radians
        self._remaining_time = self.travel_time if self.travel_time else float(
            'inf')
        self._remaining_distance = self.travel_distance if self.travel_distance else float(
            'inf')
        self._new_random_attributes()

    def get_next_position(self, node: AbcNode) -> Position:
        """Get the next position based on random directions and speeds.

        Parâmeters
        ----------
        node : AbcNode
            The node to calculates next position.

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

        current_position = node.position

        # verify remaining time and distance
        if (self._remaining_distance <= 0 or self._remaining_time <= 0):
            self._new_random_attributes()

        # calculates next position

        current_coordinates = current_position.get_coordinates()
        used_speed = self._current_speed if self.prioritize_speed else min(
            self._remaining_distance, self._current_speed)
        direction_vector = self._get_direction_vector(
            used_speed, self._current_direction)
        new_coordinates = (
            current_coordinates[0] + direction_vector[0],
            current_coordinates[1] + direction_vector[1],
            current_coordinates[2] + direction_vector[2]
        )

        # verify if next position is in the simulation limits
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
        """(private) Sets new random values for `current_speed` and `current_direction`.

        Notes
        -----
        Reset the remaining time and distance.
        """

        min_speed, max_speed = self.speed_range
        min_direction, max_direction = self.direction_range

        self._current_speed = (
            random() * (max_speed - min_speed)) + min_speed
        self._current_direction = (
            random() * (max_direction - min_direction)) + min_direction

        self._remaining_distance = self.travel_distance if self.travel_distance else float(
            'inf')
        self._remaining_time = self.travel_time if self.travel_time else float(
            'inf')

    def _get_direction_vector(self, speed: float, direction: float) -> Tuple[float, float, float]:
        """(private) Get the direction vector that can be used to calculate next position.

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
        """(private) Get the unit vector that points to the indicated direction.

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
        """(private) Bounces the node off the boundary if it is in the wrong direction.

        Parameters
        ----------
        old_coordinates : Tuple[float, float, float]
            The old coordinates of the node.
        new_coordinates : Tuple[float, float, float]
            The calculated new coordinates to check and adjust.

        Returns
        -------
        Tuple[float, float, float]
            The adjusted coordinates of the node.
        """

        # calculates the distance of the node from the boundary

        unit_vector = self._get_unit_vector(self._current_direction)

        traveled_distance_to_left_boundary = (
            - old_coordinates[0] / unit_vector[0]) if unit_vector[0] != 0 else float('inf')
        traveled_distance_to_right_boundary = ((config.dimX -
                                               old_coordinates[0]) / unit_vector[0]) if unit_vector[0] != 0 else float('inf')
        traveled_distance_to_top_boundary = ((
            config.dimY - old_coordinates[1]) / unit_vector[1]) if unit_vector[1] != 0 else float('inf')
        traveled_distance_to_bottom_boundary = (
            - old_coordinates[1] / unit_vector[1]) if unit_vector[1] != 0 else float('inf')

        on_range_direction = self._current_direction % (2 * pi)

        coordinates = new_coordinates

        # If the node is in right direction
        if (on_range_direction == 0):
            coordinates = self._check_right_boundary(
                old_coordinates, new_coordinates)

        # If the direction vector is in first quadrant
        elif (on_range_direction < (pi / 2) and on_range_direction > 0):
            less_traveled_distance = min(
                traveled_distance_to_right_boundary if traveled_distance_to_right_boundary >= 0 else float(
                    'inf'),
                traveled_distance_to_top_boundary if traveled_distance_to_top_boundary >= 0 else float(
                    'inf'),
            )

            if (traveled_distance_to_right_boundary == less_traveled_distance):
                coordinates = self._check_right_boundary(
                    old_coordinates, new_coordinates)

            if (traveled_distance_to_top_boundary == less_traveled_distance):
                coordinates = self._check_top_boundary(
                    old_coordinates, new_coordinates)

        # If the node is in top direction
        elif (on_range_direction == (pi / 2)):
            coordinates = self._check_top_boundary(
                old_coordinates, new_coordinates)

        # If the direction vector is in second quadrant
        elif (on_range_direction < pi and on_range_direction > (pi / 2)):
            less_traveled_distance = min(
                traveled_distance_to_left_boundary if traveled_distance_to_left_boundary >= 0 else float(
                    'inf'),
                traveled_distance_to_top_boundary if traveled_distance_to_top_boundary >= 0 else float(
                    'inf'),
            )

            if (traveled_distance_to_left_boundary == less_traveled_distance):
                coordinates = self._check_left_boundary(
                    old_coordinates, new_coordinates)

            if (traveled_distance_to_top_boundary == less_traveled_distance):
                coordinates = self._check_top_boundary(
                    old_coordinates, new_coordinates)

        # If the node is in left direction
        elif (on_range_direction == pi):
            coordinates = self._check_left_boundary(
                old_coordinates, new_coordinates)

        # If the direction vector is in third quadrant
        elif (on_range_direction < (3 * pi / 2) and on_range_direction > pi):
            less_traveled_distance = min(
                traveled_distance_to_left_boundary if traveled_distance_to_left_boundary >= 0 else float(
                    'inf'),
                traveled_distance_to_bottom_boundary if traveled_distance_to_bottom_boundary >= 0 else float(
                    'inf'),
            )

            if (traveled_distance_to_left_boundary == less_traveled_distance):
                coordinates = self._check_left_boundary(
                    old_coordinates, new_coordinates)

            if (traveled_distance_to_bottom_boundary == less_traveled_distance):
                coordinates = self._check_bottom_boundary(
                    old_coordinates, new_coordinates)

        # If the node is in bottom direction
        elif (on_range_direction == (3 * pi / 2)):
            coordinates = self._check_bottom_boundary(
                old_coordinates, new_coordinates)

        # If the direction vector is in fourth quadrant
        elif (on_range_direction < 2 * pi and on_range_direction > (3 * pi / 2)):
            less_traveled_distance = min(
                traveled_distance_to_right_boundary if traveled_distance_to_right_boundary >= 0 else float(
                    'inf'),
                traveled_distance_to_bottom_boundary if traveled_distance_to_bottom_boundary >= 0 else float(
                    'inf'),
            )

            if (traveled_distance_to_right_boundary == less_traveled_distance):
                coordinates = self._check_right_boundary(
                    old_coordinates, new_coordinates)

            if (traveled_distance_to_bottom_boundary == less_traveled_distance):
                coordinates = self._check_bottom_boundary(
                    old_coordinates, new_coordinates)

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

        Returns
        -------
        Tuple[float, float, float]
            The adjusted coordinates.
        """

        if (new_coordinates[0] < 0):
            unit_vector = self._get_unit_vector(self._current_direction)
            current_speed = sqrt(
                (new_coordinates[0] - old_coordinates[0])**2 +
                (new_coordinates[1] - old_coordinates[1])**2
            )

            self._current_direction = -self._current_direction + pi

            traveled_distance_to_boundary = (-
                                             old_coordinates[0] /
                                             unit_vector[0]) if unit_vector[0] != 0 else float('inf')
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

            if (__name__ == "__main__"):
                add_colision(old_coordinates,
                             limit_point,
                             new_coordinates,
                             coordinates,
                             traveled_distance_to_boundary,
                             remaining_distance)

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

        Returns
        -------
        Tuple[float, float, float]
            The adjusted coordinates.
        """

        if (new_coordinates[0] > config.dimX):

            unit_vector = self._get_unit_vector(self._current_direction)
            current_speed = sqrt(
                (new_coordinates[0] - old_coordinates[0])**2 +
                (new_coordinates[1] - old_coordinates[1])**2
            )

            self._current_direction = -self._current_direction + pi

            traveled_distance_to_boundary = ((
                config.dimX - old_coordinates[0]) / unit_vector[0]) if unit_vector[0] != 0 else float('inf')
            remaining_distance = (
                current_speed - traveled_distance_to_boundary)

            direction_vector = self._get_direction_vector(
                remaining_distance, self._current_direction)

            limit_point = (config.dimX,
                           traveled_distance_to_boundary *
                           unit_vector[1] + old_coordinates[1],
                           0)

            coordinates = (
                limit_point[0] + direction_vector[0],
                limit_point[1] + direction_vector[1],
                limit_point[2] + direction_vector[2]
            )

            if (__name__ == "__main__"):
                add_colision(old_coordinates,
                             limit_point,
                             new_coordinates,
                             coordinates,
                             traveled_distance_to_boundary,
                             remaining_distance)

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

        Returns
        -------
        Tuple[float, float, float]
            The adjusted coordinates.
        """

        if (new_coordinates[1] > config.dimY):

            unit_vector = self._get_unit_vector(self._current_direction)
            current_speed = sqrt(
                (new_coordinates[0] - old_coordinates[0])**2 +
                (new_coordinates[1] - old_coordinates[1])**2
            )

            self._current_direction = -self._current_direction

            traveled_distance_to_boundary = ((
                config.dimY - old_coordinates[1]) / unit_vector[1]) if unit_vector[1] != 0 else float('inf')
            remaining_distance = current_speed - \
                traveled_distance_to_boundary

            direction_vector = self._get_direction_vector(
                remaining_distance, self._current_direction)

            limit_point = (traveled_distance_to_boundary *
                           unit_vector[0] + old_coordinates[0],
                           config.dimY,
                           0)

            coordinates = (
                limit_point[0] + direction_vector[0],
                limit_point[1] + direction_vector[1],
                limit_point[2] + direction_vector[2]
            )

            if (__name__ == "__main__"):
                add_colision(old_coordinates,
                             limit_point,
                             new_coordinates,
                             coordinates,
                             traveled_distance_to_boundary,
                             remaining_distance)

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

        Returns
        -------
        Tuple[float, float, float]
            The adjusted coordinates.
        """

        if (new_coordinates[1] < 0):

            unit_vector = self._get_unit_vector(self._current_direction)
            current_speed = sqrt(
                (new_coordinates[0] - old_coordinates[0])**2 +
                (new_coordinates[1] - old_coordinates[1])**2
            )

            self._current_direction = -self._current_direction

            traveled_distance_to_boundary = (
                - old_coordinates[1] / unit_vector[1]) if unit_vector[1] != 0 else float('inf')
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

            if (__name__ == "__main__"):
                add_colision(old_coordinates,
                             limit_point,
                             new_coordinates,
                             coordinates,
                             traveled_distance_to_boundary,
                             remaining_distance)

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

        Notes
        -----
        If `prioritize_speed` is `True`, when calculates
        the next position it maybe exceed the chosen
        distance to maintain the previously chosen speed.

        Reset the remaining distance.
        """

        self.travel_distance = distance
        self._remaining_distance = distance

    def set_travel_time(self, time: float | int):
        """Set the travel time that the node should travel with same speed and direction.

        Parameters
        ----------
        time : float | int
            The travel time in unit of time step.

        Notes
        -----
        Reset the remaining time.
        """

        self.travel_time = time
        self._remaining_time = time

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


model = RandomWalk

if __name__ == '__main__':
    print('asd')
    random_walk = RandomWalk()

    random_walk.set_travel_distance(70)
    random_walk.set_speed_range(1, 50)

    node = InertNode(
        1,
        Position(randint(0, config.dimX),
                 randint(0, config.dimY),
                 0),
        random_walk,
        NoConnectivity(),
        NoInterference(),
        NoReliability()
    )

    trace_file = open('random_walk_example_trace.csv', 'w')
    trace_file.write('t, x, y, z\n')

    for step in range(50):
        print(step, node.get_coordinates())

        trace_graph.add_node(
            step,
            position=node.get_coordinates()[0:2],
            color='#303070')

        if step > 0:
            current_coordinates = node.get_coordinates()
            last_coordinates = trace_graph.nodes[step - 1]['position']

            trace_graph.add_edge(step - 1,
                                 step,
                                 distance="{:.1f}".format(
                                     sqrt(
                                         (current_coordinates[0] - last_coordinates[0])**2 +
                                         (current_coordinates[1] - last_coordinates[1])**2)))

        trace_file.write('{}, {}, {}, {}\n'.format(
            step,
            node.get_coordinates()[0],
            node.get_coordinates()[1],
            node.get_coordinates()[2]
        ))

        node.set_position(
            node.mobility_model.get_next_position(node))

    trace_file.close()

    # draw a graph of the borders
    border = Graph()
    border.add_node('A', position=(0, 0))
    border.add_node('B', position=(config.dimX, 0))
    border.add_node('D', position=(0, config.dimY))
    border.add_node('C', position=(config.dimX, config.dimY))
    border.add_edge('A', 'B')
    border.add_edge('B', 'C')
    border.add_edge('C', 'D')
    border.add_edge('D', 'A')
    draw(border,
         pos=get_node_attributes(
             border, 'position'),
         node_size=0)

    another_digraph_labels = {}
    another_digraph_color_map = []
    trace_graph_color_map = []

    for node in colision_digraph.nodes:
        another_digraph_color_map.append(colision_digraph.nodes[node]['color'])
        another_digraph_labels[node] = str(node).split('.')[0]

        first_position = colision_digraph.nodes[node]['position']

        for another_node in colision_digraph.nodes:
            if another_node != node:
                another_position = colision_digraph.nodes[another_node]['position']

                distance = sqrt(
                    (first_position[0] - another_position[0])**2 +
                    (first_position[1] - another_position[1])**2)

                if distance == 0:
                    try:
                        colision_digraph.remove_edge(node, another_node)
                    except:
                        pass

    for node in trace_graph.nodes:
        trace_graph_color_map.append(trace_graph.nodes[node]['color'])

    draw(colision_digraph,
         pos=get_node_attributes(colision_digraph, 'position'),
         node_size=80,
         node_color=another_digraph_color_map,
         with_labels=False,
         font_size=6,
         edge_color="#dddddd",
         font_color="black")
    draw_networkx_labels(colision_digraph,
                         pos=get_node_attributes(
                             colision_digraph, 'position'),
                         labels=another_digraph_labels,
                         font_size=6,
                         font_family='sans-serif')

    draw(trace_graph,
         pos=get_node_attributes(
             trace_graph, 'position'),
         node_size=80,
         with_labels=True,
         font_size=7,
         font_color="white",
         node_color=trace_graph_color_map)
    draw_networkx_edge_labels(trace_graph,
                              pos=get_node_attributes(
                                  trace_graph, 'position'),
                              edge_labels=get_edge_attributes(
                                  trace_graph, 'distance'),
                              font_size=5,
                              font_family='sans-serif')

    draw_networkx_edge_labels(
        colision_digraph,
        pos=get_node_attributes(colision_digraph, 'position'),
        font_size=5,
        font_family='sans-serif',
        font_color="#aaaaaa",
        edge_labels=get_edge_attributes(colision_digraph, 'distance'),
        connectionstyle='arc3, rad=0.1')

    plt.axis('equal')
    plt.show()
