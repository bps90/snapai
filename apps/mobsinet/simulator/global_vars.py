# GENERATED WITH HELP FROM CHATGPT


import logging
from datetime import datetime
from .defaults.default_custom_global import DefaultCustomGlobal
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .models.abc_message_transmission_model import AbcMessageTransmissionModel
    from .abc_custom_global import AbcCustomGlobal


class Global:
    is_running = False
    is_even_round = False
    is_async_mode = False
    start_time: Optional[datetime] = None
    start_time_of_round: Optional[datetime] = None
    log: logging.Logger = logging.getLogger('NOT CONFIGURED LOGGER')
    number_of_messages_in_this_round: int = 0
    number_of_messages_over_all: int = 0
    current_time: int = 0
    # TODO: Pensar em como deixar isso de forma não-global
    message_transmission_model: Optional['AbcMessageTransmissionModel'] = None
    custom_global: 'AbcCustomGlobal' = DefaultCustomGlobal()
    project_name: Optional[str] = None
    is_gui_mode: bool = False
    round_logs: list[str] = []
    tracefile_suffix = ''

    @staticmethod
    def reset():
        Global.is_running = False
        Global.is_even_round = False
        Global.is_async_mode = False
        Global.start_time = None
        Global.start_time_of_round = None
        Global.log = logging.getLogger('NOT CONFIGURED LOGGER')
        Global.number_of_messages_in_this_round = 0
        Global.number_of_messages_over_all = 0
        Global.current_time = 0
        Global.message_transmission_model = None
        Global.custom_global = DefaultCustomGlobal()
        Global.project_name = ""
        Global.is_gui_mode = False
        Global.round_logs = []
        Global.tracefile_suffix = ''

        Global.reset_log_configuration()

    @staticmethod
    def reset_log_configuration():
        Global.log.handlers.clear()

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logging.basicConfig()

        Global.log.addHandler(console_handler)


Global.reset_log_configuration()
