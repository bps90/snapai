from .global_vars import Global
from .network_simulator import simulation
from .tools.models_search_engine import ModelsSearchEngine
from .configuration.sim_config import SimulationConfig
from .configuration.base_config import BaseConfig
from importlib import import_module
import logging
from time import sleep
from .asynchronous_thread import AsynchronousThread
from .tools.event import Event
from typing import cast
from .models.abc_model import AbcModelParameters
from .defaults.default_custom_global import DefaultCustomGlobal


class Main:
    @staticmethod
    def init(project_name: str):
        """Initializes the simulation

        Args:
            project_name (str): _description_

        Raises:
            NoCustomGlobalException: _description_
        """
        Main.__reset_variables()

        SimulationConfig.load_from_file(
            f'{SimulationConfig.PROJECTS_DIR}{project_name}/config.json')

        try:
            ProjectConfig: BaseConfig = import_module(SimulationConfig.PROJECTS_DIR.replace(
                '/', '.') + project_name + '.project_config').ProjectConfig
            ProjectConfig.load_from_file(
                f'{SimulationConfig.PROJECTS_DIR}{project_name}/config.json')
        except Exception as e:
            pass

        Main.__set_global_variables(project_name)
        Main.__config_logging()

        Global.log.info('Starting simulation...')

        Global.custom_global.check_project_requirements()

        if (Global.is_async_mode and len(simulation.nodes()) > 0):
            AsynchronousThread.reevaluate_connections()

        simulation.pre_run()

    @staticmethod
    def __reset_variables():
        simulation.reset()
        Global.reset()
        Event.next_id = 1

    @staticmethod
    def __set_global_variables(project_name: str):
        """Sets the global variables for the initialization of the simulation

        Args:
            project_name (str): _description_
        """
        Global.project_name = project_name
        Global.is_async_mode = SimulationConfig.asynchronous
        # Default message transmission model
        Global.message_transmission_model = ModelsSearchEngine.find_message_transmission_model(
            None)(cast(AbcModelParameters, SimulationConfig.message_transmission_model_parameters))
        Global.log = logging.getLogger(Global.project_name)
        try:
            Global.custom_global = import_module(SimulationConfig.PROJECTS_DIR.replace(
                '/', '.') + project_name + '.custom_global').CustomGlobal()
        except Exception as e:
            Global.custom_global = DefaultCustomGlobal()

    @staticmethod
    def __config_logging():
        
        if Global.log:
            Global.log.handlers.clear()
            Global.log.setLevel(logging.DEBUG)

            formatter = logging.Formatter('[%(levelname)s:%(name)s] %(message)s')

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)

            # File handler
            file_handler = logging.FileHandler(
                'example.log', mode='w', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            # Adiciona ambos
            Global.log.addHandler(console_handler)
            Global.log.addHandler(file_handler)
        


if __name__ == "__main__":
    Main.init('sample1')

    while True:
        sleep(1)
