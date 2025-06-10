from ...models.abc_distribution_model import AbcDistributionModel
from ...tools.position import Position
import utm  # type: ignore
from typing import Any, Optional, cast, TypedDict
from ...configuration.sim_config import SimulationConfig


class FromTrace2DInMemoryParameters(TypedDict):
    trace_file: str
    is_lat_long: bool
    should_padding: bool
    addapt_to_dimensions: bool


class FromTrace2DInMemory(AbcDistributionModel):
    """
    Class to generate 2D distributions from a trace in memory.
    """

    def __init__(self, parameters: FromTrace2DInMemoryParameters, *args, **kwargs):
        """
        Initialize the FromTrace2DInMemory class.

        Args:
            trace: The trace data to be used for generating the distribution.
        """
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

        self.__trace: Optional[list[list[float]]] = None
        self.__min_x: Optional[float] = None
        self.__max_x: Optional[float] = None
        self.__min_y: Optional[float] = None
        self.__max_y: Optional[float] = None
        self.__trace_index = 0

        self.load_trace(self.trace_file)

    def check_parameters(self, parameters):
        if (
            'trace_file' not in parameters or
            not isinstance(parameters['trace_file'], str) or
                parameters['trace_file'] == '' or
                not parameters['trace_file'].endswith('.csv')):
            return False

        if (
            'is_lat_long' not in parameters or
            not isinstance(parameters['is_lat_long'], bool)
        ):
            return False

        if (
            'should_padding' not in parameters or
            not isinstance(parameters['should_padding'], bool)
        ):
            return False

        if (
            'addapt_to_dimensions' not in parameters or
            not isinstance(parameters['addapt_to_dimensions'], bool)
        ):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: FromTrace2DInMemoryParameters = parameters
        self.trace_file: str = parsed_parameters['trace_file']
        self.is_lat_long: bool = parsed_parameters['is_lat_long']
        self.should_padding: bool = parsed_parameters['should_padding']
        self.addapt_to_dimensions: bool = parsed_parameters[
            'addapt_to_dimensions']

    def set_lat_long(self, is_lat_long: bool):
        """
        Set whether the trace is in latitude/longitude format.

        Parameters
        ----------
        is_lat_long : bool
            True if the trace is in latitude/longitude format, False otherwise.
        """
        self.is_lat_long = is_lat_long

    def set_should_padding(self, should_padding: bool):
        """
        Set whether the trace should be padded to the simulation dimensions.

        Parameters
        ----------
        should_padding : bool
            True if the trace should be padded, False otherwise.
        """
        self.should_padding = should_padding

    def set_addapt_to_dimensions(self, addapt_to_dimensions: bool):
        """
        Set whether the trace should be addapted to the simulation dimensions.

        Parameters
        ----------
        addapt_to_dimensions : bool
            True if the trace should be addapted to the simulation dimensions, False otherwise.
        """
        self.addapt_to_dimensions = addapt_to_dimensions

    def load_trace(self, filename: str):
        """
        Load a trace file and parse it into a list of positions.

        The trace file should be a CSV file with the following format:
        `timestamp, x, y, id` or `timestamp, lat, long, id`

        Parameters
        ----------
        filename : str
            The path to the trace file.


        """
        self.__trace = []
        with open(filename, 'r') as f:

            for line in f.readlines()[1:]:
                splitted_line = list(map(float, line.split(',')))
                if (splitted_line[0] == 0):
                    self.__trace.append(splitted_line)

                if (self.__min_x is None or splitted_line[1] < self.__min_x):
                    self.__min_x = splitted_line[1]
                if (self.__max_x is None or splitted_line[1] > self.__max_x):
                    self.__max_x = splitted_line[1]
                if (self.__min_y is None or splitted_line[2] < self.__min_y):
                    self.__min_y = splitted_line[2]
                if (self.__max_y is None or splitted_line[2] > self.__max_y):
                    self.__max_y = splitted_line[2]

        self.__trace.sort(key=lambda x: x[3])

    def get_position(self):
        """
        Get the position of the node.

        Returns
        -------
        Position
            The position of the node.
        """

        if self.__trace is None:
            raise ValueError("Trace not loaded. Please load a trace first.")

        if (self.should_padding and not self.addapt_to_dimensions):
            raise ValueError(
                "Should padding must be false if addapt to dimensions is false.")

        if self.__min_x is None or self.__max_x is None or self.__min_y is None or self.__max_y is None:
            raise ValueError("Trace not loaded. Please load a trace first.")

        if (self.is_lat_long):
            max_x = self.__max_x - self.__min_x
            max_y = self.__max_y - self.__min_y
        else:
            max_x = self.__max_x
            max_y = self.__max_y

        if max_x > SimulationConfig.dim_x or max_y > SimulationConfig.dim_y:
            raise ValueError("Trace coordinates exceed simulation dimensions.")

        corresponding_position: list[float] = self.__trace[self.__trace_index]
        self.__trace_index += 1

        if self.is_lat_long:
            # Convert latitude/longitude to x/y
            x, y, _, _ = utm.from_latlon(
                corresponding_position[1], corresponding_position[2])

            if (self.should_padding):
                x = (x - self.__min_x) / \
                    (self.__max_x - self.__min_x) * \
                    SimulationConfig.dim_x * 0.9 + SimulationConfig.dim_x * 0.05
                y = (y - self.__min_y) / \
                    (self.__max_y - self.__min_y) * \
                    SimulationConfig.dim_y * 0.9 + SimulationConfig.dim_y * 0.05
            elif (self.addapt_to_dimensions):
                x = (x - self.__min_x) / \
                    (self.__max_x - self.__min_x) * SimulationConfig.dim_x
                y = (y - self.__min_y) / \
                    (self.__max_y - self.__min_y) * SimulationConfig.dim_y

        else:
            # Use x/y directly
            if (self.should_padding):
                x = corresponding_position[1] / (self.__max_x) * \
                    SimulationConfig.dim_x * 0.9 + SimulationConfig.dim_x * 0.05
                y = corresponding_position[2] / (self.__max_y) * \
                    SimulationConfig.dim_y * 0.9 + SimulationConfig.dim_y * 0.05
            elif (self.addapt_to_dimensions):
                x = corresponding_position[1] / \
                    (self.__max_x) * SimulationConfig.dim_x
                y = corresponding_position[2] / \
                    (self.__max_y) * SimulationConfig.dim_y
            else:
                x = corresponding_position[1]
                y = corresponding_position[2]

        position = Position(x, y)

        return position


model = FromTrace2DInMemory
