import networkx as nx

from .models.nodes.packet import Packet

from .tools.packets_in_the_air_buffer import PacketsInTheAirBuffer
from .models.abc_distribution_model import AbcDistributionModel
from .models.abc_mobility_model import AbcMobilityModel
from .models.abc_connectivity_model import AbcConnectivityModel
from .models.abc_interference_model import AbcInterferenceModel
from .models.abc_reliability_model import AbcReliabilityModel
from .configuration.sim_config import config
from .global_vars import Global
from .tools.color import Color


from .tools.models_normalizer import ModelsNormalizer
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .models.nodes.abc_node import AbcNode
    from .tools.event import Event


class NetworkSimulator(object):
    last_node_id = 0

    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.packets_in_the_air = PacketsInTheAirBuffer()
        self.arrived_packets: list[Packet] = []
        self.running_thread = None
        self.event_queue: list[Event] = []

    def reset(self):
        NetworkSimulator.last_node_id = 0
        self.__init__()

    def nodes(self) -> list['AbcNode']:
        return list(self.graph.nodes)

    def has_edge(self, node_from: 'AbcNode', node_to: 'AbcNode'):
        return self.graph.has_edge(node_from, node_to)

    def add_project_nodes(self):
        """Initialize the simulator with the config parameters."""

        self.add_nodes(num_nodes=config.num_nodes,
                       distribution_model=config.distribution_model,
                       node_constructor=config.node,
                       node_color=config.node_color,
                       node_size=config.node_size,
                       mobility_model=config.mobility_model,
                       connectivity_model=config.connectivity_model,
                       interference_model=config.interference_model,
                       reliability_model=config.reliability_model)

    def add_nodes(
        self,
        num_nodes: int,
        distribution_model: Type[AbcDistributionModel] | AbcDistributionModel | str = None,
        node_constructor: Type['AbcNode'] | str = None,
        node_color: str = None,
        node_size: int = None,
        mobility_model: Type[AbcMobilityModel] | AbcMobilityModel | str = None,
        connectivity_model: Type[AbcConnectivityModel] | AbcConnectivityModel | str = None,
        interference_model: Type[AbcInterferenceModel] | AbcInterferenceModel | str = None,
        reliability_model: Type[AbcReliabilityModel] | AbcReliabilityModel | str = None
    ):
        """Add a set of nodes to the network graph based on the distribution model.

        Parameters
        ----------
        num_nodes : int
            The number of nodes to add
        distribution_model : Type[AbcDistributionModel] | AbcDistributionModel | str, optional
            The distribution model to distribute nodes in the graph.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default distribution model will be used.
        node_constructor : Type[AbcNode] | str, optional
            The class of the node to instantiate when nodes are created.
            If a string, it must be exactly the name of the file containing the node implementation,
            without the ".py" extension; it will be imported from PROJECT_DIR.
            If None, the default node will be used.
        mobility_model : Type[AbcMobilityModel] | AbcMobilityModel | str, optional
            The mobility model that will be used by these nodes.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default mobility model will be used.
        connectivity_model : Type[AbcConnectivityModel] | AbcConnectivityModel | str, optional
            The connectivity model that will be used by these nodes.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default connectivity model will be used.
        interference_model : Type[AbcInterferenceModel] | AbcInterferenceModel | str, optional
            The interference model that will be used by these nodes.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default interference model will be used.
        reliability_model : Type[AbcReliabilityModel] | AbcReliabilityModel | str, optional
            The reliability model that will be used by these nodes.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default reliability model will be used.

        Examples
        --------
        ```python
        # Add 100 nodes with a uniform distribution
        >>> network_simulator.add_nodes(100, distribution_model="uniform_dist")
        # Add 5 nodes with a uniform distribution
        >>> network_simulator.add_nodes([1, 2, 3, 4, 5], distribution_model="random_dist")
        # Add 1 node with the smartphone node implementation
        >>> network_simulator.add_nodes(1, node_constructor=SmartphoneNode)
        # Add 3 nodes with random walk mobility and a random distribution
        >>> network_simulator.add_nodes([10, 20, 30], mobility_model="random_walk", distribution_model="random_dist")
        ```

        Notes
        -----
        If you want to add a unique node with a defined position, use the `add_node` method.
        """

        Global.log.info(f'Adding {num_nodes} nodes with the following configuration:\n    Distribution Model: {distribution_model}\n    Node Constructor: {node_constructor}\n    Mobility Model: {mobility_model}\n    Connectivity Model: {connectivity_model}\n    Interference Model: {interference_model}\n    Reliability Model: {reliability_model}')

        distribution_model: AbcDistributionModel = ModelsNormalizer.normalize_distribution_model(
            distribution_model)
        node_constructor = ModelsNormalizer.normalize_node_constructor(
            node_constructor)

        for _ in range(num_nodes):
            mobility = ModelsNormalizer.normalize_mobility_model(
                mobility_model)
            connectivity = ModelsNormalizer.normalize_connectivity_model(
                connectivity_model)
            interference = ModelsNormalizer.normalize_interference_model(
                interference_model)
            reliability = ModelsNormalizer.normalize_reliability_model(
                reliability_model)

            node = node_constructor(
                self._gen_node_id(),
                mobility_model=mobility,
                connectivity_model=connectivity,
                interference_model=interference,
                reliability_model=reliability
            )
            node.set_color(
                Color(hex_str=node_color if node_color else config.node_color))
            node.set_size(node_size)

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

    def run(self, rounds=config.simulation_rounds, refresh_rate: float = config.simulation_refresh_rate):
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
