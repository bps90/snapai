# GENERATED WITH HELP FROM CHATGPT

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models.nodes.abc_timer import AbcTimer
    from .models.nodes.abc_node import AbcNode


class AbcCustomGlobal(ABC):
    def __init__(self):
        self.global_timers: list['AbcTimer'] = []

    @abstractmethod
    def has_terminated(self) -> bool:
        """
        Determines if the simulation should terminate.
        """

    def on_exit(self):
        """
        Called when the application is exiting.
        """

    def on_fatal_error_exit(self):
        """
        Called when the framework crashes with a fatal error.
        """

    def pre_run(self):
        """
        Called before executing the first round of the simulation.
        """

    def pre_round(self):
        """
        Called before each round of the simulation.
        """

    def post_round(self):
        """
        Called after each round of the simulation.
        """

    def check_project_requirements(self):
        """
        Called at startup to check the project requirements.
        """

    def node_added_event(self, node: 'AbcNode'):
        """
        Called whenever a node is added to the framework.
        """

    def node_removed_event(self, node: 'AbcNode'):
        """
        Called whenever a node is removed from the framework.
        """

    def handle_global_timers(self):
        """
        Handles all global timers scheduled to execute before or at the current time.
        """
        from .global_vars import Global

        if not self.global_timers or len(self.global_timers) == 0:
            return

        self.global_timers.sort(key=lambda t: t.fire_time)

        while self.global_timers[0].fire_time <= Global.current_time:
            timer = self.global_timers[0]
            self.global_timers.remove(timer)
            timer.fire()
            Global.round_logs.append(
                f'Global timer {timer.__class__.__name__} {timer.node.id} fired')

    def handle_empty_event_queue(self):
        """
        Called when the event queue is empty.
        """
        pass
