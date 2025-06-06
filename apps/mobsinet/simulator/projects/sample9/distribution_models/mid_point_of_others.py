from ....models.abc_distribution_model import AbcDistributionModel
from ....network_simulator import simulation
from ....tools.position import Position


class MidPointOfOthers(AbcDistributionModel):
    def __init__(self):
        super().__init__('MidPointOfOthers')

    def get_position(self, node):

        midpoint = [0, 0]

        for n in simulation.nodes():
            if (n.id >= node.id):
                break
            midpoint[0] += n.position.x
            midpoint[1] += n.position.y

        midpoint[0] /= len(simulation.nodes())
        midpoint[1] /= len(simulation.nodes())

        return Position(midpoint[0], midpoint[1])


model = MidPointOfOthers
