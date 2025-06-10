from threading import Thread
from typing import TYPE_CHECKING, Optional
from .global_vars import Global
import time
from .network_simulator import simulation
from .configuration.sim_config import SimulationConfig

if TYPE_CHECKING:
    from .models.nodes.abc_node import AbcNode


class AsynchronousThread(Thread):
    connectivity_initialized = False

    def __init__(self, number_of_events: int, refresh_rate: float):
        super().__init__()
        self.number_of_events = number_of_events
        self.refresh_rate = refresh_rate
        self.last_event_node: Optional[AbcNode] = None
        self.__should_stop = False  # Local control to stop the thread

    def stop(self):
        self.__should_stop = True
        simulation.running_thread = None

    def run(self):
        Global.log.info(
            f'Starting simulation thread for {self.number_of_events} events...')

        Global.is_running = True
        if (AsynchronousThread.connectivity_initialized == False):
            AsynchronousThread.reevaluate_connections()

        ts = time.time()
        for _ in range(self.number_of_events):
            if (self.refresh_rate != 0):
                slept_time = 1/self.refresh_rate - (time.time() - ts)
                time.sleep(slept_time if slept_time > 0 else 0)

            ts = time.time()
            print()

            if (Global.is_running == False or self.__should_stop):
                Global.is_running = False
                break

            if (simulation.event_queue.is_empty()):
                Global.log.info(
                    "Event queue is empty. Handling empty event queue on custom global.")
                Global.custom_global.handle_empty_event_queue()

            if (simulation.event_queue.is_empty()):
                Global.log.info(
                    'No event to execute! Generate a event manually.')
                break

            event = simulation.event_queue.remove()

            Global.current_time = event.time
            print('current time:', Global.current_time)
            print('event time:', event.time)
            event.handle()
            print('event handled')
            print([event.id for event in simulation.event_queue])

        Global.is_running = False

    @staticmethod
    def reevaluate_connections():
        """(private) Updates the connections in the network graph."""
        if SimulationConfig.connectivity_enabled == False:
            return
        for node in simulation.nodes():
            # reset neighboorhood_changed flag
            node.neighborhood_changed = False
            connections = 0
            disconnections = 0

            # update the connections
            for possible_neighbor in simulation.nodes():
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
        AsynchronousThread.connectivity_initialized = True
