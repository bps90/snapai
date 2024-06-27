from ..config.simconfig import SimConfig


class GUIRuntime():
    def __init__(self, sim_config: SimConfig):
        self.sim_config = sim_config


        #we need to define the number of nodes of this simulation.

        # TODO: Ask to the user input the nodes. 