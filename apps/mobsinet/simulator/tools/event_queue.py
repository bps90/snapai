from .event import Event
import heapq


class EventQueue(list[Event]):
    def append(self, event: Event):
        heapq.heappush(self, event)

    def remove(self):
        if not self.is_empty():
            return heapq.heappop(self)

    def is_empty(self):
        return len(self) == 0
