from math import cos, pi, sin
from typing import Literal, Tuple, TypedDict

from ...models.abc_distribution_model import AbcDistributionModel
from ...tools.position import Position
from ...configuration.sim_config import SimulationConfig
from ...configuration.layout.form_section import FormSubSection, FormSectionLine, FormSectionNumberField, FormSectionFieldInformative, FormSectionSelectField, FormSectionNumberPairField


class CircularDistParameters(TypedDict):
    radius: float
    rotation_direction: Literal['clockwise', 'anti-clockwise']
    midpoint: list[float]
    number_of_nodes: int


class CircularDist(AbcDistributionModel):
    form_subsection_layout = FormSubSection(id='circular_dist_parameters_subsection').add_lines([
        FormSectionLine().add_fields([
            FormSectionNumberField(
                id="circular_dist_radius",
                label="Radius",
                name="radius",
                occuped_columns=3,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The distance from the midpoint to the edge of the circle.",
                ),
            ),
            FormSectionSelectField(
                id="circular_dist_rotation_direction",
                label="Rotation Direction",
                name="rotation_direction",
                occuped_columns=3,
                options=[
                    {'label': 'Clockwise ↻', 'value': 'clockwise'},
                    {'label': 'Anti-Clockwise ↺', 'value': 'anti-clockwise'},
                ],
                required=True,
                informative=FormSectionFieldInformative(
                    title="The rotation direction that the circle will be generated. (Useful only if the number of nodes for the model is not equal to the number of nodes in the simulation.)",
                ),
            ),
            FormSectionNumberPairField(
                id="circular_dist_midpoint",
                label="Midpoint",
                name="midpoint",
                occuped_columns=3,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The center of the circle. (X and Y coordinates only.)",
                ),
            ),
            FormSectionNumberField(
                id="circular_dist_number_of_nodes",
                label="Number of Nodes",
                name="number_of_nodes",
                occuped_columns=3,
                is_float=False,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The number of nodes for the model.",
                ),
            ),
        ])
    ])

    def __init__(self, parameters: CircularDistParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)

        self.set_parameters(parameters)

        self._radians: float = 0

    def check_parameters(self, parameters):
        if ('radius' not in parameters or
            parameters['radius'] is None or
            parameters['radius'] < 0 or
                (type(parameters['radius']) != float and type(parameters['radius']) != int)):
            return False

        if (
            'rotation_direction' not in parameters or
            parameters['rotation_direction'] not in [
                'clockwise', 'anti-clockwise']):
            return False

        if ('midpoint' not in parameters or
            not isinstance(parameters['midpoint'], list) or
            len(parameters['midpoint']) != 2 or
            (type(parameters['midpoint'][0]) != float and type(parameters['midpoint'][0]) != int) or
                (type(parameters['midpoint'][1]) != float and type(parameters['midpoint'][1]) != int)):
            return False

        if ('number_of_nodes' not in parameters or
            parameters['number_of_nodes'] is None or
            parameters['number_of_nodes'] < 0 or
                type(parameters['number_of_nodes']) != int):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: CircularDistParameters = parameters
        self.radius: float = parsed_parameters['radius']
        self.rotation_direction: Literal['clockwise',
                                         'anti-clockwise'] = parsed_parameters['rotation_direction']
        self.midpoint: list[float] = parsed_parameters['midpoint']
        self.number_of_nodes: int = parsed_parameters['number_of_nodes']

    def get_position(self) -> Position:
        """Get the next position for the node in the distribution.

        Raises
        ------
        ValueError
            If the radius, rotation direction or midpoint is not set.

            If the radius is too large for the midpoint.

        Returns
        -------
        Position
            The next position for the node in the distribution.
        """

        if (self.radius is None):
            raise ValueError('The radius is not set.')

        if (self.rotation_direction is None):
            raise ValueError('The rotation direction is not set.')

        if (self.midpoint is None):
            raise ValueError('The midpoint is not set.')

        if (self.midpoint[0] - self.radius < SimulationConfig.dim_x[0] or
            self.midpoint[0] + self.radius > SimulationConfig.dim_x[1] or
            self.midpoint[1] - self.radius < SimulationConfig.dim_y[0] or
                self.midpoint[1] + self.radius > SimulationConfig.dim_y[1]):
            raise ValueError('The radius is too large for the midpoint.')

        new_coordinates = self._get_new_coordinates()

        self._radians += 2 * pi / self.number_of_nodes

        position = Position(*new_coordinates)

        return position

    def _get_new_coordinates(self) -> Tuple[float, float, float]:
        """(private) Get the next coordinates for the node in the distribution."""

        return (
            self.midpoint[0] + self.radius * cos(self._radians),
            self.midpoint[1] + self.radius * (sin(
                self._radians) if self.rotation_direction == 'anti-clockwise' else -sin(self._radians)),
            0
        )

    def set_number_of_nodes(self, number_of_nodes: int):
        """Set the number of nodes that will be distributed.

        Also calculates the separation between nodes.
        """

        self.number_of_nodes = number_of_nodes

        self._radians = 0

    def set_rotation_direction(self, rotation_direction: Literal['anti-clockwise', 'clockwise']):
        """Set the rotation direction of the nodes.

        Parameters
        ----------
        rotation_direction : str
            The rotation direction. Either 'anti-clockwise' or 'clockwise'.
        """

        self.rotation_direction = rotation_direction

    def set_radius(self, radius: float):
        """Set the radius of the circle.

        Parameters
        ----------
        radius : float
            The radius in unit of length.

        Raises
        ------
        ValueError
            If the radius is negative.
        """

        if (radius < 0):
            raise ValueError('The radius must be positive.')

        self.radius = radius

    def set_midpoint(self, midpoint: Position):
        """Set the midpoint of the circle.

        Parameters
        ----------
        midpoint : Position
            The midpoint of the circle.
        """

        self.midpoint = midpoint.get_coordinates()


model = CircularDist
