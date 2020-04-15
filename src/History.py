from collections import deque
from datetime import datetime

from events.EventInterface import EventInterface


class History:

    def __init__(self):
        self.causes = deque()
        self.effects = deque()
        self.timestamps = deque()
        self.events_size = 0
        self.effects_size = 0

    def start(self, events_count: int, effects_count: int):
        self.causes.clear()
        self.effects.clear()
        self.timestamps.clear()
        self.events_size = events_count
        self.effects_size = effects_count

    def add_sample(self, timestamp: float):
        self.causes.appendleft([None] * self.events_size)
        self.effects.appendleft([None] * self.effects_size)
        self.timestamps.appendleft(timestamp)

    def set_event(self, event: EventInterface, value: float):
        item = self.effects[0] if event.type is EventInterface.TYPE_EFFECT else self.causes[0]
        item[event.position] = value

    def get_cause(self, position: int = 1, delay: int = 0, null_value=None):
        try:
            value = self.causes[delay][position - 1]
            return value if value is not None else null_value
        except:
            return null_value

    def get_effect(self, position: int = 1, delay: int = 0, null_value=None):
        try:
            value = self.effects[delay][position - 1]
            return value if value is not None else null_value
        except:
            return null_value

    def get_timestamp(self, delay: int = 0) -> float:
        return self.timestamps[delay]

    def get_datetime(self, delay: int = 0) -> datetime:
        return datetime.fromtimestamp(self.get_timestamp(delay))
