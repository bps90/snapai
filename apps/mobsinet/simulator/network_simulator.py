import networkx as nx

from .models.nodes.packet import Packet

from .tools.packets_in_the_air_buffer import PacketsInTheAirBuffer
from .models.abc_distribution_model import AbcDistributionModel
from .models.abc_mobility_model import AbcMobilityModel
from .models.abc_connectivity_model import AbcConnectivityModel
from .models.abc_interference_model import AbcInterferenceModel
from .models.abc_reliability_model import AbcReliabilityModel
from .models.abc_model import AbcModelParameters
from .configuration.sim_config import SimulationConfig
from .global_vars import Global
from .tools.color import Color
from .tools.event_queue import EventQueue
import inspect

from .tools.models_normalizer import ModelsSearchEngine
from typing import Type, TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from .models.nodes.abc_node import AbcNode
    from .tools.event import Event


class NetworkSimulator(object):
    last_node_id = 0

    def _init_instance_variables(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.packets_in_the_air = PacketsInTheAirBuffer()
        self.arrived_packets: list[Packet] = []
        self.running_thread = None
        self.event_queue: EventQueue = EventQueue()

    def __init__(self):
        self._init_instance_variables()

    def reset(self):
        NetworkSimulator.last_node_id = 0
        self._init_instance_variables()

    def nodes(self) -> list['AbcNode']:
        return list(self.graph.nodes)

    def has_edge(self, node_from: 'AbcNode', node_to: 'AbcNode'):
        return self.graph.has_edge(node_from, node_to)

    def add_nodes(
        self,
        num_nodes: int,
        distribution_model_arg: Type[AbcDistributionModel] | AbcDistributionModel | str,
        node_arg: Type['AbcNode'] | str,
        node_color: str,
        node_size: int,
        mobility_model_arg: Type[AbcMobilityModel] | AbcMobilityModel | str,
        connectivity_model_arg: Type[AbcConnectivityModel] | AbcConnectivityModel | str,
        interference_model_arg: Type[AbcInterferenceModel] | AbcInterferenceModel | str,
        reliability_model_arg: Type[AbcReliabilityModel] | AbcReliabilityModel | str,
        distribution_model_parameters: AbcModelParameters = {},
        mobility_model_parameters: AbcModelParameters = {},
        connectivity_model_parameters: AbcModelParameters = {},
        interference_model_parameters: AbcModelParameters = {},
        reliability_model_parameters: AbcModelParameters = {}
    ):
        """
        Adds nodes to the network simulator.

        Parameters
        ----------
        num_nodes : int
            The number of nodes to add.
        distribution_model_arg : Type[AbcDistributionModel] | AbcDistributionModel | str
            The distribution model to use for each node. It can be either a string
            with the name of the distribution model class, an instance of the model
            class, or the class itself.
        node_arg : Type['AbcNode'] | str
            The node class to use for each node. It can be either a string
            with the name of the node class, or the class itself.
        node_color : str
            The color of each node as a hexadecimal string.
        node_size : int
            The size of each node.
        mobility_model_arg : Type[AbcMobilityModel] | AbcMobilityModel | str
            The mobility model to use for each node. It can be either a string
            with the name of the mobility model class, an instance of the model
            class, or the class itself.
        connectivity_model_arg : Type[AbcConnectivityModel] | AbcConnectivityModel | str
            The connectivity model to use for each node. It can be either a string
            with the name of the connectivity model class, an instance of the model
            class, or the class itself.
        interference_model_arg : Type[AbcInterferenceModel] | AbcInterferenceModel | str
            The interference model to use for each node. It can be either a string
            with the name of the interference model class, an instance of the model
            class, or the class itself.
        reliability_model_arg : Type[AbcReliabilityModel] | AbcReliabilityModel | str
            The reliability model to use for each node. It can be either a string
            with the name of the reliability model class, an instance of the model
            class, or the class itself.
        distribution_model_parameters : dict[str, Any]
            The parameters for the distribution model.
        mobility_model_parameters : dict[str, Any]
            The parameters for the mobility model.
        connectivity_model_parameters : dict[str, Any]
            The parameters for the connectivity model.
        interference_model_parameters : dict[str, Any]
            The parameters for the interference model.
        reliability_model_parameters : dict[str, Any]
            The parameters for the reliability model.

        Returns
        -------
        None
        """
        if (isinstance(distribution_model_arg, str)):
            distribution_model = ModelsSearchEngine.find_distribution_model(
                distribution_model_arg)(distribution_model_parameters)
        if (isinstance(node_arg, str)):
            node_constructor = ModelsSearchEngine.find_node_implementation(
                node_arg)
        if (isinstance(mobility_model_arg, str)):
            mobility_model = ModelsSearchEngine.find_mobility_model(
                mobility_model_arg)(mobility_model_parameters)
        if (isinstance(connectivity_model_arg, str)):
            connectivity_model = ModelsSearchEngine.find_connectivity_model(
                connectivity_model_arg)(connectivity_model_parameters)
        if (isinstance(interference_model_arg, str)):
            interference_model = ModelsSearchEngine.find_interference_model(
                interference_model_arg)(interference_model_parameters)
        if (isinstance(reliability_model_arg, str)):
            reliability_model = ModelsSearchEngine.find_reliability_model(
                reliability_model_arg)(reliability_model_parameters)

        if (isinstance(distribution_model_arg, AbcDistributionModel)):
            distribution_model = distribution_model_arg
        if (isinstance(mobility_model_arg, AbcMobilityModel)):
            mobility_model = mobility_model_arg
        if (isinstance(connectivity_model_arg, AbcConnectivityModel)):
            connectivity_model = connectivity_model_arg
        if (isinstance(interference_model_arg, AbcInterferenceModel)):
            interference_model = interference_model_arg
        if (isinstance(reliability_model_arg, AbcReliabilityModel)):
            reliability_model = reliability_model_arg

        if (inspect.isclass(distribution_model_arg)):
            distribution_model = distribution_model_arg(
                distribution_model_parameters)
        if (inspect.isclass(mobility_model_arg)):
            mobility_model = mobility_model_arg(
                mobility_model_parameters)
        if (inspect.isclass(connectivity_model_arg)):
            connectivity_model = connectivity_model_arg(
                connectivity_model_parameters)
        if (inspect.isclass(interference_model_arg)):
            interference_model = interference_model_arg(
                interference_model_parameters)
        if (inspect.isclass(reliability_model_arg)):
            reliability_model = reliability_model_arg(
                reliability_model_parameters)

        Global.log.info(f'''Adding {num_nodes} nodes with the following configuration:
                        Node Constructor: {node_constructor.__name__}
                        Distribution Model: {distribution_model.__class__.__name__}
                        Mobility Model: {mobility_model.__class__.__name__}
                        Connectivity Model: {connectivity_model.__class__.__name__}
                        Interference Model: {interference_model.__class__.__name__}
                        Reliability Model: {reliability_model.__class__.__name__}''')

        for _ in range(num_nodes):

            node = node_constructor(
                self._gen_node_id(),
                mobility_model=mobility_model,
                connectivity_model=connectivity_model,
                interference_model=interference_model,
                reliability_model=reliability_model,
                color=Color(hex_str=node_color),
                size=node_size
            )

            position = distribution_model.get_position()

            node.set_position(position)

            self.add_node(node)

    def add_node(
        self,
        node: 'AbcNode',
    ):
        """Add a node to the network graph.

        Parameters
        ----------
        node : AbcNode
            The node implementation object.
        """

        if node not in self.nodes():
            self.graph.add_node(node)
            Global.custom_global.node_added_event(node)
        else:
            raise ValueError(
                f"Node with ID {node.id} already exists.")

    def remove_node(self, node_id: int):
        """Remove a node from the network graph by their ID.

        Raises
        ------
        ValueError
            If the node is not in the graph.
        """

        for n in self.nodes():
            if n.id == node_id:
                self.graph.remove_node(n)
                Global.custom_global.node_removed_event(n)
                break
        else:
            raise ValueError(
                f"Node with ID {node_id} already removed or do not exists.")

    def remove_all_nodes(self):
        """Remove all nodes from the network graph."""

        for n in self.nodes():
            self.graph.remove_node(n)
            Global.custom_global.node_removed_event(n)

    def add_edge(self, node_from: 'AbcNode', node_to: 'AbcNode'):
        """Add an edge between two nodes in the network graph.

        Parameters
        ----------
        node_from : AbcNode
            The source node.
        node_to : AbcNode
            The destination node.
        """

        # TODO: Criar EdgeImplementation (talvez)
        self.graph.add_edge(node_from, node_to, number_of_packets=0)

    def add_bi_directional_edge(self, node1: 'AbcNode', node2: 'AbcNode'):
        """Add a bi-directional edge between two nodes in the network graph."""

        self.add_edge(node1, node2)
        self.add_edge(node2, node1)

    def remove_edge(self,  node_from, node_to):
        """Remove an edge between two nodes in the network graph.

        Parameters
        ----------
        node_from : AbcNode
            The source node.
        node_to : AbcNode
            The destination node.
        """

        self.graph.remove_edge(node_from, node_to)

    def remove_bi_directional_edge(self, node1: 'AbcNode', node2: 'AbcNode'):
        """Remove a bi-directional edge between two nodes in the network graph."""

        self.remove_edge(node1, node2)
        self.remove_edge(node2, node1)

    def __str__(self) -> str:
        return str(self.graph)

    def _gen_node_id(self):
        """(private) Generates a new unique `node_id` for this simulation."""

        NetworkSimulator.last_node_id += 1

        return NetworkSimulator.last_node_id

    def pre_run(self):
        """Called before executing the first round of the simulation."""

        Global.custom_global.pre_run()

    def run(self, rounds=SimulationConfig.simulation_rounds, refresh_rate: float = SimulationConfig.simulation_refresh_rate):
        from .synchronous_thread import SynchronousThread
        from .asynchronous_thread import AsynchronousThread

        if Global.is_running:
            return

        if Global.is_async_mode:
            self.running_thread = AsynchronousThread(
                rounds, refresh_rate)
        else:
            self.running_thread = SynchronousThread(
                rounds, refresh_rate)

        self.running_thread.start()

    def stop(self):
        if (not self.running_thread):
            return

        Global.log.info('Stopping simulation...')
        self.running_thread.stop()
        Global.is_running = False

    def get_node_by_id(self, node_id: int):
        for node in self.nodes():
            if node.id == node_id:
                return node

    def remove_all_async_events(self):
        for event in self.event_queue:
            event.drop()
        self.event_queue.clear()


simulation = NetworkSimulator()

if __name__ == "__main__":
    # TODO: Do something here
    pass
