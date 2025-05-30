from ....models.abc_mobility_model import AbcMobilityModel
from ....network_simulator import simulation
from ....tools.position import Position
import random
from math import cos, sin, radians, pi
from ....configuration.sim_config import config


class MidPointOfOthers(AbcMobilityModel):
    def __init__(self):
        super().__init__('MidPointOfOthers')

        radius_range = config.mobility_model_parameters.get(
            'waypoint_radius_range', [0, 200])
        self.__direction = random.random() * pi * 2
        self.__radius = random.random(
        ) * (radius_range[1] - radius_range[0]) + radius_range[0]

    def get_next_position(self, node):
        midpoint = [0, 0]
        nodes = list(filter(lambda n: n.id != node.id, simulation.nodes()))

        for n in nodes:
            midpoint[0] += n.position.x
            midpoint[1] += n.position.y

        midpoint[0] /= len(nodes)
        midpoint[1] /= len(nodes)

        coordinates = [
            midpoint[0] + self.__radius * cos(self.__direction),
            midpoint[1] + self.__radius * sin(self.__direction)]

        return Position(coordinates[0], coordinates[1])


model = MidPointOfOthers
