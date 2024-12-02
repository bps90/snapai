# GENERATED WITH HELP FROM CHATGPT


import logging
from datetime import datetime
from .defaults.default_custom_global import DefaultCustomGlobal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models.abc_message_transmission_model import AbcMessageTransmissionModel
    from .abc_custom_global import AbcCustomGlobal

class Global:
    is_running = False
    is_even_round = False
    start_time: datetime = None
    start_time_of_round: datetime = None
    log: logging.Logger = None 
    number_of_messages_in_this_round: int = 0
    number_of_messages_over_all: int = 0
    current_time: int = 0
    message_transmission_model: 'AbcMessageTransmissionModel' = None # TODO: Pensar em como deixar isso de forma não-global
    custom_global: 'AbcCustomGlobal' = DefaultCustomGlobal()
    project_name: str = ""
    is_gui_mode: bool = False
    
    @staticmethod
    def reset():
        Global.is_running = False
        Global.is_even_round = False
        Global.start_time = None
        Global.start_time_of_round = None
        Global.log = None 
        Global.number_of_messages_in_this_round = 0
        Global.number_of_messages_over_all = 0
        Global.current_time = 0
        Global.message_transmission_model = None
        Global.custom_global = DefaultCustomGlobal()
        Global.project_name = ""
        Global.is_gui_mode = False
        