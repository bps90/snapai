from ...models.nodes.abc_node import AbcNode


class InertNode(AbcNode):
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
