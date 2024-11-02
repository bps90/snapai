# GENERATED WITH HELP FROM CHATGPT

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .global_vars import Global

if TYPE_CHECKING:
    from .models.nodes.abc_timer import AbcTimer


class AbcCustomGlobal(ABC):
    global_timers: list['AbcTimer'] = []

    @abstractmethod
    def has_terminated(self) -> bool:
        """
        Determines if the simulation should terminate.
        """
        pass


    def on_exit(self):
        """
        Called when the application is exiting.
        """
        pass

    def on_fatal_error_exit(self):
        """
        Called when the framework crashes with a fatal error.
        """
        pass

    def pre_run(self):
        """
        Called before executing the first round of the simulation.
        """
        pass

    def pre_round(self):
        """
        Called before each round of the simulation.
        """
        pass

    def post_round(self):
        """
        Called after each round of the simulation.
        """
        pass

    def check_project_requirements(self):
        """
        Called at startup to check the project requirements.
        """
        pass

    def node_added_event(self, node):
        """
        Called whenever a node is added to the framework.
        """
        pass

    def node_removed_event(self, node):
        """
        Called whenever a node is removed from the framework.
        """
        pass

    def handle_global_timers(self):
        """
        Handles all global timers scheduled to execute before or at the current time.
        """
        if not self.global_timers:
            return
        
        self.global_timers.sort(key=lambda t: t.fire_time)
        
        while self.global_timers[0].fire_time <= Global.current_time:
            timer = self.global_timers[0]
            self.global_timers.remove(timer)
            timer.fire()
