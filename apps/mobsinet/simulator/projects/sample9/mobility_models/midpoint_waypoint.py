from ....models.abc_mobility_model import AbcMobilityModel
from ....models.nodes.abc_node import AbcNode
from ....tools.position import Position
from random import randint, random
import math
from ....network_simulator import simulation
from typing import TypedDict, Optional, Tuple


class MidpointWaypointParameters(TypedDict):
    waypoint_radius_range: list[float]
    speed_range: list[float]
    waiting_time_range: list[float]


class MidpointWaypoint(AbcMobilityModel):

    def __init__(self, parameters: MidpointWaypointParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)

        self.set_parameters(parameters)
        self._next_destination: Optional[Position] = None
        self._move_vector: Optional[Tuple[float, float, float]] = None
        self._remaining_waiting_time: float = 0
        self._remaining_moves: int = 0

    def check_parameters(self, parameters):
        if (
            'waypoint_radius_range' not in parameters or
            not isinstance(parameters['waypoint_radius_range'], list) or
            len(parameters['waypoint_radius_range']) != 2 or
            (not isinstance(parameters['waypoint_radius_range'][0], float) and not isinstance(parameters['waypoint_radius_range'][0], int)) or
            (not isinstance(parameters['waypoint_radius_range'][1], float) and not isinstance(parameters['waypoint_radius_range'][1], int)) or
            parameters['waypoint_radius_range'][0] < 0 or
            parameters['waypoint_radius_range'][1] < 0 or
            parameters['waypoint_radius_range'][0] > parameters['waypoint_radius_range'][1]
        ):
            return False

        if (
            'speed_range' not in parameters or
            not isinstance(parameters['speed_range'], list) or
            len(parameters['speed_range']) != 2 or
            (not isinstance(parameters['speed_range'][0], float) and not isinstance(parameters['speed_range'][0], int)) or
            (not isinstance(parameters['speed_range'][1], float) and not isinstance(parameters['speed_range'][1], int)) or
            parameters['speed_range'][0] < 0 or
            parameters['speed_range'][1] < 0 or
            parameters['speed_range'][0] > parameters['speed_range'][1]
        ):
            return False

        if (
            'waiting_time_range' not in parameters or
            not isinstance(parameters['waiting_time_range'], list) or
            len(parameters['waiting_time_range']) != 2 or
            (not isinstance(parameters['waiting_time_range'][0], float) and not isinstance(parameters['waiting_time_range'][0], int)) or
            (not isinstance(parameters['waiting_time_range'][1], float) and not isinstance(parameters['waiting_time_range'][1], int)) or
            parameters['waiting_time_range'][0] < 0 or
            parameters['waiting_time_range'][1] < 0 or
            parameters['waiting_time_range'][0] > parameters['waiting_time_range'][1]
        ):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: MidpointWaypointParameters = parameters

        self.waypoint_radius_range = parsed_parameters['waypoint_radius_range']
        self.speed_range = parsed_parameters['speed_range']
        self.waiting_time_range = parsed_parameters['waiting_time_range']

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
            self._remaining_waiting_time = random() * (self.waiting_time_range[1] - self.waiting_time_range[0]) + \
                self.waiting_time_range[0]

            self._remaining_moves = 0
        else:
            if (self._move_vector is None):
                raise ValueError('Move vector is None.')

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

        midpoint: list[float] = [0, 0]
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
            (self.waypoint_radius_range[1] - self.waypoint_radius_range[0]
             ) + self.waypoint_radius_range[0]
        rand_direction = random() * math.pi * 2

        midpoint[0] += rand_radius * math.cos(rand_direction)
        midpoint[1] += rand_radius * math.sin(rand_direction)

        return Position(midpoint[0], midpoint[1])


model = MidpointWaypoint
