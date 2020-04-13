from random import uniform

from events.EventInterface import EventInterface


class Continuous(EventInterface):

    def __init__(self, min_value: float, max_value: float, **kwargs):
        super().__init__(**kwargs)
        self.__min_value = min_value
        self.__max_value = max_value

    def generate(self) -> float:
        return uniform(self.__min_value, self.__max_value)
