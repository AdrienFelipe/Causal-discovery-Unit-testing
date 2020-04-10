from __future__ import annotations

import random
from collections import deque
from typing import Callable
from typing import List

import pandas as pd

from events.Continuous import Continuous
from events.Discrete import Discrete
from events.EventInterface import EventInterface


class Generator:
    EMPTY_VALUE = 0

    def __init__(self, cause_function: Callable[[deque], float], ordered: bool = False):
        self.__causes = []
        self.__noises = []
        self.__cause_function = cause_function
        self.__ordered = ordered

    def generate(self, samples: int = 3) -> pd.DataFrame:
        data = pd.DataFrame()

        events = self.get_noises() + self.get_causes()
        weights = [event.probability for event in events]
        default_sample = {event.get_label(): self.EMPTY_VALUE for event in events}
        default_sample['X'] = self.EMPTY_VALUE
        cause_values = deque()

        for _ in range(samples):
            sample = default_sample.copy()
            cause_values.appendleft([None] * len(self.__causes))

            if self.__ordered:
                result = self.__cause_function(cause_values)
                if result is not None:
                    sample['X'] = result

                else:
                    event = random.choices(events, weights)[0]
                    sample[event.get_label()] = value = event.generate()
                    if event.type is EventInterface.TYPE_CAUSE:
                        cause_values[0][event.position] = value

                data = data.append(sample, ignore_index=True)
                continue

            # Generate values.
            for event in events:
                label = event.get_label()
                sample[label] = value = event.generate()
                if event.type is EventInterface.TYPE_CAUSE:
                    cause_values[0][event.position] = value

            sample['X'] = self.__cause_function(cause_values)
            data = data.append(sample, ignore_index=True)

        return data

    def get_noises(self) -> List[EventInterface]:
        return self.__noises

    def get_causes(self) -> List[EventInterface]:
        return self.__causes

    @staticmethod
    def __add_position(values: List[EventInterface]) -> int:
        count = len(values)
        if count == 0:
            return 0
        if count == 1:
            values[0].position = 1
        return count + 1

    def add_noise_continuous(self, min_value: int = 0, max_value: int = 10) -> Generator:
        position = self.__add_position(self.__noises)
        self.__noises.append(Continuous(min_value, max_value, EventInterface.TYPE_NOISE, position))
        return self

    def add_noise_discrete(self, probability: float = 0.3) -> Generator:
        position = self.__add_position(self.__noises)
        self.__noises.append(Discrete(probability, EventInterface.TYPE_NOISE, position))
        return self

    def add_cause_continuous(self, min_value: int = 0, max_value: int = 10) -> Generator:
        position = self.__add_position(self.__causes)
        self.__causes.append(Continuous(min_value, max_value, EventInterface.TYPE_CAUSE, position))
        return self

    def add_cause_discrete(self, probability: float = 0.3) -> Generator:
        position = self.__add_position(self.__causes)
        self.__causes.append(Discrete(probability, EventInterface.TYPE_CAUSE, position))
        return self
