from random import random


class EventInterface:
    TYPE_NOISE = 'noise'
    TYPE_CAUSE = 'cause'
    TYPE_TIME = 'timestamps'

    LABEL_NOISE = 'N'
    LABEL_CAUSE = 'E'
    LABEL_TIME = 'T'

    type = 'undefined'
    mode = 'undefined'
    probability = 1
    position = 0

    def __init__(self, mode: str):
        self.mode = mode

    def setup(self, value_type: str, position: int):
        self.type = value_type
        self.position = position

    def get_type(self) -> str:
        return self.mode

    def generate(self) -> float:
        pass

    def get_probability(self) -> float:
        return self.probability

    def get_label(self) -> str:
        label = self.LABEL_CAUSE if self.type is self.TYPE_CAUSE else self.LABEL_NOISE
        return label + (str(self.position) if self.position is not 0 else '')

    def draw(self) -> bool:
        return random() < self.probability
