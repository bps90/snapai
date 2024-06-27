from ..config.simconfig import SimConfig
from .guiruntime import GUIRuntime

def mainRuntime():

    sim_config = SimConfig()

    if not sim_config.config["batchMode"]:
        gui = GUIRuntime(sim_config)
    else:
        pass




if __name__ == '__main__':
    mainRuntime()