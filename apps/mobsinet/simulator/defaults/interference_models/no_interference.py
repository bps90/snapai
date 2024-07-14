from ...models.abc_interference_model import AbcInterferenceModel

class NoInterference(AbcInterferenceModel):
    def __init__(self):
        super().__init__('NoInterference')

model = NoInterference
    