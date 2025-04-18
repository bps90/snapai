from ...abc_custom_global import AbcCustomGlobal
from ...network_simulator import simulation
from .nodes.tank_node import TankNode
from .nodes.logistics_node import LogisticsNode
from .nodes.mechanized_infantry_node import MechanizedInfantryNode
from .nodes.staff_and_mortar_node import StaffAndMortarNode
from ...defaults.distribution_models.from_trace_2d_in_memory import FromTrace2DInMemory
from ...defaults.mobility_models.from_trace_2d_in_memory import FromTrace2DInMemory as FromTrace2DInMemoryMobility
from ...defaults.connectivity_models.no_connectivity import NoConnectivity
from ...defaults.reliability_models.reliable_delivery import ReliableDelivery
from ...defaults.interference_models.no_interference import NoInterference
from ...global_vars import Global


class CustomGlobal(AbcCustomGlobal):
    def has_terminated(self):
        return Global.current_time >= 7800

    def pre_run(self):
        simulation.remove_all_nodes()
        with open('apps/mobsinet/simulator/projects/sample9/vehicle_information.csv', 'r') as f:
            distribution_model = FromTrace2DInMemory()
            distribution_model.set_lat_long(True)
            distribution_model.load_trace(
                'traces/filtered_anglova.csv')
            distribution_model.set_should_padding(True)

            lines = [line.strip().split(',') for line in f.readlines()[1:]]
            lines.sort(key=lambda x: int(x[0]))
            for line in lines:
                vehicle_id = int(line[0])
                company_id = int(line[1])
                company_type = line[2]
                platoon_id = int(line[3])
                platoon_type = line[4]
                vehicle_function = line[5]
                vehicle_type = line[6]
                command = line[7]
                position = distribution_model.get_position()
                mobility_model = FromTrace2DInMemoryMobility()
                mobility_model.set_lat_long(True)
                mobility_model.load_trace('traces/filtered_anglova.csv')
                mobility_model.set_should_padding(True)
                connectivy_model = NoConnectivity()
                reliability_model = ReliableDelivery()
                interference_model = NoInterference()

                if (company_type == 'Tank'):
                    node = TankNode(vehicle_id, company_id, platoon_id,
                                    platoon_type, vehicle_function, vehicle_type, command, position, mobility_model,
                                    connectivy_model, interference_model, reliability_model)
                elif (company_type == 'Logistics'):
                    node = LogisticsNode(vehicle_id, company_id, platoon_id,
                                         platoon_type, vehicle_function, vehicle_type, command, position, mobility_model,
                                         connectivy_model, interference_model, reliability_model)
                elif (company_type == 'Mechanized Infantry'):
                    node = MechanizedInfantryNode(vehicle_id, company_id, platoon_id,
                                                  platoon_type, vehicle_function, vehicle_type, command, position, mobility_model,
                                                  connectivy_model, interference_model, reliability_model)
                elif (company_type == 'Staff and Mortar'):
                    node = StaffAndMortarNode(vehicle_id, company_id, platoon_id,
                                              platoon_type, vehicle_function, vehicle_type, command, position, mobility_model,
                                              connectivy_model, interference_model, reliability_model)
                else:
                    raise Exception('Unknown vehicle type: ' + vehicle_type)

                simulation.add_node(node)
