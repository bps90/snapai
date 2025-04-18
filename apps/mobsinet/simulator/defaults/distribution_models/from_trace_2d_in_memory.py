from ...models.abc_distribution_model import AbcDistributionModel
from ...configuration.sim_config import config
from ...tools.position import Position


class FromTrace2DInMemory(AbcDistributionModel):
    """
    Class to generate 2D distributions from a trace in memory.
    """

    def __init__(self):
        """
        Initialize the FromTrace2DInMemory class.

        Args:
            trace: The trace data to be used for generating the distribution.
        """
        super().__init__('FromTrace2DInMemory')
        self.__trace: list[list[float]] = None
        self.is_lat_long = config.distribution_model_parameters.get(
            'is_lat_long', False)
        self.should_padding = config.distribution_model_parameters.get(
            'should_padding', False
        )
        self.__min_x = None
        self.__max_x = None
        self.__min_y = None
        self.__max_y = None
        self.__trace_index = 0

        self.load_trace(
            config.distribution_model_parameters.get('trace_file'))

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
                line = list(map(float, line.split(',')))
                if (line[0] == 0):
                    self.__trace.append(line)

                if (self.__min_x is None or line[1] < self.__min_x):
                    self.__min_x = line[1]
                if (self.__max_x is None or line[1] > self.__max_x):
                    self.__max_x = line[1]
                if (self.__min_y is None or line[2] < self.__min_y):
                    self.__min_y = line[2]
                if (self.__max_y is None or line[2] > self.__max_y):
                    self.__max_y = line[2]
        self.__trace.sort(key=lambda x: x[3])

    def get_position(self):
        """
        Get the position of the node.

        Returns
        -------
        Position
            The position of the node.
        """
        print(f"Trace index: {self.__trace_index}")
        if self.__trace is None:
            raise ValueError("Trace not loaded. Please load a trace first.")

        if (self.is_lat_long):
            max_x = self.__max_x - self.__min_x
            max_y = self.__max_y - self.__min_y
        else:
            max_x = self.__max_x
            max_y = self.__max_y

        if max_x > config.dimX or max_y > config.dimY:
            raise ValueError("Trace coordinates exceed simulation dimensions.")

        corresponding_position: list[float] = self.__trace[self.__trace_index]
        self.__trace_index += 1

        if self.is_lat_long:
            # Convert latitude/longitude to x/y
            lat = corresponding_position[1]
            long = corresponding_position[2]
            if (self.should_padding):
                x = (lat - self.__min_x) / \
                    (self.__max_x - self.__min_x) * \
                    config.dimX * 0.9 + config.dimX * 0.05
                y = (long - self.__min_y) / \
                    (self.__max_y - self.__min_y) * \
                    config.dimY * 0.9 + config.dimY * 0.05
            else:
                x = (lat - self.__min_x) / \
                    (self.__max_x - self.__min_x) * config.dimX
                y = (long - self.__min_y) / \
                    (self.__max_y - self.__min_y) * config.dimY

        else:
            # Use x/y directly
            if (self.should_padding):
                x = corresponding_position[1] / (self.__max_x) * \
                    config.dimX * 0.9 + config.dimX * 0.05
                y = corresponding_position[2] / (self.__max_y) * \
                    config.dimY * 0.9 + config.dimY * 0.05
            else:
                x = corresponding_position[1] / (self.__max_x) * config.dimX
                y = corresponding_position[2] / (self.__max_y) * config.dimY

        position = Position(x, y)

        return position


model = FromTrace2DInMemory
