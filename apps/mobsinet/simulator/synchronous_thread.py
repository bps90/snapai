# GENERATED WITH HELP FROM CHATGPT

from datetime import datetime
from threading import Thread
from .global_vars import Global
from .models.nodes.abc_node import AbcNode
from .network_simulator import simulation
import time
from .configuration.sim_config import config


class SynchronousThread(Thread):
    tracefile_suffix = ''

    def __init__(self, number_of_rounds: int = 0, refresh_rate: float = 0):
        super().__init__()
        self.number_of_rounds = number_of_rounds
        self.refresh_rate = refresh_rate    # Taxa de atualização da GUI
        self.__should_stop = False  # Controle local para parar a thread

    def stop(self):
        self.__should_stop = True
        simulation.running_thread = None

    def run(self):
        self.__should_stop = False

        Global.log.info(
            f'Starting simulation thread for {self.number_of_rounds} rounds...')

        Global.is_running = True
        Global.start_time = datetime.now()

        ts = time.time()
        for i in range(self.number_of_rounds):
            if (self.refresh_rate != 0):
                slept_time = 1/self.refresh_rate - (time.time() - ts)
                time.sleep(slept_time if slept_time > 0 else 0)

            ts = time.time()
            if (Global.is_running == False or self.__should_stop):
                Global.is_running = False
                break

            Global.round_logs = []
            Global.current_time += 1
            Global.is_even_round = not Global.is_even_round
            Global.start_time_of_round = datetime.now()
            Global.number_of_messages_in_this_round = 0

            # ts = time.time()
            Global.custom_global.pre_round()
            self.__round()
            Global.custom_global.post_round()
            # print(f'{time.time() - ts} s for round')

            Global.number_of_messages_over_all += Global.number_of_messages_in_this_round

            if (Global.custom_global.has_terminated()):
                break

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
        if (config.connectivity_enabled):
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

        if (config.save_trace and Global.current_time == 1):
            tracefile = open(
                f'traces/{config.simulation_name+SynchronousThread.tracefile_suffix}.csv', 'w')
            tracefile.write('time,x,y,id\n')

            for node in simulation.nodes():
                tracefile.write(
                    f'{Global.current_time - 1},{node.position.x},{node.position.y},{node.id}\n')

            tracefile.close()

        tracefile = open(f"traces/{config.simulation_name+SynchronousThread.tracefile_suffix}.csv",
                         "a") if config.save_trace else None

        for node in simulation.nodes():
            node: 'AbcNode'

            # move the node
            node.set_position(node.mobility_model.get_next_position(node))

            if tracefile:
                tracefile.write(str(Global.current_time) + "," + str(node.position.x) + "," + str(
                    node.position.y) + "," + str(node.id) + "\n")

        if tracefile:
            tracefile.close()

    def __update_connections(self):
        """(private) Updates the connections in the network graph."""

        # TODO: Criar logging para conexão
        for node in simulation.nodes():
            node: 'AbcNode'

            # reset neighboorhood_changed flag
            node.neighborhood_changed = False
            connections = 0
            disconnections = 0

            # update the connections
            for possible_neighbor in simulation.nodes():
                possible_neighbor: 'AbcNode'

                if possible_neighbor == node:
                    continue

                is_connected = node.connectivity_model.is_connected(
                    node, possible_neighbor)
                has_edge = simulation.has_edge(node, possible_neighbor)

                if (is_connected and not has_edge):
                    simulation.add_edge(node, possible_neighbor)
                    node.neighborhood_changed = True
                    connections += 1

                elif (not is_connected and has_edge):
                    simulation.remove_edge(node, possible_neighbor)
                    simulation.packets_in_the_air.denyFromEdge(
                        node, possible_neighbor)
                    node.neighborhood_changed = True
                    disconnections += 1

            if node.neighborhood_changed:
                Global.round_logs.append(
                    f'Node {node.id} had {connections} connections and {disconnections} disconnections')

    def __step_nodes(self):
        """(private) Performs a step for each node in the network graph."""

        for node in simulation.nodes():
            node: 'AbcNode'
            node.step()
