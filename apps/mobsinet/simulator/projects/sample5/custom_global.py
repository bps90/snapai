from ...abc_custom_global import AbcCustomGlobal

class CustomGlobal(AbcCustomGlobal):
    def check_project_requirements(self):
        print('Checando')
    
    def has_terminated(self):
        return super().has_terminated()
