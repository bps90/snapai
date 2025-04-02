import math
from random import random
from ...configuration.sim_config import config
from ...tools.position import Position
from ...models.abc_mobility_model import AbcMobilityModel
from ...models.nodes.abc_node import AbcNode


class RandomDirection(AbcMobilityModel):
    def __init__(self):
        super().__init__('RandomDirection')

        self._move_vector = None
        self._remaining_waiting_time = 0
        self._remaining_moves = 0
        self.speed_range = config.mobility_model_parameters['speed_range']
        self.waiting_time_range = config.mobility_model_parameters['waiting_time_range']
        self.move_time_range = config.mobility_model_parameters['move_time_range']
        self._initialize = True

    def get_next_position(self, node: AbcNode) -> Position:
        current_position = node.position

        if self._initialize:
            wt = abs(random(
            ) * (self.waiting_time_range[1] - self.waiting_time_range[0]) + self.waiting_time_range[0])
            mt = abs(random(
            ) * (self.move_time_range[1] - self.move_time_range[0]) + self.move_time_range[0])
            fraction = random() * (wt + mt)

            if (fraction < wt):
                self._remaining_waiting_time = math.ceil(wt - fraction)
                self._remaining_moves = 0
            else:
                speed = abs(
                    random() * (self.speed_range[1] - self.speed_range[0]) + self.speed_range[0])
                self._initialize_next_move(speed, mt + wt - fraction)
            self._initialize = False

        if self._remaining_waiting_time > 0:
            self._remaining_waiting_time -= 1
            return current_position

        if self._remaining_moves == 0:
            speed = abs(
                random() * (self.speed_range[1] - self.speed_range[0]) + self.speed_range[0])
            move_time = abs(random(
            ) * (self.move_time_range[1] - self.move_time_range[0]) + self.move_time_range[0])

            self._initialize_next_move(speed, move_time)

        new_x = current_position.x + self._move_vector[0]
        new_y = current_position.y + self._move_vector[1]
        new_z = current_position.z + self._move_vector[2]

        new_x, new_y, new_z = self._reflect_if_outside(new_x, new_y, new_z)

        next_position = Position(new_x, new_y, new_z)

        if self._remaining_moves <= 1:
            self._remaining_waiting_time = math.ceil(
                abs(random() * (self.waiting_time_range[1] - self.waiting_time_range[0]) + self.waiting_time_range[0]))
            self._remaining_moves = 0
        else:
            self._remaining_moves -= 1

        return next_position

    def _initialize_next_move(self, speed: float, move_time: float):
        angle_xy = 2 * math.pi * random()
        angle_z = math.pi * (0.5 - random()) if config.dimZ else 0
        distance = move_time * speed

        dx = distance * math.cos(angle_xy) * math.cos(angle_z)
        dy = distance * math.sin(angle_xy) * math.cos(angle_z)
        dz = distance * math.sin(angle_z)

        self._remaining_moves = math.ceil(move_time)
        self._move_vector = (dx / move_time, dy / move_time, dz / move_time)

    def _reflect_if_outside(self, x, y, z):
        reflected = True
        while reflected:
            reflected = False
            if x < 0:
                x = -x
                self._move_vector = (-self._move_vector[0],
                                     self._move_vector[1], self._move_vector[2])
                reflected = True
            if y < 0:
                y = -y
                self._move_vector = (
                    self._move_vector[0], -self._move_vector[1], self._move_vector[2])
                reflected = True
            if z < 0:
                z = -z
                self._move_vector = (
                    self._move_vector[0], self._move_vector[1], -self._move_vector[2])
                reflected = True
            if x > config.dimX:
                x = 2 * config.dimX - x
                self._move_vector = (-self._move_vector[0],
                                     self._move_vector[1], self._move_vector[2])
                reflected = True
            if y > config.dimY:
                y = 2 * config.dimY - y
                self._move_vector = (
                    self._move_vector[0], -self._move_vector[1], self._move_vector[2])
                reflected = True
            if z > config.dimZ:
                z = 2 * config.dimZ - z
                self._move_vector = (
                    self._move_vector[0], self._move_vector[1], -self._move_vector[2])
                reflected = True
        return x, y, z


model = RandomDirection
