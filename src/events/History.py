from collections import deque


class History:

    def __init__(self):
        self.events = deque()
        self.effects = deque()
        self.timestamps = deque()
        self.events_size = 0
        self.effects_size = 0

    def start(self, events_count: int, effects_count: int):
        self.events.clear()
        self.effects.clear()
        self.timestamps.clear()
        self.events_size = events_count
        self.effects_size = effects_count

    def add_sample(self, timestamp: float):
        self.events.appendleft([None] * self.events_size)
        self.effects.appendleft([None] * self.effects_size)
        self.timestamps.appendleft(timestamp)

    def set_event(self, position: int, value: float):
        self.events[0][position] = value

    def get_event(self, position: int = 0, delay: int = 0, null_value=None):
        try:
            value = self.events[delay][position]
            return value if value is not None else null_value
        except:
            return null_value

    def set_effect(self, position: int, value: float):
        self.effects[0][position] = value

    def get_effect(self, position: int = 0, delay: int = 0, null_value=None):
        try:
            value = self.effects[delay][position]
            return value if value is not None else null_value
        except:
            return null_value

    def get_timestamp(self, delay: int = 0) -> float:
        return self.timestamps[delay]
