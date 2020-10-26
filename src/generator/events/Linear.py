from generator.events.EventInterface import EventInterface


class Linear(EventInterface):

    def __init__(self, start: float, step: float, **kwargs):
        super().__init__(**kwargs)
        self.value = start
        self.step = step

    def generate(self) -> float:
        self.value += self.step
        return self.value
