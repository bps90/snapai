from ...abc_custom_global import AbcCustomGlobal
from ...network_simulator import simulation, NetworkSimulator
from .nodes.tank_node import TankNode
from .nodes.logistics_node import LogisticsNode
from .nodes.mechanized_infantry_node import MechanizedInfantryNode
from .nodes.staff_and_mortar_node import StaffAndMortarNode
from ...defaults.distribution_models.from_trace_2d_in_memory import FromTrace2DInMemory
from ...defaults.mobility_models.from_trace_2d_in_memory import FromTrace2DInMemory as FromTrace2DInMemoryMobility
from ...global_vars import Global
from ...tools.models_normalizer import ModelsNormalizer
from ...configuration.sim_config import config


class CustomGlobal(AbcCustomGlobal):
    def has_terminated(self):
        return Global.current_time >= 7800

    def pre_run(self):
        simulation.remove_all_nodes()
        with open('apps/mobsinet/simulator/projects/sample9/vehicle_information.csv', 'r') as information_f:
            with open('apps/mobsinet/simulator/projects/sample9/comm-channels.csv', 'r') as channels_f:
                distribution_model = FromTrace2DInMemory()
                distribution_model.set_lat_long(True)
                distribution_model.load_trace(
                    'apps/mobsinet/simulator/projects/sample9/filtered_anglova.csv')

                lines = [line.strip().split(',')
                         for line in information_f.readlines()[1:]]
                lines.sort(key=lambda x: int(x[0]))
                comm_lines = [list(filter(lambda x: x != '', line.strip().split(',')[0:35]))
                              for line in channels_f.readlines()]

                for line in lines[:]:
                    vehicle_id = int(line[0])
                    company_id = int(line[1])
                    company_type = line[2]
                    platoon_id = int(line[3])
                    platoon_type = line[4]
                    vehicle_function = line[5]
                    vehicle_type = line[6]
                    command = line[7]
                    comm_channels = comm_lines[vehicle_id - 1]
                    position = distribution_model.get_position()
                    mobility_model = FromTrace2DInMemoryMobility()
                    mobility_model.set_lat_long(True)
                    mobility_model.load_trace(
                        'apps/mobsinet/simulator/projects/sample9/filtered_anglova.csv')
                    connectivy_model = ModelsNormalizer.normalize_connectivity_model(
                        config.connectivity_model)
                    reliability_model = ModelsNormalizer.normalize_reliability_model(
                        config.reliability_model)
                    interference_model = ModelsNormalizer.normalize_interference_model(
                        config.interference_model)

                    if (company_type == 'Tank'):
                        node = TankNode(vehicle_id, company_id, platoon_id,
                                        platoon_type, vehicle_function, vehicle_type, command, comm_channels, position, mobility_model,
                                        connectivy_model, interference_model, reliability_model)
                    elif (company_type == 'Logistics'):
                        node = LogisticsNode(vehicle_id, company_id, platoon_id,
                                             platoon_type, vehicle_function, vehicle_type, command, comm_channels, position, mobility_model,
                                             connectivy_model, interference_model, reliability_model)
                    elif (company_type == 'Mechanized Infantry'):
                        node = MechanizedInfantryNode(vehicle_id, company_id, platoon_id,
                                                      platoon_type, vehicle_function, vehicle_type, command, comm_channels, position, mobility_model,
                                                      connectivy_model, interference_model, reliability_model)
                    elif (company_type == 'Staff and Mortar'):
                        node = StaffAndMortarNode(vehicle_id, company_id, platoon_id,
                                                  platoon_type, vehicle_function, vehicle_type, command, comm_channels, position, mobility_model,
                                                  connectivy_model, interference_model, reliability_model)
                    else:
                        raise Exception(
                            'Unknown vehicle type: ' + vehicle_type)

                    simulation.add_node(node)
                    NetworkSimulator.last_node_id = vehicle_id
