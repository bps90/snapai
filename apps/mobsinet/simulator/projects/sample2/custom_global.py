from ...abc_custom_global import AbcCustomGlobal


class CustomGlobal(AbcCustomGlobal):

    def has_terminated(self):
        return False
