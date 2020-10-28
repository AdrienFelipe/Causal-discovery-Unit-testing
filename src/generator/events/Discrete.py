from random import choices

from generator.events.EventInterface import EventInterface


class Discrete(EventInterface):

    def __init__(self, samples: int = 2, weights: tuple = None, **kwargs):
        super().__init__(**kwargs)
        self.samples = samples
        self.weights = weights

    def generate(self) -> int:
        if self.weights is None:
            self.weights = (1,) * self.samples

        return choices(range(self.samples), self.weights)[0]
