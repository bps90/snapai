from abc import ABC, abstractmethod
from math import pow


class Event(ABC):
    next_id = 1

    def __init__(self, time: float):
        """
        Creates an event with a given time to execute.
        :param time: The time the event will happen.
        """
        self.time = time
        self.id = Event.next_id
        Event.next_id += 1

    def get_execution_time_string(self, digits: int) -> str:
        """
        Returns a string representation of the time when this event executes,
        truncated to the given number of digits.
        :param digits: The number of digits to display
        :return: A truncated string representation of the execution time
        """
        if digits > 10:
            return str(self.time)
        factor = pow(10, digits)
        temp = round(self.time * factor) / factor
        return str(temp)

    @abstractmethod
    def is_node_event(self) -> bool:
        pass

    @abstractmethod
    def get_event_node(self):
        pass

    @abstractmethod
    def handle(self):
        pass
