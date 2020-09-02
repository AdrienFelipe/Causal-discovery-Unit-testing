import re
from datetime import timedelta


class TimeParser:
    __REGEX = re.compile(
        r'^((?P<days>[.\d]+?)d)?((?P<hours>[.\d]+?)h)?((?P<minutes>[.\d]+?)m)?((?P<seconds>[.\d]+?)s)?$'
    )

    @staticmethod
    def timedelta(duration: str) -> timedelta:
        """
        Parse a timestamps string e.g. (2h13m) into a timedelta object.
        Source: https://stackoverflow.com/a/4628148/851699

        :param duration: A string identifying a duration.  (eg. 2h13m)
        :return datetime.timedelta: A datetime.timedelta object
        """
        parts = TimeParser.__REGEX.match(duration)
        assert parts is not None, "Could not parse any timestamps information from '{}'. " \
                                  "Examples of valid strings: '8h', '2d8h5m20s', '2m4.5s'" \
            .format(duration)
        time_params = {name: float(param) for name, param in parts.groupdict().items() if param}

        return timedelta(**time_params)
