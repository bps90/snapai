# GENERATED WITH HELP FROM CHATGPT

from datetime import datetime
from threading import Thread
from .global_vars import Global
from .models.nodes.abc_node import AbcNode
from .network_simulator import simulation


class SynchronousThread(Thread):

    def __init__(self, number_of_rounds: int = 0, refresh_rate: int = 1):
        super().__init__()
        self.number_of_rounds = number_of_rounds 
        self.refresh_rate = refresh_rate    # Taxa de atualização da GUI

    def run(self):
        Global.is_running = True
        Global.start_time = datetime.now()

        for current_round in range(self.number_of_rounds):
            Global.current_time += 1
            Global.is_even_round = not Global.is_even_round
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

        for node in simulation.nodes():
            node: 'AbcNode'
            # move the node
            node.set_position(node.mobility_model.get_next_position(node))

            # TODO: Criar logging para movimentação de nós

    def __update_connections(self):
        """(private) Updates the connections in the network graph."""

        # TODO: Criar logging para conexão

        for node in simulation.nodes():
            node: 'AbcNode'

            # reset neighboorhood_changed flag
            node.neighborhood_changed = False

            # update the connections
            for possible_neighbor in simulation.nodes():
                possible_neighbor: 'AbcNode'
                
                if possible_neighbor == node:
                    continue

                is_connected = node.connectivity_model.is_connected(node, possible_neighbor)
                has_edge = simulation.has_edge(node, possible_neighbor)

                if (is_connected and not has_edge):
                    simulation.add_edge(node, possible_neighbor)
                    node.neighborhood_changed = True
                    
                elif (not is_connected and has_edge):
                    simulation.remove_edge(node, possible_neighbor)
                    node.neighborhood_changed = True
                    
    def __step_nodes(self):
        """(private) Performs a step for each node in the network graph."""

        for node in simulation.nodes():
            node: 'AbcNode'
            node.step()