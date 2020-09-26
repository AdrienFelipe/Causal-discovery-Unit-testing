from generator.events.EventInterface import EventInterface


class Constant(EventInterface):

    def __init__(self, value: float, **kwargs):
        super().__init__(**kwargs)
        self.__value = value

    def generate(self) -> float:
        return self.__value
