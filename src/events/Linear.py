from events.EventInterface import EventInterface


class Linear(EventInterface):
    type = 'linear'

    def __init__(self, start: float, step: float):
        super(Linear, self).__init__(self.mode)
        self.value = start
        self.step = step

    def generate(self) -> float:
        self.value += self.step
        return self.value
