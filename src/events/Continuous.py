from random import uniform

from events.EventInterface import EventInterface


class Continuous(EventInterface):
    mode = 'continuous'

    def __init__(self, min_value: float, max_value: float, value_type: str, position: int):
        super(Continuous, self).__init__(value_type, self.mode, position)
        self.__min_value = min_value
        self.__max_value = max_value

    def generate(self) -> float:
        return uniform(self.__min_value, self.__max_value)
