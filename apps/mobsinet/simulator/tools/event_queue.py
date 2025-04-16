from .event import Event


class EventQueue(list[Event]):
    def append(self, event: Event):
        super().append(event)
        super().sort(key=lambda e: e.time)

    def remove(self):
        if not self.is_empty():
            return super().pop(0)

    def is_empty(self):
        return len(self) == 0
