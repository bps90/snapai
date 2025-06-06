from ...models.abc_mobility_model import AbcMobilityModel
from typing import Literal
from ...models.nodes.abc_node import AbcNode
from ...global_vars import Global
from ...network_simulator import simulation
from ...configuration.sim_config import config
from ...tools.position import Position
import utm


class FromTrace2DInMemory(AbcMobilityModel):
    __traces: dict[str, list[list[list[float]],
                             float, float, float, float]] = {}

    def __init__(self):
        super().__init__('FromTrace2DInMemory')
        self.is_lat_long: bool = config.mobility_model_parameters.get(
            'is_lat_long', False)
        self.should_padding: bool = config.mobility_model_parameters.get(
            'should_padding', False)
        self.addapt_to_dimensions: bool = config.mobility_model_parameters.get(
            'addapt_to_dimensions', False
        )
        self.__trace_index: int = 0
        self.trace_file: str = config.mobility_model_parameters.get(
            'trace_file')

        self.load_trace(self.trace_file)

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
        if (filename not in FromTrace2DInMemory.__traces):
            FromTrace2DInMemory.__traces.__setitem__(
                filename, [[], None, None, None, None])
        else:
            return
        with open(filename, 'r') as f:

            for line in f.readlines()[1:]:
                line = list(map(float, line.split(',')))
                FromTrace2DInMemory.__traces[filename][0].append(line)

                min_x = FromTrace2DInMemory.__traces[filename][1]
                max_x = FromTrace2DInMemory.__traces[filename][2]
                min_y = FromTrace2DInMemory.__traces[filename][3]
                max_y = FromTrace2DInMemory.__traces[filename][4]

                if (min_x is None or line[1] < min_x):
                    FromTrace2DInMemory.__traces[filename][1] = line[1]
                if (max_x is None or line[1] > max_x):
                    FromTrace2DInMemory.__traces[filename][2] = line[1]
                if (min_y is None or line[2] < min_y):
                    FromTrace2DInMemory.__traces[filename][3] = line[2]
                if (max_y is None or line[2] > max_y):
                    FromTrace2DInMemory.__traces[filename][4] = line[2]

        FromTrace2DInMemory.__traces[filename][0].sort(key=lambda x: x[0])

    def get_next_position(self, node: AbcNode):
        """Return the next position for the node.

        Parameters
        ----------
        node : AbcNode
            The node object.
        """
        if self.trace_file not in FromTrace2DInMemory.__traces:
            raise ValueError(
                "Trace not loaded. Please load a trace file first.")

        if (self.should_padding and not self.addapt_to_dimensions):
            raise ValueError(
                "Should padding must be false if addapt to dimensions is false.")

        trace_data = FromTrace2DInMemory.__traces[self.trace_file]

        """
        trace_data[0] is the list of positions
        trace_data[1] is the min x
        trace_data[2] is the max x
        trace_data[3] is the min y
        trace_data[4] is the max y
        """
        if (self.is_lat_long):
            max_x = trace_data[2] - trace_data[1]
            max_y = trace_data[4] - trace_data[3]
        else:
            max_x = trace_data[2]
            max_y = trace_data[4]

        if max_x > config.dimX or max_y > config.dimY:
            raise ValueError("Trace coordinates exceed simulation dimensions.")

        corresponding_position: list[float] = None

        for i in range(self.__trace_index, len(trace_data[0])):
            line = trace_data[0][i]
            if (line[0] > Global.current_time):
                break
            if (line[3] == node.id and line[0] == Global.current_time):
                corresponding_position = line
                self.__trace_index = i
                break

        if (corresponding_position is None):
            return node.position.copy()

        if self.is_lat_long:
            x, y, _, _ = utm.from_latlon(
                corresponding_position[1], corresponding_position[2])

            if (self.should_padding):
                x = (x - trace_data[1]) / \
                    (trace_data[2] - trace_data[1]) * \
                    config.dimX * 0.9 + (config.dimX * 0.05)
                y = (y - trace_data[3]) / \
                    (trace_data[4] - trace_data[3]) * \
                    config.dimY * 0.9 + (config.dimY * 0.05)
            elif (self.addapt_to_dimensions):
                x = (x - trace_data[1]) / \
                    (trace_data[2] - trace_data[1]) * config.dimX
                y = (y - trace_data[3]) / \
                    (trace_data[4] - trace_data[3]) * config.dimY

        else:
            if (self.should_padding):
                x = corresponding_position[1] / \
                    (trace_data[2]) * config.dimX * 0.9 + (config.dimX * 0.05)
                y = corresponding_position[2] / \
                    (trace_data[4]) * config.dimY * 0.9 + (config.dimY * 0.05)
            elif (self.addapt_to_dimensions):
                x = corresponding_position[1] / \
                    (trace_data[2]) * config.dimX
                y = corresponding_position[2] / \
                    (trace_data[4]) * config.dimY
            else:
                x = corresponding_position[1]
                y = corresponding_position[2]

        position = Position(x, y)

        return position


model = FromTrace2DInMemory
