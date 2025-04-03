from .event import Event
from ..models.nodes.abc_timer import AbcTimer


class TimerEvent(Event):
    num_timer_events_on_the_fly = 0

    def __init__(self, timer: AbcTimer, time: float):
        """
        Creates a TimerEvent for the given timer, a given time, and a node.
        :param timer: The timer that will fire.
        :param time: The time the timer will fire.
        """
        super().__init__(time)
        self.timer = timer
        TimerEvent.num_timer_events_on_the_fly += 1

    def handle(self):
        """
        Handles the event by triggering the timer.
        """
        if self.timer:
            self.timer.fire()

    def drop(self):
        """
        Called when this event is removed before being handled. No action required.
        """
        pass

    def __str__(self):
        return "TimerEvent"

    def get_event_list_text(self, has_executed: bool) -> str:
        """
        Returns the text to be displayed in the extended control panel for this event.
        :param has_executed: True if the event has already executed.
        """
        if self.timer.node:
            if has_executed:
                return f"Timer at node {self.timer.node.ID}"
            return f"TE (Node:{self.timer.node.ID}, Time:{self.get_execution_time_string(4)})"
        else:
            if has_executed:
                return "Global Timer"
            return f"GTE (Time:{self.get_execution_time_string(4)})"

    def get_event_list_tooltip_text(self, has_executed: bool) -> str:
        """
        Returns the tooltip text for this event.
        :param has_executed: True if the event has already executed.
        """
        if self.timer.node:  # a node timer
            if has_executed:
                return (f"The timer fired at node {self.timer.node.ID}\n"
                        f"The type of the timer was {self.timer.__class__.__name__}")
            return (f"At time {self.time} a timer fires at node {self.timer.node.ID}\n"
                    f"The type of the timer is {self.timer.__class__.__name__}")
        else:  # a global timer
            if has_executed:
                return f"A global timer fired. Its type was {self.timer.__class__.__name__}"
            return (f"At time {self.time} a global timer fires.\n"
                    f"The type of the timer is {self.timer.__class__.__name__}")

    def get_event_node(self):
        """
        Returns the node for which the event is scheduled, or None if it is a global timer event.
        """
        return self.timer.node if self.timer else None

    def is_node_event(self) -> bool:
        """
        Returns True if this event is associated with a node, otherwise False.
        """
        return (self.timer.node != None) if self.timer else False
