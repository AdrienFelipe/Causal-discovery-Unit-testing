from __future__ import annotations

import random
import time
from typing import Callable
from typing import List
from typing import Union

import pandas as pd

from History import History
from events.Continuous import Continuous
from events.Discrete import Discrete
from events.Effect import Effect
from events.EventInterface import EventInterface
from events.Linear import Linear
from relation.Relation import Relation
from events.Time import Time
from relation.RelationFactory import RelationFactory
from relation.RelationPlot import RelationPlot


class Generator:
    EMPTY_VALUE = 0

    def __init__(self, ordered: bool = False):
        self.__causes = []
        self.__noises = []
        self.__time = None
        self.__effects = []
        self.__ordered = ordered
        self.history = History()

    def generate(self, samples: int = 3) -> pd.DataFrame:
        data = pd.DataFrame()
        self.history.start(events_count=len(self.__causes), effects_count=len(self.__effects))

        events = self.get_noises() + self.get_causes()
        weights = [event.probability for event in events]
        default_sample = {event.label: self.EMPTY_VALUE for event in events + self.get_effects()}

        for _ in range(samples):
            sample = default_sample.copy()
            timestamp = self.__next_timestamp()
            self.history.add_sample(timestamp)
            if self.get_time() is not None and not self.get_time().shadow:
                sample[EventInterface.LABEL_TIME] = timestamp

            if self.__ordered:
                result = None
                for effect in self.get_effects():
                    result = effect.generate()
                    if result is not None:
                        sample[EventInterface.LABEL_EFFECT] = result
                        break

                if result is None:
                    event = random.choices(events, weights)[0]
                    sample[event.label] = value = event.generate()
                    if event.type is EventInterface.TYPE_CAUSE:
                        self.history.set_event(event, value)

                data = data.append(sample, ignore_index=True)
                continue

            # Generate values.
            for event in events + self.get_effects():
                sample[event.label] = value = event.generate()
                if event.type in (EventInterface.TYPE_CAUSE, EventInterface.TYPE_EFFECT):
                    self.history.set_event(event, value)
            data = data.append(sample, ignore_index=True)

            # Remove shadow causes from dataset.
            columns = [event.label for event in events if event.shadow]
            data = data.drop(columns, axis=1)

        return data

    def process_causes(self) -> Union[float, None]:
        try:
            return self.__effects[0](self.history)
        except:
            return None

    def get_noises(self) -> List[EventInterface]:
        return self.__noises

    def get_causes(self) -> List[EventInterface]:
        return self.__causes

    def get_effects(self) -> List[Effect]:
        return self.__effects

    def get_time(self) -> Union[Time, None]:
        return self.__time

    def __next_timestamp(self) -> float:
        return time.time() if self.get_time() is None else self.get_time().generate()

    def __add_noise(self, event: EventInterface) -> Generator:
        event.setup(EventInterface.TYPE_NOISE, self.__noises)
        self.__noises.append(event)
        return self

    def __add_cause(self, event: EventInterface) -> Generator:
        event.setup(EventInterface.TYPE_CAUSE, self.__causes)
        self.__causes.append(event)
        return self

    def add_effect(self, effect_function: Callable[[History], float], **kwargs) -> Generator:
        event = Effect(effect_function, self.history, **kwargs)
        event.setup(EventInterface.TYPE_EFFECT, self.__effects)
        self.__effects.append(event)
        return self

    def add_noise_continuous(self, min_value: int = 0, max_value: int = 10, **kwargs) -> Generator:
        return self.__add_noise(Continuous(min_value, max_value, **kwargs))

    def add_cause_continuous(self, min_value: int = 0, max_value: int = 10, **kwargs) -> Generator:
        return self.__add_cause(Continuous(min_value, max_value, **kwargs))

    def add_noise_discrete(self, probability: float = 0.3, **kwargs) -> Generator:
        return self.__add_noise(Discrete(probability, **kwargs))

    def add_cause_discrete(self, probability: float = 0.3, **kwargs) -> Generator:
        return self.__add_cause(Discrete(probability, **kwargs))

    def add_noise_linear(self, start: float = 0, step: float = 1, **kwargs) -> Generator:
        return self.__add_noise(Linear(start, step, **kwargs))

    def add_cause_linear(self, start: float = 0, step: float = 1, **kwargs) -> Generator:
        return self.__add_cause(Linear(start, step, **kwargs))

    def set_time(self, start_date: str = None, step: str = '1m', precision: str = None, **kwargs) -> Generator:
        self.__time = Time(start_date, step, precision, **kwargs)
        return self

    def build_relations(self) -> List[Relation]:
        return RelationFactory.build_relations(self.get_effects())

    def plot_relations(self):
        RelationPlot.show(self.get_effects(), self.build_relations())

