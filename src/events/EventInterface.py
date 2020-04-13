from __future__ import annotations

from typing import List


class EventInterface:
    TYPE_NOISE = 'noise'
    TYPE_CAUSE = 'cause'
    TYPE_TIME = 'time'
    TYPE_EFFECT = 'effect'

    LABEL_NOISE = 'N'
    LABEL_CAUSE = 'E'
    LABEL_TIME = 'T'
    LABEL_EFFECT = 'X'

    LABEL_MAPPING = {
        TYPE_NOISE: LABEL_NOISE,
        TYPE_CAUSE: LABEL_CAUSE,
        TYPE_TIME: LABEL_TIME,
    }

    type = 'undefined'
    label = 'undefined'
    probability = 1
    position = 0

    def __init__(self, shadow: bool = False, **kwargs):
        self.shadow = shadow

    def setup(self, value_type: str, events: List[EventInterface]):
        self.type = value_type
        self.position = len(events)
        self.label = self.LABEL_MAPPING[self.type]
        self.__update_labels(events)

    def __update_labels(self, events: List[EventInterface]):
        if self.position > 0:
            self.label += str(self.position + 1)
        if self.position == 1:
            events[0].label += str(self.position)

    def generate(self) -> float:
        pass
