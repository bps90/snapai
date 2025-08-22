from ....models.abc_mobility_model import AbcMobilityModel
from ....network_simulator import simulation
from ....tools.position import Position
import random
from math import cos, pi, sin
from typing import TypedDict
from ....configuration.layout.form_section import FormSubSection, FormSectionFieldInformative, FormSectionLine, FormSectionNumberPairField

class MidPointOfOthersParameters(TypedDict):
    waypoint_radius_range: list[float]


class MidPointOfOthers(AbcMobilityModel):
    form_subsection_layout = FormSubSection(id="mid_point_of_others_parameters_subsection").add_line(
        FormSectionLine().add_field(
            FormSectionNumberPairField(
                id="mid_point_of_others_waypoint_radius_range",
                label="Waypoint radius range",
                name="waypoint_radius_range",
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The range of waypoint radius that the node can assume to move in unit of length. (min, max)",
                ),
                min_left_value=0,
                min_right_value=0,
                right_should_be_gte_left=True,
                occuped_columns=12
            )
        )
    )
    
    def __init__(self, parameters: MidPointOfOthersParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

        self.__direction = random.random() * pi * 2
        self.__radius = random.random(
        ) * (self.radius_range[1] - self.radius_range[0]) + self.radius_range[0]

    def check_parameters(self, parameters):
        if ('waypoint_radius_range' not in parameters or
            not isinstance(parameters['waypoint_radius_range'], list) or
            len(parameters['waypoint_radius_range']) != 2 or
            (not isinstance(parameters['waypoint_radius_range'][0], float) and not isinstance(parameters['waypoint_radius_range'][0], int)) or
            (not isinstance(parameters['waypoint_radius_range'][1], float) and not isinstance(parameters['waypoint_radius_range'][1], int)) or
            parameters['waypoint_radius_range'][0] < 0 or
            parameters['waypoint_radius_range'][1] < 0 or
                parameters['waypoint_radius_range'][0] > parameters['waypoint_radius_range'][1]):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: MidPointOfOthersParameters = parameters

        self.radius_range = parsed_parameters['waypoint_radius_range']

    def get_next_position(self, node):
        midpoint: list[float] = [0, 0]
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
