from random import choices

from generator.events.EventInterface import EventInterface


class Discrete(EventInterface):

    def __init__(self, weight: float, **kwargs):
        super().__init__(**kwargs)
        self.weight = weight

    def generate(self) -> int:
        population = [0, 1]
        weights = [1 - self.weight, self.weight]
        return choices(population, weights)[0]
