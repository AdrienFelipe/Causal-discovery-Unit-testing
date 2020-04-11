import re
from datetime import datetime
from datetime import timedelta

from events.EventInterface import EventInterface


class Time(EventInterface):
    __REGEX = re.compile(
        r'^((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$'
    )

    type = 'time'

    def __init__(self, start_date: str = None, step: str = '1m'):
        super(Time, self).__init__(self.mode)
        self.date = datetime.fromisoformat(start_date) if start_date is not None else datetime.now()
        self.step = self.__parse_duration(step)

    def generate(self) -> float:
        self.date += self.step
        return self.date.timestamp()

    def __parse_duration(self, duration: str):
        """
        Parse a timestamps string e.g. (2h13m) into a timedelta object.

        Modified from virhilo's answer at https://stackoverflow.com/a/4628148/851699

        :param duration: A string identifying a duration.  (eg. 2h13m)
        :return datetime.timedelta: A datetime.timedelta object
        """
        parts = self.__REGEX.match(duration)
        assert parts is not None, "Could not parse any timestamps information from '{}'.  Examples of valid strings: '8h', '2d8h5m20s', '2m4s'".format(duration)
        time_params = {name: float(param) for name, param in parts.groupdict().items() if param}

        return timedelta(**time_params)
