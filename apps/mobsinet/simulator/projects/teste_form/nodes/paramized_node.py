from ....models.nodes.abc_node import AbcNode
from ...sample1.messages.pingpong_message import PingPongMessage
from ...sample1.timers.pingpong_timer import PingPongTimer
from ...sample1.timers.init_pingpong_timer import InitPingPongTimer
from ....tools.color import Color
from random import randint
from ....network_simulator import simulation
from ....configuration.layout.form_section import FormSubSection, FormSectionLine, FormSectionColorField, FormSectionNumberField, FormSectionFieldInformative
from typing import TypedDict, TYPE_CHECKING
from ....tools.position import Position
import math

if TYPE_CHECKING:
    from ....models.abc_mobility_model import AbcMobilityModel
    from ....models.abc_connectivity_model import AbcConnectivityModel
    from ....models.abc_interference_model import AbcInterferenceModel
    from ....models.abc_reliability_model import AbcReliabilityModel


class ParamizedNodeParameters(TypedDict):
    border_color: int


class ParamizedNode(AbcNode):
    form_subsection_layout = FormSubSection("paramized_node_parameters_subsection").add_line(
        FormSectionLine().add_fields([
            FormSectionColorField(
                id="border_color",
                name="border_color",
                label="Border Color",
                occuped_columns=4,
                required=True,
                informative=FormSectionFieldInformative(
                    title="The border color of the node.",
                ),
            ),
            FormSectionNumberField(
                id="max_simultaneous_connections",
                name="max_simultaneous_connections",
                label="Max Simultaneous Connections",
                occuped_columns=1,
                informative=FormSectionFieldInformative(
                    title="The max simultaneous connections of the node.",
                    help_text="The max simultaneous connections of the node.<br>By default, it is infinite.",
                    as_html=True
                ),
                is_float=True,
                required=False,
                min_value=0,
            ),
            FormSectionNumberField(
                id="border_angle",
                name="border_angle",
                is_angle='deg',
                informative=FormSectionFieldInformative(
                    title="The border angle of the node.",
                ),
                is_float=True,
                label="Border Angle",
                occuped_columns=3,
                required=True,
                min_value=0,
                max_value=360
            ),
            FormSectionNumberField(
                id="other_angle",
                name="other_angle",
                is_angle='rad',
                informative=FormSectionFieldInformative(
                    title="The other angle of the node.",
                ),
                is_float=False,
                label="Other Angle",
                occuped_columns=4,
                required=True,
                min_value=math.pi/5,
                max_value=math.pi*2
            )
        ])
    )
    default_parameters = True

    def __init__(self, id: int,
                 mobility_model: 'AbcMobilityModel',
                 connectivity_model: 'AbcConnectivityModel',
                 interference_model: 'AbcInterferenceModel',
                 reliability_model: 'AbcReliabilityModel',
                 color: Color = Color(0, 0, 0),
                 size: int = 1,
                 position: 'Position' = Position(),
                 parameters: ParamizedNodeParameters = {"border_color": 0}):
        super().__init__(id, mobility_model, connectivity_model,
                         interference_model, reliability_model, color, size, position, parameters)
        self.pingpong_inited = False
        self.__local_r: int = 0
        self.__local_g: int = 0
        self.__local_b: int = 0
        self.size = 10

        self.set_parameters(parameters)

        if (len(simulation.nodes()) == 0):
            init_pingpong_timer = InitPingPongTimer()
            init_pingpong_timer.start_relative(1, self)

    def init_pingpong(self):
        if (not self.pingpong_inited):
            self.pingpong_inited = True
            message = PingPongMessage()
            message.set_r(randint(0, 255))
            message.set_g(randint(0, 255))
            message.set_b(randint(0, 255))

            timer = PingPongTimer(message, 10)
            timer.start_relative(1, self)

    def handle_messages(self, inbox):
        received_from = []

        for packet in inbox.packet_list:
            message = packet.message
            if (isinstance(message, PingPongMessage) and packet.origin not in received_from):
                self.__local_r = message.get_r()
                self.__local_g = message.get_g()
                self.__local_b = message.get_b()

                self.set_color(
                    Color(self.__local_r, self.__local_g, self.__local_b))

                message.set_r(randint(0, 255))
                message.set_g(randint(0, 255))
                message.set_b(randint(0, 255))

                timer = PingPongTimer(message)
                timer.start_relative(1, self)

                received_from.append(packet.origin)

    def check_parameters(self, parameters):
        if (
            'border_color' not in parameters or
                not isinstance(parameters['border_color'], int)):
            return False

        return True

    def set_parameters(self, parameters):
        if not self.check_parameters(parameters):
            raise ValueError('Invalid parameters.')

        parsed_parameters: ParamizedNodeParameters = parameters
        self.border_color: float = parsed_parameters['border_color']

    def check_requirements(self):
        pass

    def init(self):
        pass

    def on_neighboorhood_change(self):
        pass

    def post_step(self):
        pass

    def pre_step(self):
        pass


node = ParamizedNode
