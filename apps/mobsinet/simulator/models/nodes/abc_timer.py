from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod
from ...global_vars import Global
from ...network_simulator import simulation
from ...tools.timer_event import TimerEvent

if TYPE_CHECKING:
    from .abc_node import AbcNode


class AbcTimer(ABC):

    def __init__(self):
        self.node: Optional['AbcNode']
        self.fire_time: float

    def start_global_timer(self, time: float):
        """Starts a global timer.

        Parameters
        ----------
        time : float
            The time in unit of time step. Should be greater than 0.

        Raises
        ------
        ValueError
            If the time is less than or equal to 0.

        """

        if (time <= 0):
            raise ValueError("Time should be greater than 0.")

        self.node = None
        self.fire_time = Global.current_time + time

        if (Global.is_async_mode):
            simulation.event_queue.append(
                TimerEvent(self, self.fire_time))
        else:
            Global.custom_global.global_timers.append(self)

    def start_relative(self, time: float, node: 'AbcNode'):
        """Starts a relative timer.

        Parameters
        ----------
            time : float
                The time in unit of time step. Should be greater than 0.
            node : AbcNode
                The node object.

        Raises
        ------
        ValueError
            If the time is less than or equal to 0.
        """

        if (time <= 0):
            raise ValueError("Time should be greater than 0.")

        self.node = node
        self.fire_time = Global.current_time + time

        if (Global.is_async_mode):
            simulation.event_queue.append(
                TimerEvent(self, self.fire_time))
        else:
            node.add_timer(self)

    def start_absolute(self, global_time: int, node: 'AbcNode'):
        """Starts an absolute timer.

        Parameters
        ----------
            global_time : int
                The global time in unit of time step. Should be greater than the current global time.
            node : AbcNode
                The node object.

        Raises
        ------
        ValueError
            If the global time is less than the current global time.
        """

        if (global_time <= Global.current_time):
            raise ValueError(
                "Global time should be greater than the current global time.")

        self.node = node
        self.fire_time = global_time

        if (Global.is_async_mode):
            simulation.event_queue.append(
                TimerEvent(self, self.fire_time))
        else:
            node.add_timer(self)

    def isGlobalTimer(self) -> bool:
        """Checks if the timer is a global timer.

        Returns
        -------
        bool
            True if the timer is a global timer, False otherwise.
        """

        return self.node is None

    @abstractmethod
    def fire(self):
        """Fires the timer."""
