from ..abc_custom_global import AbcCustomGlobal

class DefaultCustomGlobal(AbcCustomGlobal):
    def has_terminated(self):
        return False