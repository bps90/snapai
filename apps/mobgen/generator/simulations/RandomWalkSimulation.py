from typing import List, Union, Tuple
from ..Node import Node
from ..mobility_models.RandomWalk import RandomWalk
from ..Scenario import Scenario
from ..scenarios.OneDimensionalScenario import OneDimensionalScenario
from ..scenarios.TwoDimensionalScenario import TwoDimensionalScenario
from ..scenarios.ThreeDimensionalScenario import ThreeDimensionalScenario
from time import sleep
from ..Simulation import Simulation, SimulationData

class RandomWalkSimulationData(SimulationData):
    pass

class RandomWalkSimulation(Simulation):
    def __init__(self, data: RandomWalkSimulationData):
        super().__init__(data)
        
        self.mobilityModel = RandomWalk(self.nodes, self.scenario)

        print(f'[{"\033[32m." * 8} OK {"." * 8 + "\033[0m"}] Simulation Created')

    def add_node(self, node: Node):
        self.nodes.append(node)

    def start(self):
        print('[....................] Starting Simulation...')

        csvfile = open('output.csv', 'w')

        csvheader = 'id,x,y,z,time\n'

        csvfile.write(csvheader)
        yield csvheader

        for i in range(self.currenttime, self.simulation_time + 1):
            progressPercent = (i*100)/(self.simulation_time + 1)
            progressPoints = int(progressPercent // 5)
            canPrint = progressPercent % 5 == 0

            if canPrint: print(f'[{"\033[32m.\033[0m" * progressPoints}{"." * (20 - progressPoints)}] Simulation in Progress...')

            self.currenttime = i
            for node in self.nodes:
                newLine = f'{node.id},{node.position.x},{node.position.y},{node.position.z},{self.currenttime}\n'
                
                csvfile.write(newLine)
                
                # sleep(0.1)
                yield newLine

                node.position = self.mobilityModel.getNextPosition(node)

        csvfile.close()

        print(f'[{"\033[32m." * 8} OK {"." * 8 + "\033[0m"}] Simulation Finished')

