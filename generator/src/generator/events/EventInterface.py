from __future__ import annotations

from random import random
from typing import List


class EventInterface:
    TYPE_TIME = 'time'
    TYPE_EVENT = 'effect'

    LABEL_TIME = 'T'
    LABEL_EVENT = 'E'

    LABEL_MAPPING = {
        TYPE_TIME: LABEL_TIME,
        TYPE_EVENT: LABEL_EVENT,
    }

    type = TYPE_EVENT
    position = 0

    def __init__(self, probability: float = 1, shadow: bool = False, label=None, **kwargs):
        self.probability = probability
        self.shadow = shadow
        self.label = label

    def setup(self, events: List[EventInterface]):
        self.position = len(events)
        if self.label is None:
            self.label = self.LABEL_MAPPING[self.type]
            if self.position is not 0:
                self.label += str(self.position)

    def draw(self) -> bool:
        return random() < self.probability

    def generate(self) -> float:
        pass

    def __hash__(self):
        return self.position
