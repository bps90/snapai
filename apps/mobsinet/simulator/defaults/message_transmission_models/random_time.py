import random
from ...models.abc_message_transmission_model import AbcMessageTransmissionModel
from ...models.nodes.abc_node import AbcNode
from ...models.nodes.packet import Packet
from typing import TypedDict


class RandomTimeParameters(TypedDict):
    time_range: list[float]


class RandomTime(AbcMessageTransmissionModel):
    def __init__(self, parameters: RandomTimeParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

    def check_parameters(self, parameters):
        if ('time_range' not in parameters or
                (not isinstance(parameters['time_range'], list)) or
                len(parameters['time_range']) != 2 or
                (not isinstance(parameters['time_range'][0], float) and not isinstance(parameters['time_range'][0], int)) or
                (not isinstance(parameters['time_range'][1], float) and not isinstance(parameters['time_range'][1], int)) or
                parameters['time_range'][0] < 0 or
                parameters['time_range'][1] < 0 or
                parameters['time_range'][0] > parameters['time_range'][1]):
            return False
        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: RandomTimeParameters = parameters
        self.time_range: list[float] = parsed_parameters['time_range']

    def time_to_reach(self,
                      packet: Packet,
                      origin_node: AbcNode,
                      destination_node: AbcNode):
        """Determines the time that the packet will take to reach the destination node.

        On this model, the time is a random number between 
        the min and max time defined in the configuration 
        or setted directly on the model object.

        Parameters
        ----------
        packet : AbcPacket
            The packet object.
        origin_node : AbcNode
            The origin node object.
        destination_node : AbcNode
            The destination node object.

        Returns
        -------
        float
            The time that the packet will take to reach the destination node.
        """

        return random.uniform(self.time_range[0], self.time_range[1])

    def set_interval(self, time_range: list[float]):
        """Set the time range for the random time model.

        Parameters
        ----------
        time_range : list[float]
            The time range in the format [min_time, max_time].
        """

        self.time_range = time_range


model = RandomTime
