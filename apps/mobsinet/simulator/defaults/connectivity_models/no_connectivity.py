from ...models.abc_connectivity_model import AbcConnectivityModel

class NoConnectivity(AbcConnectivityModel):
    def __init__(self):
        super().__init__('NoConnectivity')

model = NoConnectivity