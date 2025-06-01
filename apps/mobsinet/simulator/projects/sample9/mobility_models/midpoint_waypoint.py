from ....configuration.sim_config import config
from ....models.abc_mobility_model import AbcMobilityModel
from ....models.nodes.abc_node import AbcNode
from ....tools.position import Position
from random import randint, random
import math
from ....network_simulator import simulation


class MidpointWaypoint(AbcMobilityModel):

    def __init__(self):
        super().__init__('MidPointWaypoint')

        self._next_destination = None
        self._move_vector = None
        self._remaining_waiting_time = 0
        self._remaining_moves = 0
        self._waypoint_radius_range = config.mobility_model_parameters.get(
            'waypoint_radius_range', [0, 200])
        self.speed_range: list[float |
                               int] = config.mobility_model_parameters['speed_range']
        self.waiting_time_range: list[float |
                                      int] = config.mobility_model_parameters['waiting_time_range']

    def get_next_position(self, node: 'AbcNode') -> Position:
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

            self.next_destination = self.get_next_waypoint(node)

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

    def get_next_waypoint(self, node: 'AbcNode') -> Position:
        """Get the midpoint of other nodes as a waypoint.

        Returns
        -------
        Position
            The midpoint of other nodes.
        """

        midpoint = [0, 0]
        other_nodes = list(
            filter(lambda n: n.id != node.id and (simulation.has_edge(node, n) or simulation.has_edge(n, node)), simulation.nodes()))

        other_nodes = other_nodes if len(other_nodes) > 0 else list(
            filter(lambda n: n.id != node.id, simulation.nodes()))

        for n in other_nodes:
            midpoint[0] += n.position.x
            midpoint[1] += n.position.y

        midpoint[0] /= len(other_nodes)
        midpoint[1] /= len(other_nodes)

        rand_radius = random() * \
            (self._waypoint_radius_range[1] - self._waypoint_radius_range[0]
             ) + self._waypoint_radius_range[0]
        rand_direction = random() * math.pi * 2

        midpoint[0] += rand_radius * math.cos(rand_direction)
        midpoint[1] += rand_radius * math.sin(rand_direction)

        return Position(midpoint[0], midpoint[1])


model = MidpointWaypoint
