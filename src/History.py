from collections import deque
from datetime import datetime

from events.EventInterface import EventInterface


class History:
    DEFAULT_POSITION = 1
    DEFAULT_DELAY = 0

    def __init__(self):
        self.events = deque()
        self.timestamps = deque()
        self.events_size = 0

    def start(self, events_count:int):
        self.events.clear()
        self.timestamps.clear()
        self.events_size = events_count

    def add_sample(self, timestamp: float):
        self.events.appendleft([None] * self.events_size)
        self.timestamps.appendleft(timestamp)

    def set_event(self, event: EventInterface, value: float):
        self.events[0][event.position] = value

    def get_event(self, position: int = DEFAULT_POSITION, delay: int = DEFAULT_DELAY, null_value=None):
        try:
            value = self.events[delay][position - self.DEFAULT_POSITION]
            return value if value is not None else null_value
        except:
            return null_value

    def get_timestamp(self, delay: int = DEFAULT_DELAY) -> float:
        return self.timestamps[delay]

    def get_datetime(self, delay: int = DEFAULT_DELAY) -> datetime:
        return datetime.fromtimestamp(self.get_timestamp(delay))
