from ...abc_custom_global import AbcCustomGlobal
from ...network_simulator import simulation
import random
from .nodes.s8_node import S8Node
from ...global_vars import Global


class CustomGlobal(AbcCustomGlobal):

    def __init__(self):
        super().__init__()
        self.empty_queue_handled = False

    def handle_empty_event_queue(self):
        """
        Called when the event queue is empty.
        """
        if (self.empty_queue_handled):
            Global.log.info(
                "Empty event queue already handled. No action taken.")
            return
        random_node: S8Node = simulation.nodes(
        )[random.randint(0, len(simulation.nodes()) - 1)]

        while (isinstance(random_node, S8Node) == False):
            random_node = simulation.nodes()[random.randint(
                0, len(simulation.nodes()) - 1)]
        Global.log.info(
            "Random node: %d is broadcasting a green message", random_node.id)
        random_node.broadcast_green()
        self.empty_queue_handled = True

    def has_terminated(self) -> bool:
        return super().has_terminated()
