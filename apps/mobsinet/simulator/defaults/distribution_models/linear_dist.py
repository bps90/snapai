from ...models.abc_distribution_model import AbcDistributionModel
from ...tools.position import Position
from ...configuration.sim_config import config

config.distribution_model_parameters = config.distribution_model_parameters


class LinearDist(AbcDistributionModel):
    def __init__(self):
        super().__init__('LinearDist')
        self.orientation = config.distribution_model_parameters['orientation']
        self.length = config.dimX if self.orientation == 'horizontal' else config.dimY
        self.line_position = config.distribution_model_parameters['line_position'] if 'line_position' in config.distribution_model_parameters and config.distribution_model_parameters['line_position'] is not None else (
            config.dimY / 2 if self.orientation == 'horizontal' else config.dimX / 2
        )
        self.number_of_nodes: int = 0

        self._last_position: Position | None = None
        self._separation: float = None
        
        self.set_number_of_nodes(config.distribution_model_parameters['number_of_nodes'])

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
            middle = config.dimX / \
                2 if self.number_of_nodes % 2 != 0 else (
                    config.dimX / 2) - (self._separation / 2)

            distance_from_middle = (
                middle) - (self._last_position.x) if self._last_position is not None else None

            if (distance_from_middle == None):
                x = middle
            elif (distance_from_middle < 0):
                x = (middle) + (distance_from_middle)
            else:
                x = (middle) + (distance_from_middle) + self._separation

            if (x < 0):
                x = 0
            if (x > config.dimX):
                x = config.dimX

            y = self.line_position
            z = 0

            position = Position(x, y, z)

            self._last_position = position

            return position
        else:
            middle = config.dimY / \
                2 if self.number_of_nodes % 2 != 0 else (
                    config.dimY / 2) - (self._separation / 2)

            distance_from_middle = (
                middle) - (self._last_position.y) if self._last_position is not None else None

            if (distance_from_middle == None):
                y = middle
            elif (distance_from_middle < 0):
                y = (middle) + (distance_from_middle)
            else:
                y = (middle) + (distance_from_middle) + self._separation

            if (y < 0):
                y = 0
            if (y > config.dimY):
                y = config.dimY

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

        self.orientation = orientation

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
            config.dimX if self.orientation == 'horizontal' else config.dimY)
        self._separation = self.length / (self.number_of_nodes - 1)


model = LinearDist

if __name__ == '__main__':
    ld = LinearDist()

    ld.set_number_of_nodes(11)
    ld.set_length(120)
    ld.set_orientation('vertical')

    for i in range(10):
        position = ld.get_position()

        print(position)
