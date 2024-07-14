from ...models.abc_reliability_model import AbcReliabilityModel

class NoReliability(AbcReliabilityModel):

    def __init__(self):
        super().__init__('NoReliability')

model = NoReliability