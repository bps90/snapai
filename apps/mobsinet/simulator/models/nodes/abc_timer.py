from abc import ABC, abstractmethod

from apps.mobsinet.simulator.models.nodes.abc_node_implementation import AbcNodeImplementation
from apps.mobsinet.simulator.network_simulator import simulation


class AbcTimer(ABC):

    def __init__(self):
        self.node_implementation: AbcNodeImplementation | None = None
        self.fire_time: int | None = None

    def start_global_timer(self, time: int):
        """Starts a global timer.

        Parameters
        ----------
        time : int
            The time in unit of time step. Should be greater than 0.

        Raises
        ------
        ValueError
            If the time is less than or equal to 0.

        """

        if (time <= 0):
            raise ValueError("Time should be greater than 0.")

        self.node_implementation = None
        self.fire_time = simulation.global_time + time

        simulation.add_global_timer(self)

    def start_relative(self, time: int, node_implementation: AbcNodeImplementation):
        """Starts a relative timer.

        Parameters
        ----------
            time : int
                The time in unit of time step. Should be greater than 0.
            node_implementation : AbcNodeImplementation
                The node implementation object.

        Raises
        ------
        ValueError
            If the time is less than or equal to 0.
        """

        if (time <= 0):
            raise ValueError("Time should be greater than 0.")

        self.node_implementation = node_implementation
        self.fire_time = simulation.global_time + time

        node_implementation.add_timer(self)

    def start_absolute(self, global_time: int, node_implementation: AbcNodeImplementation):
        """Starts an absolute timer.

        Parameters
        ----------
            global_time : int
                The global time in unit of time step. Should be greater than the current global time.
            node_implementation : AbcNodeImplementation
                The node implementation object.

        Raises
        ------
        ValueError
            If the global time is less than the current global time.
        """

        if (global_time <= simulation.global_time):
            raise ValueError(
                "Global time should be greater than the current global time.")

        self.node_implementation = node_implementation
        self.fire_time = global_time

        node_implementation.add_timer(self)

    def isGlobalTimer(self) -> bool:
        """Checks if the timer is a global timer.

        Returns
        -------
        bool
            True if the timer is a global timer, False otherwise.
        """

        return self.node_implementation is None

    @abstractmethod
    def fire(self):
        """Fires the timer."""
        pass
