# GENERATED WITH HELP FROM CHATGPT



from datetime import datetime
from .models.abc_message_transmission_model import AbcMessageTransmissionModel
from .defaults.default_custom_global import DefaultCustomGlobal
from .abc_custom_global import AbcCustomGlobal

class Global:
    is_running = False
    is_even_round = False
    start_time: datetime = None
    start_time_of_round: datetime = None
    # log: Logging = None # TODO: Implementar Logging
    number_of_messages_in_this_round: int = 0
    number_of_messages_over_all: int = 0
    current_time: int = 0
    message_transmission_model: AbcMessageTransmissionModel = None # TODO: Pensar em como deixar isso de forma não-global
    custom_global: 'AbcCustomGlobal' = DefaultCustomGlobal()
    use_project: bool = False
    project_name: str = ""
    is_gui_mode: bool = False
