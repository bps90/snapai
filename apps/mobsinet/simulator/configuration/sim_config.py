from typing import Any
from .base_config import BaseConfig


class SimulationConfig(BaseConfig):
    PROJECTS_DIR = "apps/mobsinet/simulator/projects/"
    simulation_name: str = "Network Simulation"
    simulation_rounds: float = 1000
    simulation_refresh_rate: float = 1
    nack_messages_enabled: bool = True
    dim_x: list[float] = [0, 100]
    dim_y: list[float] = [0, 100]
    dim_z: list[float] = [0, 0]
    save_trace: bool = False
    asynchronous: bool = False
    connectivity_enabled: bool = True
    interference_enabled: bool = True
    message_transmission_model: str = 'constant_time'
    message_transmission_model_parameters: dict[str, Any] = {
        "time": 1
    }

    @staticmethod
    def set_simulation_name(name: str):
        SimulationConfig.simulation_name = name

    @staticmethod
    def set_simulation_rounds(rounds: float):
        SimulationConfig.simulation_rounds = rounds

    @staticmethod
    def set_simulation_refresh_rate(refresh_rate: float):
        SimulationConfig.simulation_refresh_rate = refresh_rate

    @staticmethod
    def set_nack_messages_enabled(enabled: bool):
        SimulationConfig.nack_messages_enabled = enabled

    @staticmethod
    def set_simulation_dimensions(dim_x: list[float], dim_y: list[float], dim_z: list[float]):
        SimulationConfig.dim_x = dim_x
        SimulationConfig.dim_y = dim_y
        SimulationConfig.dim_z = dim_z

    @staticmethod
    def set_message_transmission_model(model: str):
        SimulationConfig.message_transmission_model = model

    @staticmethod
    def set_message_transmission_model_parameters(params: dict[str, Any]):
        SimulationConfig.message_transmission_model_parameters = params

    @staticmethod
    def set_asynchronous(async_mode: bool):
        SimulationConfig.asynchronous = async_mode

    @staticmethod
    def set_save_trace(save_trace: bool):
        SimulationConfig.save_trace = save_trace

    @staticmethod
    def set_connectivity_enabled(enabled: bool):
        SimulationConfig.connectivity_enabled = enabled

    @staticmethod
    def set_interference_enabled(enabled: bool):
        SimulationConfig.interference_enabled = enabled

    @staticmethod
    def print_config():
        print("Simulation Configuration:")
        print(f"Simulation Name: {SimulationConfig.simulation_name}")
        print(f"Simulation Rounds: {SimulationConfig.simulation_rounds}")
        print(
            f"Simulation Refresh Rate: {SimulationConfig.simulation_refresh_rate}")
        print(
            f"Nack Messages Enabled: {SimulationConfig.nack_messages_enabled}")
        print(
            f"Network Dimensions: {SimulationConfig.dim_x} x {SimulationConfig.dim_y} x {SimulationConfig.dim_z}")
        print(f"Asynchronous: {SimulationConfig.asynchronous}")
        print(f"Save Trace: {SimulationConfig.save_trace}")
        print(f"Connectivity Enabled: {SimulationConfig.connectivity_enabled}")
        print(f"Interference Enabled: {SimulationConfig.interference_enabled}")
        print(
            f"Message Transmission Model: {SimulationConfig.message_transmission_model}")
        print(
            f"Message Transmission Model Parameters: {SimulationConfig.message_transmission_model_parameters}")
