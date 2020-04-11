from collections import deque


class History:

    def __init__(self):
        self.events = deque()
        self.size = 0

    def start(self, size: int):
        self.events.clear()
        self.size = size

    def add_sample(self):
        self.events.appendleft([None] * self.size)

    def set_event(self, position: int, value: float):
        self.events[0][position] = value

    def get_event(self, position: int, time: int = 0, null_value=None):
        try:
            value = self.events[time][position]
            return value if value is not None else null_value
        except:
            return null_value
