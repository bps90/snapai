# GENERATED WITH HELP FROM CHATGPT

from datetime import datetime
from threading import Thread
from .global_vars import Global
from .models.nodes.abc_node_implementation import AbcNodeImplementation
from .network_simulator import simulation


class SynchronousThread(Thread):

    def __init__(self, runtime=None):
        super().__init__()
        self.number_of_rounds = 0  # Antes de iniciar, alguem deve definir esse valor
        self.runtime = runtime  # Se estiver no modo GUI, mantém a referência ao GUIRuntime
        self.refresh_rate = 1    # Taxa de atualização da GUI

    def run(self):
        Global.is_running = True
        Global.start_time = datetime.now()

        # TODO: Colocar código existente em network_simulator.py : run()
        for current_round in range(self.number_of_rounds):
            Global.current_time += 1

            self.__round()

        Global.is_running = False

    def __round(self):
        """(private) Performs a single simulation round."""

        Global.custom_global.pre_roundx()
        Global.custom_global.handle_global_timers()
        self.__move_nodes()
        # self.__update_connections()
        # self.packets_in_the_air.test_interference()
        # self.__step_nodes()

    def __move_nodes(self):
        """(private) Moves the nodes in the network graph."""

        for node in simulation.graph.nodes():
            node_implementation: 'AbcNodeImplementation' = simulation.graph.nodes[
                node]["implementation"]

            # move the node
            node_implementation.set_position(
                node_implementation.mobility_model.get_next_position(node_implementation))

            # TODO: Criar logging para movimentação de nós
