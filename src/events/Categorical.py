from random import choices

from events.EventInterface import EventInterface


class Categorical(EventInterface):

    def __init__(self, values: tuple = (0, 1), weights: tuple = None, **kwargs):
        super().__init__(**kwargs)
        self.__values = values
        self.__weights = ((1,) * len(values)) if weights is None else weights

    def generate(self) -> int:
        return choices(self.__values, self.__weights)[0]
