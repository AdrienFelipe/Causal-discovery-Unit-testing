from random import uniform

from events.EventInterface import EventInterface


class Uniform(EventInterface):

    def __init__(self, min: float, max: float, round: int = None, **kwargs):
        super().__init__(**kwargs)
        self.__min = min
        self.__max = max
        self.__round = round

    def generate(self) -> float:
        value = uniform(self.__min, self.__max)
        if self.__round is not None:
            value = round(value, self.__round)
        return value
