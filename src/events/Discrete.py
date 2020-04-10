from random import choices

from events.EventInterface import EventInterface


class Discrete(EventInterface):
    type = 'discrete'

    def __init__(self, probability: float, value_type: str, position: int):
        super(Discrete, self).__init__(value_type, self.mode, position)
        self.probability = probability

    def generate(self) -> int:
        population = [0, 1]
        weights = [1 - self.probability, self.probability]
        return choices(population, weights)[0]
