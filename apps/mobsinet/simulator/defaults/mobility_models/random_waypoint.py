from ...configuration.sim_config import SimulationConfig
from ...models.abc_mobility_model import AbcMobilityModel
from ...models.nodes.abc_node import AbcNode
from ...tools.position import Position
from random import random
import math
from typing import TypedDict, Tuple, Optional


class RandomWaypointParameters(TypedDict):
    speed_range: list[float]
    waiting_time_range: list[float]


class RandomWaypoint(AbcMobilityModel):

    def __init__(self, parameters: RandomWaypointParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

        self._next_destination: Optional[Position] = None
        self._move_vector: Optional[Tuple[float, float, float]] = None
        self._remaining_waiting_time: float = 0
        self._remaining_moves: int = 0

    def check_parameters(self, parameters):
        if ('speed_range' not in parameters or
                not isinstance(parameters['speed_range'], list) or
                len(parameters['speed_range']) != 2 or
                (not isinstance(parameters['speed_range'][0], float) and not isinstance(parameters['speed_range'][0], int)) or
                (not isinstance(parameters['speed_range'][1], float) and not isinstance(parameters['speed_range'][1], int)) or
                parameters['speed_range'][0] < 0 or
                parameters['speed_range'][1] < 0 or
                parameters['speed_range'][0] > parameters['speed_range'][1]
                ):
            return False

        if ('waiting_time_range' not in parameters or
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
            raise ValueError(
                'Invalid parameters.')

        parsed_parameters: RandomWaypointParameters = parameters
        self.speed_range: list[float] = parsed_parameters['speed_range']
        self.waiting_time_range: list[float] = parsed_parameters['waiting_time_range']

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
            self._remaining_waiting_time = random() * \
                (self.waiting_time_range[1] - self.waiting_time_range[0]
                 ) + self.waiting_time_range[0]
            self._remaining_moves = 0
        else:
            if self._move_vector is None:
                raise ValueError('Move vector is not set.')

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
            random() *
            (SimulationConfig.dim_x[1] - SimulationConfig.dim_x[0]
             ) + SimulationConfig.dim_x[0],
            random() *
            (SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0]
             ) + SimulationConfig.dim_y[0],
            random() *
            (SimulationConfig.dim_z[1] - SimulationConfig.dim_z[0]
             ) + SimulationConfig.dim_z[0]
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


model = RandomWaypoint
