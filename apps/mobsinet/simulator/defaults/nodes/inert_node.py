from ...models.nodes.abc_node import AbcNode


class InertNode(AbcNode):
    def __init__(self, id, position=None, mobility_model=None, connectivity_model=None, interference_model=None, reliability_model=None):
        super().__init__(id, position, mobility_model,
                         connectivity_model, interference_model, reliability_model)
        self.size = 3

    def check_requirements(self):
        pass

    def handle_messages(self, inbox):
        pass

    def init(self):
        pass

    def post_step(self):
        pass

    def pre_step(self):
        pass

    def on_neighboorhood_change(self):
        pass


node = InertNode
