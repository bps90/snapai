from ...abc_custom_global import AbcCustomGlobal
from ...global_vars import Global
from ...configuration.sim_config import config

class CustomGlobal(AbcCustomGlobal):
    def check_project_requirements(self):
        print('Checando')
    
    def has_terminated(self):
        return super().has_terminated()
