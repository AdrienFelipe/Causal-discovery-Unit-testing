from collections import deque


class History:

    def __init(self):
        self.events = deque()
        self.size = 0

    def start(self, size:int):
        self.events = deque()
        self.size = size

    def add_time(self):
        self.events.appendleft([None] * self.size)

    def set_event(self, position: int, value: float):
        self.events[0][position] = value

    def get_event(self, position: int, time: int = 0):
        try:
            return self.events[time][position]
        except:
            return None
