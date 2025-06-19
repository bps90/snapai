from ...models.abc_distribution_model import AbcDistributionModel
from ...tools.position import Position
from ...configuration.sim_config import SimulationConfig
from typing import Literal, TypedDict, cast
from ...configuration.layout.form_section import FormSubSection, FormSectionLine,  FormSectionNumberField, FormSectionFieldInformative, FormSectionSelectField


class LinearDistParameters(TypedDict):
    orientation: Literal['horizontal', 'vertical']
    line_position: float
    number_of_nodes: int


class LinearDist(AbcDistributionModel):
    form_subsection_layout = FormSubSection('linear_dist_parameters_subsection').add_line(
        FormSectionLine().add_fields([
            FormSectionSelectField(
                id="linear_dist_orientation",
                label="Orientation",
                name="orientation",
                occuped_columns=4,
                options=[
                    {'value': 'horizontal', 'label': 'Horizontal'},
                    {'value': 'vertical', 'label': 'Vertical'},
                ],
                required=True,
                informative=FormSectionFieldInformative(
                    title="The orientation of the line.",
                ),
            ),
            FormSectionNumberField(
                id="linear_dist_line_position",
                label="Line Position",
                name="line_position",
                occuped_columns=4,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The position of the line. Coordinate X if orientation is vertical, coordinate Y if vertical.",
                ),
            ),
            FormSectionNumberField(
                id="linear_dist_number_of_nodes",
                label="Number of Nodes",
                name="number_of_nodes",
                occuped_columns=4,
                is_float=False,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The number of nodes to be placed. The nodes will be placed evenly from the center to the edges of the line.",
                ),
            ),
        ])
    )

    def __init__(self, parameters: LinearDistParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)
        self.length = (SimulationConfig.dim_x[1] - SimulationConfig.dim_x[0]) if self.orientation == 'horizontal' else (
            SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0])
        self._last_position: Position | None = None
        self._separation: float = self.length / (self.number_of_nodes - 1)

    def check_parameters(self, parameters):
        if ('orientation' not in parameters or
                parameters['orientation'] not in ['horizontal', 'vertical']):
            return False

        if ('line_position' not in parameters or
            parameters['line_position'] is None or
                (type(parameters['line_position']) != float and type(parameters['line_position']) != int)):
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

        parsed_parameters: LinearDistParameters = parameters
        self.orientation: Literal['horizontal',
                                  'vertical'] = parsed_parameters['orientation']
        self.line_position: float = parsed_parameters['line_position']
        self.number_of_nodes: int = parsed_parameters['number_of_nodes']

    def get_position(self):
        """Get the next position for the node in the distribution.

        Raises
        ------
        Exception
            If the number of nodes is not set.
        """

        if not self.number_of_nodes:
            raise Exception(
                'The number of nodes must be set before getting the position. Use the set_number_of_nodes() method.')

        if (self.orientation == 'horizontal'):
            middle = (SimulationConfig.dim_x[1] - SimulationConfig.dim_x[0]) / \
                2 if self.number_of_nodes % 2 != 0 else (
                    (SimulationConfig.dim_x[1] - SimulationConfig.dim_x[0]) / 2) - (self._separation / 2)

            distance_from_middle = (
                middle) - (self._last_position.x) if self._last_position is not None else None

            if (distance_from_middle is None):
                x = middle
            elif (distance_from_middle < 0):
                x = (middle) + (distance_from_middle)
            else:
                x = (middle) + (distance_from_middle) + self._separation

            if (x < SimulationConfig.dim_x[0]):
                x = SimulationConfig.dim_x[0]
            if (x > SimulationConfig.dim_x[1]):
                x = SimulationConfig.dim_x[1]

            y = self.line_position
            z = 0

            position = Position(x, y, z)

            self._last_position = position

            return position
        else:
            middle = (SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0]) / \
                2 if self.number_of_nodes % 2 != 0 else (
                    (SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0]) / 2) - (self._separation / 2)

            distance_from_middle = (
                middle) - (self._last_position.y) if self._last_position is not None else None

            if (distance_from_middle is None):
                y = middle
            elif (distance_from_middle < 0):
                y = (middle) + (distance_from_middle)
            else:
                y = (middle) + (distance_from_middle) + self._separation

            if (y < SimulationConfig.dim_y[0]):
                y = SimulationConfig.dim_y[0]
            if (y > SimulationConfig.dim_y[1]):
                y = SimulationConfig.dim_y[1]

            x = self.line_position
            z = 0

            position = Position(x, y, z)

            self._last_position = position

            return position

    def set_number_of_nodes(self, number_of_nodes: int):
        """Set the number of nodes that will be distributed. Also calculates the separation between nodes."""
        self.number_of_nodes = number_of_nodes
        self._separation = self.length / (number_of_nodes - 1)

    def set_line_position(self, line_position: float):
        """Set the position of the line in the distribution."""
        self.line_position = line_position

    def set_orientation(self, orientation: str):
        """Set the orientation of the distribution.

        Parameters
        ----------
        orientation : str
            The orientation of the distribution. Must be either "horizontal" or "vertical".

        Raises
        ------
        Exception
            If the orientation is not "horizontal" or "vertical".
        """
        if orientation not in ['horizontal', 'vertical']:
            raise Exception(
                'The orientation must be either "horizontal" or "vertical"')

        self.orientation = cast(Literal['horizontal', 'vertical'], orientation)

    def set_length(self, length: float):
        """Set the length of the distribution. Also calculates the separation between nodes.

        Parameters
        ----------
        length : float
            The length of the distribution.
            Can't be greater than the simulation area.
            If the length is greater than the simulation area, it will be set to the simulation area.
            If the area is retangular, maybe use `set_orientation()` before setting the length.
        """

        self.length = min(
            length,
            (SimulationConfig.dim_x[1] - SimulationConfig.dim_x[0]) if self.orientation == 'horizontal' else (
                SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0]))
        self._separation = self.length / (self.number_of_nodes - 1)


model = LinearDist
