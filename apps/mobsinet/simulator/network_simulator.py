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


from .tools.models_normalizer import ModelsNormalizer
from typing import Type, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .models.nodes.abc_node import AbcNode


class NetworkSimulator(object):
    last_id = 0

    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.packets_in_the_air = PacketsInTheAirBuffer()
        self.arrived_packets: list[Packet] = []

    def nodes(self):
        return self.graph.nodes()
    
    def has_edge(self, node_from: 'AbcNode', node_to: 'AbcNode'):
        return self.graph.has_edge(node_from, node_to)

    def init_simulator(self, parameters: dict[str, Any]):
        """Initialize the simulator with the given parameters.
        
        Parameters
        ----------
        parameters : dict[str, Any]
            A dictionary containing the parameters to initialize the simulator.
            
            refresh_rate: int
                The refresh rate of the simulator.
            
            number_of_nodes: int
                The number of nodes to add.
            
            distribution_model: Type[AbcDistributionModel] | AbcDistributionModel | str
                The distribution model to distribute nodes in the graph.
            
            node_constructor: Type[AbcNode] | str
                The class of the node to instantiate when nodes are created.
            
            mobility_model: Type[AbcMobilityModel] | AbcMobilityModel | str
                The mobility model that will be used by these nodes.
            
            connectivity_model: Type[AbcConnectivityModel] | AbcConnectivityModel | str
                The connectivity model that will be used by these nodes.
            
            interference_model: Type[AbcInterferenceModel] | AbcInterferenceModel | str
                The interference model that will be used by these nodes.
            
            reliability_model: Type[AbcReliabilityModel] | AbcReliabilityModel | str
                The reliability model that will be used by these nodes.
        """
        
        config.refresh_rate = parameters['refresh_rate']
        
        self.add_nodes(num_nodes=parameters['number_of_nodes'],
                       distribution_model=parameters['distribution_model'],
                       node_constructor=parameters['node_constructor'],
                       mobility_model=parameters['mobility_model'],
                       connectivity_model=parameters['connectivity_model'],
                       interference_model=parameters['interference_model'],
                       reliability_model=parameters['reliability_model'])

    def add_nodes(
        self,
        num_nodes: int,
        distribution_model: Type[AbcDistributionModel] | AbcDistributionModel | str = None,
        node_constructor: Type['AbcNode'] | str = None,
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

        distribution_model: AbcDistributionModel = ModelsNormalizer.normalize_distribution_model(
            distribution_model)
        node_constructor = ModelsNormalizer.normalize_node_constructor(
            node_constructor)

        for _ in range(num_nodes):
            mobility_model = ModelsNormalizer.normalize_mobility_model(
                mobility_model)
            connectivity_model = ModelsNormalizer.normalize_connectivity_model(
                connectivity_model)
            interference_model = ModelsNormalizer.normalize_interference_model(
                interference_model)
            reliability_model = ModelsNormalizer.normalize_reliability_model(
                reliability_model)

            node = node_constructor(
                self._gen_node_id(),
                mobility_model=mobility_model,
                connectivity_model=connectivity_model,
                interference_model=interference_model,
                reliability_model=reliability_model
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
        self.graph.add_edge(node_from, node_to)

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

        NetworkSimulator.last_id += 1

        return NetworkSimulator.last_id

    def pre_run(self):
        """Called before executing the first round of the simulation."""
        
        Global.custom_global.pre_run()
        
    def run(self):
        from .synchronous_thread import SynchronousThread
        
        if Global.is_running:
            return
        
        thread = SynchronousThread(config.simulation_rounds, config.simulation_refresh_rate)
        
        thread.start()
        
        

simulation = NetworkSimulator()

if __name__ == "__main__":
    # for i in range(1, 4):
    #     ns.add_node(i)

    simulation.add_nodes([1, 2, 3, 4])

    simulation.add_bi_directional_edge(1, 4)
    simulation.add_edge(2, 3)
    print(simulation.graph.edges())
    simulation.remove_bi_directional_edge(1, 4)
    print(simulation.graph.edges())
    print(simulation)
    print(simulation.graph.nodes())
    simulation.init_net_models()

    # dist_model  = importlib.util.spec_from_file_location("random_dist", "apps/mobsinet/simulator/defaults/distribution_models/random_dist.py")
    # foo = importlib.util.module_from_spec(dist_model)
    # sys.modules["random_dist"] = foo
    # dist_model.loader.exec_module(foo)

    # print(foo)

    # randomDistModule = importlib.import_module(
    #     'apps.mobsinet.simulator.defaults.distribution_models.random_dist')

    # print(randomDistModule.model())

    print('\nGraph nodes with his attributes')
    print(simulation.graph.nodes(data=True))
