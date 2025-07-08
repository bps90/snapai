from ...models.abc_message_transmission_model import AbcMessageTransmissionModel
from ...models.nodes.abc_node import AbcNode
from ...models.nodes.packet import Packet
from typing import TypedDict
from ...configuration.layout.form_section import FormSubSection, FormSectionLine, FormSectionNumberField, FormSectionFieldInformative


class ConstantTimeParameters(TypedDict):
    time: float


class ConstantTime(AbcMessageTransmissionModel):
    form_subsection_layout = FormSubSection(id="constant_time_parameters_subsection").add_line(
        FormSectionLine().add_field(
            FormSectionNumberField(
                id="constant_time_time",
                label="Time",
                name="time",
                occuped_columns=12,
                is_float=True,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The time that the packet will take to reach the destination node.",
                )
            )
        )
    )

    def __init__(self, parameters: ConstantTimeParameters, *args, **kwargs):
        super().__init__(parameters, *args, **kwargs)
        self.set_parameters(parameters)

    def check_parameters(self, parameters):
        if ('time' not in parameters
                or (not isinstance(parameters['time'], float) and not isinstance(parameters['time'], int))
                or parameters['time'] < 0):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: ConstantTimeParameters = parameters
        self.time: float = parsed_parameters['time']

    def time_to_reach(
            self,
            packet: Packet,
            origin_node: AbcNode,
            destination_node: AbcNode) -> float:
        """Determines the time that the packet will take to reach the destination node.

        On this model, the time is a constant defined in the configuration or setted directly on the model object.

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

        return self.time

    def set_time(self, time: float):
        """Set the time that the packet will take to reach the destination node.

        Parameters
        ----------
        time : int
            The time that the packet will take to reach the destination node.
        """

        self.time = time


model = ConstantTime
