import random
from ...tools.position import Position
from ...models.abc_distribution_model import AbcDistributionModel

#SEED such seed could be configured from config file to reproduce simulation.
#seed_value = 10
#random.seed(seed_value)


class Random(AbcDistributionModel):

    def get_next_position(self) -> Position:
        p = Position(x= random.randrange(0, DIM_X),
                     y= random.randrange(0, DIM_Y),
                     z= random.randrange(0, DIM_Z))

        return p
    

if __name__ == "__main__":
    # Create instances of the class
    dm = Random()
    print(dm.get_next_position())