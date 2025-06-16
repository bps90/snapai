from ...models.abc_distribution_model import AbcDistributionModel
from ...tools.position import Position
import utm  # type: ignore
from typing import Optional, TypedDict
from ...configuration.sim_config import SimulationConfig


class FromTrace2DInMemoryParameters(TypedDict):
    trace_file: str
    is_lat_long: bool
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
        self.__min_trace_x: Optional[float] = None
        self.__max_trace_x: Optional[float] = None
        self.__min_trace_y: Optional[float] = None
        self.__max_trace_y: Optional[float] = None
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
                timestamp, x, y, id = list(
                    map(float, line.split(',')))
                if (timestamp == 0):
                    self.__trace.append([timestamp, x, y, id])

                if (self.__min_trace_x is None or x < self.__min_trace_x):
                    self.__min_trace_x = x
                if (self.__max_trace_x is None or x > self.__max_trace_x):
                    self.__max_trace_x = x
                if (self.__min_trace_y is None or y < self.__min_trace_y):
                    self.__min_trace_y = y
                if (self.__max_trace_y is None or y > self.__max_trace_y):
                    self.__max_trace_y = y

        if (self.is_lat_long):
            self.__min_trace_x, self.__min_trace_y = utm.from_latlon(
                self.__min_trace_x, self.__min_trace_y)
            self.__max_trace_x, self.__max_trace_y = utm.from_latlon(
                self.__max_trace_x, self.__max_trace_y)

        self.__trace.sort(key=lambda x: x[3])  # sort by id

    def get_position(self):
        """
        Get the position of the node.

        Returns
        -------
        Position
            The position of the node.
        """

        if (self.__trace is None or
            self.__min_trace_x is None or
            self.__max_trace_x is None or
            self.__min_trace_y is None or
                self.__max_trace_y is None):
            raise ValueError("Trace not loaded. Please load a trace first.")

        if (self.__max_trace_x > SimulationConfig.dim_x[1] or
            self.__max_trace_y > SimulationConfig.dim_y[1] or
            self.__min_trace_x < SimulationConfig.dim_x[0] or
                self.__min_trace_y < SimulationConfig.dim_y[0]):
            raise ValueError("Trace coordinates exceed simulation dimensions.")

        _, current_x, current_y, _ = self.__trace[self.__trace_index]
        self.__trace_index += 1

        x, y = utm.from_latlon(current_x, current_y)[
            0:2] if self.is_lat_long else [current_x, current_y]

        if (self.addapt_to_dimensions):
            x = (x - self.__min_trace_x) / \
                (self.__max_trace_x - self.__min_trace_x) * \
                (SimulationConfig.dim_x[1] - SimulationConfig.dim_x[0])
            y = (y - self.__min_trace_y) / \
                (self.__max_trace_y - self.__min_trace_y) * \
                (SimulationConfig.dim_y[1] - SimulationConfig.dim_y[0])

        position = Position(x, y)

        return position


model = FromTrace2DInMemory
