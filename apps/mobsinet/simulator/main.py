# THIS FILE IS TEMPORARY AND SHOULD BE REMOVED AFTERWARDS

from .global_vars import Global
from .network_simulator import simulation
from .tools.models_normalizer import ModelsNormalizer
from .configuration.sim_config import config, SimulationConfig
from importlib import import_module
import logging
from time import sleep
from .asynchronous_thread import AsynchronousThread
from .tools.event import Event


class Main:
    @staticmethod
    def init(project_name: str):
        simulation.reset()
        Global.reset()

        Global.project_name = project_name
        config.load_from_file(
            f'apps/mobsinet/simulator/projects/{project_name}/config.json')

        Global.is_async_mode = config.asynchronous
        Global.message_transmission_model = ModelsNormalizer.normalize_message_transmission_model(
            None)  # Default message transmission model
        Event.next_id = 1
        try:
            Global.custom_global = import_module(SimulationConfig.PROJECTS_DIR.replace(
                '/', '.') + project_name + '.custom_global').CustomGlobal()
        except Exception as e:
            print('No custom global', e)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        console_handler.setFormatter(formatter)

        logging.basicConfig(filename='example.log',
                            encoding='utf-8', level=logging.DEBUG, filemode='w')
        Global.log = logging.getLogger(Global.project_name)
        Global.log.handlers.clear()
        Global.log.addHandler(console_handler)

        Global.log.info('Starting simulation...')

        Global.custom_global.check_project_requirements()

        simulation.add_project_nodes()

        if (Global.is_async_mode and len(simulation.nodes()) > 0):
            AsynchronousThread.reevaluate_connections()

        simulation.pre_run()


if __name__ == "__main__":
    Main.init('sample1')

    while True:
        sleep(1)
