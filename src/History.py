from collections import deque
from datetime import datetime

from events.EventInterface import EventInterface


class History:
    DEFAULT_POSITION = 1
    DEFAULT_DELAY = 0

    def __init__(self):
        self.events = deque()
        self.events_size = 0
        self.time_buffer = None

    def start(self, events_count: int):
        self.events.clear()
        self.events_size = events_count

    def __add_sample(self):
        self.events.appendleft([None] * self.events_size)

    def pop_sample(self):
        del self.events[0]

    def set_event(self, event: EventInterface, value: float):
        if event.type is EventInterface.TYPE_TIME and event.position is 0:
            self.time_buffer = value
            return

        elif self.time_buffer is not None:
            self.__add_sample()
            self.events[0][0] = self.time_buffer
            self.time_buffer = None

        self.events[0][event.position] = value

    def get_event(self, position: int = DEFAULT_POSITION, delay: int = DEFAULT_DELAY, null_value=None):
        try:
            value = self.events[delay][position]
            return value if value is not None else null_value
        except:
            return null_value

    def e(self, position: int = DEFAULT_POSITION, delay: int = DEFAULT_DELAY, null_value=None):
        return self.get_event(position, delay, null_value)

    def get_timestamp(self, delay: int = DEFAULT_DELAY) -> float:
        if delay is 0 and self.time_buffer is not None:
            return self.time_buffer
        return self.events[delay][0]

    def get_datetime(self, delay: int = DEFAULT_DELAY) -> datetime:
        return datetime.fromtimestamp(self.get_timestamp(delay))
