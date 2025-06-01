from ....models.nodes.abc_timer import AbcTimer


class InitPingPongTimer(AbcTimer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fire(self):
        self.node.init_pingpong()
