from collections import deque


class History:

    def __init__(self):
        self.events = deque()
        self.timestamps = deque()
        self.size = 0

    def start(self, size: int):
        self.events.clear()
        self.timestamps.clear()
        self.size = size

    def add_sample(self, timestamp: float):
        self.events.appendleft([None] * self.size)
        self.timestamps.appendleft(timestamp)

    def set_event(self, position: int, value: float):
        self.events[0][position] = value

    def get_event(self, position: int = 0, delay: int = 0, null_value=None):
        try:
            value = self.events[delay][position]
            return value if value is not None else null_value
        except:
            return null_value

    def get_timestamp(self, delay: int = 0) -> float:
        return self.timestamps[delay]
