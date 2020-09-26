from collections import deque
from datetime import datetime

import numpy as np

from generator.events.EventInterface import EventInterface
from tools.TimeParser import TimeParser


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

    def get_range(self, position: int = DEFAULT_POSITION, time_range: str = '1m', null_value=None) -> list:
        try:
            time_limit = self.get_timestamp() - TimeParser.timedelta(time_range).total_seconds()
            np_events = np.array(self.events)
            result = np_events[:, position][np_events[:, 0] > time_limit]
            if null_value is not None:
                result = np.where(result is None, null_value, result)
            return result
        except:
            return [null_value]

    def get_timestamp(self, delay: int = DEFAULT_DELAY) -> float:
        if delay is 0 and self.time_buffer is not None:
            return self.time_buffer
        return self.events[delay][0]

    def get_datetime(self, delay: int = DEFAULT_DELAY) -> datetime:
        return datetime.fromtimestamp(self.get_timestamp(delay))
