from .mobility_model import MobilityModelQueryParser, MobilityModelQuery

class RandomWalkQuery(MobilityModelQuery):
    pass

class RandomWalkQueryParser(MobilityModelQueryParser):
    def get_query(self) -> RandomWalkQuery:
        return RandomWalkQuery(self.nodes, self.time, self.dimensions, self.size_x, self.size_y, self.size_z)