from ....models.abc_connectivity_model import AbcConnectivityModel
from ..nodes.s9_node import S9Node


class HierarchyConnectivity(AbcConnectivityModel):

    def check_parameters(self, parameters):
        return True

    def set_parameters(self, parameters):
        pass

    def is_connected(self, node_a, node_b):
        if (not isinstance(node_a, S9Node) or not isinstance(node_b, S9Node)):
            return False

        if (node_a.command == 'Head Quarter' and node_b.command == 'Head Quarter'):
            return True
        if (node_a.command == 'Battalion Commander' and node_b.command == 'Head Quarter'):
            return True
        if (node_a.command == 'Head Quarter' and node_b.command == 'Battalion Commander'):
            return True
        if (node_a.command == 'Deputy Battalion Commander' and node_b.command == 'Battalion Commander'):
            return True
        if (node_a.command == 'Battalion Commander' and node_b.command == 'Deputy Battalion Commander'):
            return True
        if (node_a.command == 'Company Commander' and node_b.command == 'Deputy Battalion Commander'):
            return True
        if (node_a.command == 'Deputy Battalion Commander' and node_b.command == 'Company Commander'):
            return True
        if (node_a.command == 'Company Commander' and node_b.command == 'Battalion Commander'):
            return True
        if (node_a.command == 'Battalion Commander' and node_b.command == 'Company Commander'):
            return True
        if (node_a.command == 'Deputy Company Commander' and node_b.command == 'Company Commander' and node_a.company_id == node_b.company_id):
            return True
        if (node_a.command == 'Company Commander' and node_b.command == 'Deputy Company Commander' and node_a.company_id == node_b.company_id):
            return True
        if (node_a.command == 'Platoon Leader' and node_b.command == 'Deputy Company Commander' and node_a.company_id == node_b.company_id):
            return True
        if (node_a.command == 'Deputy Company Commander' and node_b.command == 'Platoon Leader' and node_a.company_id == node_b.company_id):
            return True
        if (node_a.command == 'Platoon Leader' and node_b.command == 'Company Commander' and node_a.company_id == node_b.company_id):
            return True
        if (node_a.command == 'Company Commander' and node_b.command == 'Platoon Leader' and node_a.company_id == node_b.company_id):
            return True
        if (node_a.command == 'Deputy Platoon Leader' and node_b.command == 'Platoon Leader' and node_a.company_id == node_b.company_id and node_a.platoon_id == node_b.platoon_id):
            return True
        if (node_a.command == 'Platoon Leader' and node_b.command == 'Deputy Platoon Leader' and node_a.company_id == node_b.company_id and node_a.platoon_id == node_b.platoon_id):
            return True
        if (node_a.command == '' and node_b.command == 'Deputy Platoon Leader' and node_a.company_id == node_b.company_id and node_a.platoon_id == node_b.platoon_id):
            return True
        if (node_a.command == 'Deputy Platoon Leader' and node_b.command == '' and node_a.company_id == node_b.company_id and node_a.platoon_id == node_b.platoon_id):
            return True
        if (node_a.command == '' and node_b.command == 'Platoon Leader' and node_a.company_id == node_b.company_id and node_a.platoon_id == node_b.platoon_id):
            return True
        if (node_a.command == 'Platoon Leader' and node_b.command == '' and node_a.company_id == node_b.company_id and node_a.platoon_id == node_b.platoon_id):
            return True
        return False


model = HierarchyConnectivity
