from abc import ABC, abstractmethod

class MobilityModelQuery(ABC):
    def __init__(self, nodes_qty: int, simulation_time: int, scenario_dimensions: int | None, scenario_size_x: int, scenario_size_y: int | None, scenario_size_z: int | None):
        self.nodes_qty = nodes_qty
        self.simulation_time = simulation_time
        self.scenario_dimensions = scenario_dimensions
        self.scenario_size_x = scenario_size_x
        self.scenario_size_y = scenario_size_y
        self.scenario_size_z = scenario_size_z

class MobilityModelQueryParser(ABC):
    def __init__(self, query: dict):
        self._parse(query)

    def _parse(self, query: dict):
        """
        :param query: The url query dictionary (string: string)
        """
        """
        First we need to get each object from the query
        """
        nodes: str = query.get('nodes')
        time: str = query.get('time')
        dimensions: str = query.get('dimensions')
        size_x: str = query.get('sizex')
        size_y: str = query.get('sizey')
        size_z: str = query.get('sizez')

        if (not nodes) or (not time) or (not size_x):
            raise Exception('Missing parameters (nodes, time, sizex)')

        if ((not nodes.isdigit()) or
            (not time.isdigit()) or
                    (dimensions and not dimensions.isdigit()) or
                (not size_x.isdigit()) or
                (size_y and not size_y.isdigit()) or
            (size_z and not size_z.isdigit())
            ):
            raise Exception(
                'Parameters nodes, time, dimensions, sizex, sizey, sizez must be int')

        self.nodes = int(nodes)
        self.time = int(time)
        self.dimensions = int(dimensions) if dimensions else None
        self.size_x = int(size_x)
        self.size_y = int(size_y) if size_y else None
        self.size_z = int(size_z) if size_z else None

    @abstractmethod
    def get_query(self) -> MobilityModelQuery:
        pass
