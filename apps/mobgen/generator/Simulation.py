from typing import List, Union, Tuple
from .Node import Node
from .MobilityModel import MobilityModel
from .Scenario import Scenario
from .scenarios.OneDimensionalScenario import OneDimensionalScenario
from .scenarios.TwoDimensionalScenario import TwoDimensionalScenario
from .scenarios.ThreeDimensionalScenario import ThreeDimensionalScenario
from time import sleep
from abc import ABC, abstractmethod

class SimulationData(ABC):
    def __init__(self, nodes_qty: int, simulation_time: int, scenario_dimensions: int, scenario_size: tuple[int, int, int]):
        self.nodes_qty = nodes_qty
        self.simulation_time = simulation_time
        self.scenario_dimensions = scenario_dimensions
        self.scenario_size = scenario_size

class Simulation(ABC):
    def __init__(self, data: SimulationData):
        print('[....................] Creating Simulation...')
        self.nodes: List[Node] = []
        self.currenttime = 0
        self.mobilityModel: MobilityModel
        self.simulation_time = data.simulation_time

        if data.scenario_dimensions == 1: self.scenario = OneDimensionalScenario(data.scenario_size)
        elif data.scenario_dimensions == 2: self.scenario = TwoDimensionalScenario(data.scenario_size)
        elif data.scenario_dimensions == 3: self.scenario = ThreeDimensionalScenario(data.scenario_size)
        else: raise Exception('Invalid Dimensions')

        print('[....................] Creating Nodes...')
        for i in range(1, data.nodes_qty + 1):
            progressPercent = (i*100)/data.nodes_qty
            progressPoints = int(progressPercent // 5)
            canPrint = progressPercent % 5 == 0

            if canPrint: print(f'[{"\033[32m.\033[0m" * progressPoints}{"." * (20 - progressPoints)}] Creating Nodes...')
            
            self.nodes.append(Node(i))
        print(f'[{"\033[32m." * 8} OK {"." * 8 + "\033[0m"}] Nodes Created')


    def add_node(self, node: Node):
        self.nodes.append(node)

    @abstractmethod
    def start(self, time: int):
        pass