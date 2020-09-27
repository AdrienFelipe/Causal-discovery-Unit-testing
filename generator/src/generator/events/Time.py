import re
from datetime import datetime
from datetime import timedelta
from random import uniform

from generator.events.EventInterface import EventInterface
from utils.TimeParser import TimeParser


class Time(EventInterface):
    type = EventInterface.TYPE_TIME

    __REGEX = re.compile(
        r'^((?P<days>[.\d]+?)d)?((?P<hours>[.\d]+?)h)?((?P<minutes>[.\d]+?)m)?((?P<seconds>[.\d]+?)s)?$'
    )

    def __init__(self, start_date: str = None, step: str = None, precision: str = None, **kwargs):
        super().__init__(**kwargs)
        self.count = 0
        self.start_date = datetime.fromisoformat(start_date) if start_date is not None else datetime.now()
        self.step = TimeParser.timedelta(step) if step is not None else timedelta()
        self.precision = TimeParser.timedelta(precision) if precision is not None else None

    def generate(self) -> float:
        date = self.start_date + self.step * self.count
        self.count += 1
        if self.precision is not None:
            seconds = uniform(-self.precision.total_seconds(), self.precision.total_seconds())
            date += timedelta(seconds=seconds)
        return date.timestamp()
