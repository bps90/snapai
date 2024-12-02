# GENERATED WITH HELP FROM CHATGPT

from datetime import datetime
from threading import Thread
from .global_vars import Global
from .models.nodes.abc_node import AbcNode
from .models.nodes.packet import Packet
from .network_simulator import simulation
from networkx.readwrite import json_graph
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import time
from multiprocessing import Pool, cpu_count
import random
from .tools.position import Position
from .configuration.sim_config import config
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor,as_completed
from multiprocessing import Manager
from typing import Any
import dill
from math import ceil

class SynchronousThread(Thread):

    def __init__(self, number_of_rounds: int = 0, refresh_rate: int = 1):
        super().__init__()
        self.number_of_rounds = number_of_rounds
        self.refresh_rate = refresh_rate    # Taxa de atualização da GUI

    def run(self):
        Global.log.info(
            f'Starting simulation thread for {self.number_of_rounds} rounds...')

        Global.is_running = True
        Global.start_time = datetime.now()
        

        end = time.time()
        for i in range(self.number_of_rounds):
            # time.sleep(0.1)
            if (Global.is_running == False): break
            
            Global.current_time += 1
            Global.is_even_round = not Global.is_even_round
            Global.start_time_of_round = datetime.now()
            Global.number_of_messages_in_this_round = 0

            # ts = time.time()
            Global.custom_global.pre_round()
            self.__round()
            Global.custom_global.post_round()
            # print(f'{time.time() - ts} s for round')

            if (Global.custom_global.has_terminated()):
                break

            Global.number_of_messages_over_all += Global.number_of_messages_in_this_round

            # TODO: Remove after
            # if (i % 50 == 0): 
            #     Global.log.info(
            #     f'Round {i} finished. Number of messages in this round: {Global.number_of_messages_in_this_round}')
                
            #     print(f'{time.time() - end} s since last 50 rounds')
                
            #     # GUI.set_fps(100 / ((time.time() - end) or 1))
                
            #     end = time.time()
                

        
        Global.is_running = False

    def __round(self):
        """(private) Performs a single simulation round."""
        # print(f'Round {Global.current_time}')
        # ttimers = time.time()
        Global.custom_global.handle_global_timers()
        # print('Time to handle global timers: ', time.time() - ttimers)
        # tmove = time.time()
        self.__move_nodes()
        # print('Time to move nodes: ', time.time() - tmove)
        
        # tconn = time.time()
        self.__update_connections()
        # print('Time to update connections: ', time.time() - tconn)
        # tinterf = time.time()
        simulation.packets_in_the_air.test_interference()
        # print('Time to test interference: ', time.time() - tinterf)
        # tstep = time.time()
        self.__step_nodes()
        # print('Time to step nodes: ', time.time() - tstep)

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

                is_connected = node.connectivity_model.is_connected(
                    node, possible_neighbor)
                has_edge = simulation.has_edge(node, possible_neighbor)

                if (is_connected and not has_edge):
                    # Global.log.info(
                    #    f'Connected node {node.id} with node {possible_neighbor.id}')
                    simulation.add_edge(node, possible_neighbor)
                    node.neighborhood_changed = True

                elif (not is_connected and has_edge):
                    # Global.log.info(
                    #    f'Disconnected node {node.id} with node {possible_neighbor.id}')
                    simulation.remove_edge(node, possible_neighbor)
                    node.neighborhood_changed = True

    def __step_nodes(self):
        """(private) Performs a step for each node in the network graph."""

        for node in simulation.nodes():
            node: 'AbcNode'
            node.step()
