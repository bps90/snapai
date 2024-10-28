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
            
            Global.start_time_of_round = datetime.now()
            Global.number_of_messages_in_this_round = 0

            Global.custom_global.pre_round()
            self.__round()
            Global.custom_global.post_round()

            if (Global.custom_global.has_terminated()):
                break
            
            Global.number_of_messages_over_all += Global.number_of_messages_in_this_round

        Global.is_running = False

    def __round(self):
        """(private) Performs a single simulation round."""

        Global.custom_global.handle_global_timers()
        self.__move_nodes()
        self.__update_connections()
        simulation.packets_in_the_air.test_interference()
        self.__step_nodes()
        

    def __move_nodes(self):
        """(private) Moves the nodes in the network graph."""

        for node in simulation.graph.nodes():
            node_implementation: 'AbcNodeImplementation' = simulation.graph.nodes[
                node]["implementation"]

            # move the node
            node_implementation.set_position(
                node_implementation.mobility_model.get_next_position(node_implementation))

            # TODO: Criar logging para movimentação de nós

    def __update_connections(self):
        """(private) Updates the connections in the network graph."""

        # TODO: Criar logging para conexão

        for node in simulation.graph.nodes():
            node_implementation: 'AbcNodeImplementation' = simulation.graph.nodes[node]["implementation"]

            # reset neighboorhood_changed flag
            node_implementation.neighboorhood_changed = False

            # update the connections
            for possible_neighbor in simulation.graph.nodes():
                if possible_neighbor == node:
                    continue

                possible_neighbor_implementation: 'AbcNodeImplementation' = simulation.graph.nodes[
                    possible_neighbor]["implementation"]

                is_connected = node_implementation.connectivity_model.is_connected(node_implementation,
                                                                                   possible_neighbor_implementation)
                has_edge = simulation.graph.has_edge(node, possible_neighbor)

                if (is_connected and not has_edge):
                    simulation.add_edge(node, possible_neighbor)
                    node_implementation.neighboorhood_changed = True
                    
                elif (not is_connected and has_edge):
                    simulation.remove_edge(node, possible_neighbor)
                    node_implementation.neighboorhood_changed = True
                    
    def __step_nodes(self):
        """(private) Performs a step for each node in the network graph."""

        for node in simulation.graph.nodes():
            node_implementation: 'AbcNodeImplementation' = simulation.graph.nodes[node]["implementation"]
            node_implementation.step()