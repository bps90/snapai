import networkx as nx

from .models.abc_distribution_model import AbcDistributionModel
from .models.abc_mobility_model import AbcMobilityModel
from .models.abc_connectivity_model import AbcConnectivityModel
from .models.abc_interference_model import AbcInterferenceModel
from .models.abc_reliability_model import AbcReliabilityModel
from .models.nodes.abc_node_implementation import AbcNodeImplementation
from .tools.position import Position
from .tools.models_normalizer import ModelsNormalizer
from .configuration.sim_config import sim_config_env
from typing import Type, Any


class NetworkSimulator(object):

    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.global_time = 0

    def add_nodes(
        self,
        nodes: int | list[Any],
        distribution_model: Type[AbcDistributionModel] | AbcDistributionModel | str = None,
        node_implementation_constructor: Type[AbcNodeImplementation] | str = None,
        mobility_model: Type[AbcMobilityModel] | AbcMobilityModel | str = None,
        connectivity_model: Type[AbcConnectivityModel] | AbcConnectivityModel | str = None,
        interference_model: Type[AbcInterferenceModel] | AbcInterferenceModel | str = None,
        reliability_model: Type[AbcReliabilityModel] | AbcReliabilityModel | str = None
    ):
        """Add a set of nodes to the network graph based on the distribution model.

        Parameters
        ----------
        nodes : int | list[Any]
            The number of nodes to add or a list of nodes to add
        distribution_model : Type[AbcDistributionModel] | AbcDistributionModel | str, optional
            The distribution model to distribute nodes in the graph.
            If a class, it will be instantiated.
            If a string, it must be exactly the name of the file containing the model,
            without the ".py" extension; it will be imported from PROJECT_DIR and instantiated.
            If None, the default distribution model will be used.
        node_implementation_constructor : Type[AbcNodeImplementation] | str, optional
            The class of the node_implementation to instantiate when nodes are created.
            If a string, it must be exactly the name of the file containing the node implementation,
            without the ".py" extension; it will be imported from PROJECT_DIR.
            If None, the default node_implementation will be used.
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
        >>> network_simulator.add_nodes(1, node_implementation_constructor=SmartphoneNodeImplementation)
        # Add 3 nodes with random walk mobility and a random distribution
        >>> network_simulator.add_nodes([10, 20, 30], mobility_model="random_walk", distribution_model="random_dist")
        ```

        Notes
        -----
        If you want to add a unique node with a defined position, use the `add_node` method.
        """

        distribution_model: AbcDistributionModel = ModelsNormalizer.normalize_distribution_model(
            distribution_model)
        node_implementation_constructor = ModelsNormalizer.normalize_node_implementation_constructor(
            node_implementation_constructor)

        for id in (range(nodes) if type(nodes) is int else nodes):
            mobility_model = ModelsNormalizer.normalize_mobility_model(
                mobility_model)
            connectivity_model = ModelsNormalizer.normalize_connectivity_model(
                connectivity_model)
            interference_model = ModelsNormalizer.normalize_interference_model(
                interference_model)
            reliability_model = ModelsNormalizer.normalize_reliability_model(
                reliability_model)

            node_implementation = node_implementation_constructor(
                id if type(nodes) is not int else self._gen_node_id(),
                mobility_model=mobility_model,
                connectivity_model=connectivity_model,
                interference_model=interference_model,
                reliability_model=reliability_model
            )

            position = distribution_model.get_position()

            node_implementation.set_position(position)

            self.add_node(node_implementation)

    def add_node(
        self,
        node_implementation: AbcNodeImplementation,
    ):
        """Add a node to the network graph.

        Parameters
        ----------
        node_implementation : AbcNodeImplementation
            The node implementation object.
        """

        if node_implementation.id not in self.graph.nodes():
            self.graph.add_node(
                node_implementation.id,
                implementation=node_implementation
            )
        else:
            raise ValueError(
                f"Node with ID {node_implementation.id} already exists.")

    def remove_node(self, node_id: int):
        """Remove a node from the network graph by their ID.

        Raises
        ------
        ValueError
            If the node is not in the graph.
        """

        if node_id in self.graph.nodes():
            self.graph.remove_node(node_id)
        else:
            raise ValueError(
                f"Node with ID {node_id} already removed or do not exists.")

    def add_edge(self, from_id, to_id):
        """Add an edge between two nodes in the network graph.

        Parameters
        ----------
        from_id : int
            The ID of the source node.
        to_id : int
            The ID of the destination node.
        """

        self.graph.add_edge(from_id, to_id)

    def add_bi_directional_edge(self, id1, id2):
        """Add a bi-directional edge between two nodes in the network graph."""

        self.add_edge(id1, id2)
        self.add_edge(id2, id1)

    def remove_edge(self,  from_id, to_id):
        """Remove an edge between two nodes in the network graph.

        Parameters
        ----------
        from_id : int
            The ID of the source node.
        to_id : int
            The ID of the destination node.
        """

        self.graph.remove_edge(from_id, to_id)

    def remove_bi_directional_edge(self, id1, id2):
        """Remove a bi-directional edge between two nodes in the network graph."""

        self.remove_edge(id1, id2)
        self.remove_edge(id2, id1)

    def init_net_models(self):
        """Init the models that will be used in the simulation."""

        # dist_model:AbcDistributionModel  = importlib.util.spec_from_file_location("random_dist", "/Users/bps/Documents/playground/MobENV/apps/mobsinet/simulator/defaults/distribution_models/random_dist.py")
        # foo = importlib.util.module_from_spec(dist_model)
        # sys.modules["random_dist"] = foo
        # dist_model.loader.exec_module(foo)
        # print(foo.RandomDist())
        pass

    def run(self):
        """Starts the simulation running."""

        simulation_name = sim_config_env.simulation_name
        simulation_steps = sim_config_env.simulation_steps
        self.logs_file_w = open(f"logs-{simulation_name}.txt", "w")

        for current_step in range(simulation_steps):
            self.__step()

        self.logs_file_w.close()

    def __step(self):
        """(private) Performs a single simulation step."""

        self.__move_nodes()
        self.__update_connections()

    def __move_nodes(self):
        """(private) Moves the nodes in the network graph."""

        for node in self.graph.nodes():
            node_implementation: AbcNodeImplementation = self.graph.nodes[node]["implementation"]

            # move the node
            node_implementation.set_position(
                node_implementation.mobility_model.get_next_position(node_implementation))

            self.logs_file_w.write(
                f"Moved node {node_implementation.id} for position ({node_implementation.position.x},{node_implementation.position.y},{node_implementation.position.z})\n")

    def __update_connections(self):
        """(private) Updates the connections in the network graph."""

        for node in self.graph.nodes():
            node_implementation: AbcNodeImplementation = self.graph.nodes[node]["implementation"]

            # update the connections
            for possible_neighbor in self.graph.nodes():
                if possible_neighbor == node:
                    continue

                possible_neighbor_implementation: AbcNodeImplementation = self.graph.nodes[
                    possible_neighbor]["implementation"]

                if (node_implementation.connectivity_model.is_connected(
                        node_implementation, possible_neighbor_implementation) and not self.graph.has_edge(node, possible_neighbor)):

                    self.add_edge(node, possible_neighbor)

                    self.logs_file_w.write(
                        f"Connected node {node_implementation.id} with node {possible_neighbor_implementation.id}\n")
                elif (self.graph.has_edge(node, possible_neighbor)):

                    self.remove_edge(node, possible_neighbor)

                    self.logs_file_w.write(
                        f"Disconnected node {node_implementation.id} with node {possible_neighbor_implementation.id}\n")

    def __str__(self) -> str:
        return str(self.graph)

    def _gen_node_id(self):
        """(private) Generates a new `node_id` based on number of current nodes in the graph.

        Notes
        -----
        The generated id may have already been used by another node that is no longer in the graph
        """
        node_id = self.graph.number_of_nodes() + 1

        while node_id in self.graph.nodes():
            node_id += 1

        return node_id


if __name__ == "__main__":
    # Create instances of the class
    ns = NetworkSimulator()
    # for i in range(1, 4):
    #     ns.add_node(i)

    ns.add_nodes([1, 2, 3, 4])

    ns.add_bi_directional_edge(1, 4)
    ns.add_edge(2, 3)
    print(ns.graph.edges())
    ns.remove_bi_directional_edge(1, 4)
    print(ns.graph.edges())
    print(ns)
    print(ns.graph.nodes())
    ns.init_net_models()

    # dist_model  = importlib.util.spec_from_file_location("random_dist", "apps/mobsinet/simulator/defaults/distribution_models/random_dist.py")
    # foo = importlib.util.module_from_spec(dist_model)
    # sys.modules["random_dist"] = foo
    # dist_model.loader.exec_module(foo)

    # print(foo)

    # randomDistModule = importlib.import_module(
    #     'apps.mobsinet.simulator.defaults.distribution_models.random_dist')

    # print(randomDistModule.model())

    print('\nGraph nodes with his attributes')
    print(ns.graph.nodes(data=True))
