from __future__ import annotations

import random
from typing import Callable
from typing import List
from typing import Union

import pandas as pd

from events.Continuous import Continuous
from events.Discrete import Discrete
from events.EventInterface import EventInterface
from events.History import History
from events.Linear import Linear


class Generator:
    EMPTY_VALUE = 0

    def __init__(self, cause_function: Callable[[History], float], ordered: bool = False):
        self.__causes = []
        self.__noises = []
        self.__cause_function = cause_function
        self.__ordered = ordered
        self.history = History()

    def generate(self, samples: int = 3) -> pd.DataFrame:
        data = pd.DataFrame()
        self.history.start(size=len(self.get_causes()))

        events = self.get_noises() + self.get_causes()
        weights = [event.probability for event in events]
        default_sample = {event.get_label(): self.EMPTY_VALUE for event in events}
        default_sample['X'] = self.EMPTY_VALUE

        for _ in range(samples):
            sample = default_sample.copy()
            self.history.add_sample()

            if self.__ordered:
                result = self.process_causes()
                if result is not None:
                    sample['X'] = result

                else:
                    event = random.choices(events, weights)[0]
                    sample[event.get_label()] = value = event.generate()
                    if event.type is EventInterface.TYPE_CAUSE:
                        self.history.set_event(event.position, value)

                data = data.append(sample, ignore_index=True)
                continue

            # Generate values.
            for event in events:
                label = event.get_label()
                sample[label] = value = event.generate()
                if event.type is EventInterface.TYPE_CAUSE:
                    self.history.set_event(event.position, value)

            sample['X'] = self.__cause_function(self.history)
            data = data.append(sample, ignore_index=True)

        return data

    def process_causes(self) -> Union[float, None]:
        try:
            return self.__cause_function(self.history)
        except:
            return None

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

    def __add_noise(self, event: EventInterface) -> Generator:
        position = self.__add_position(self.__noises)
        event.setup(EventInterface.TYPE_NOISE, position)
        self.__noises.append(event)

        return self

    def __add_cause(self, event: EventInterface) -> Generator:
        position = self.__add_position(self.__causes)
        event.setup(EventInterface.TYPE_CAUSE, position)
        self.__causes.append(event)

        return self

    def add_noise_continuous(self, min_value: int = 0, max_value: int = 10) -> Generator:
        return self.__add_noise(Continuous(min_value, max_value))

    def add_noise_discrete(self, probability: float = 0.3) -> Generator:
        return self.__add_noise(Discrete(probability))

    def add_cause_continuous(self, min_value: int = 0, max_value: int = 10) -> Generator:
        return self.__add_cause(Continuous(min_value, max_value))

    def add_cause_discrete(self, probability: float = 0.3) -> Generator:
        return self.__add_cause(Discrete(probability))

    def add_noise_linear(self, start: float = 0, step: float = 1) -> Generator:
        return self.__add_noise(Linear(start, step))

    def add_cause_linear(self, start: float = 0, step: float = 1) -> Generator:
        return self.__add_cause(Linear(start, step))
