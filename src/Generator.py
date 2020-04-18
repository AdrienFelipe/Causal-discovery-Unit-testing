from __future__ import annotations

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
from events.Time import Time
from relation.Relation import Relation
from relation.RelationFactory import RelationFactory
from relation.RelationPlot import RelationPlot


class Generator:
    EMPTY_VALUE = None

    def __init__(self, sequential: bool = False):
        self.__causes = []
        self.__noises = []
        self.__time = None
        self.__effects = []
        self.__events = []
        self.__sequential = sequential
        self.history = History()

    def generate(self, samples: int = 3) -> pd.DataFrame:
        data = pd.DataFrame()
        self.history.start(events_count=len(self.__events))
        default_sample = {event.label: self.EMPTY_VALUE for event in self.get_events()}

        events = self.get_events()
        position = 0

        while len(data) < samples:
            sample = default_sample.copy()
            timestamp = self.__next_timestamp()
            self.history.add_sample(timestamp)
            if self.get_time() is not None and not self.get_time().shadow:
                sample[EventInterface.LABEL_TIME] = timestamp

            if self.__sequential:
                # Process only one event at a time.
                events = [self.get_events()[position]]
                position = (position + 1) % len(self.__events)

            for event in events:
                # Allow event to be executed regarding its probability,
                if not event.draw():
                    continue

                value = event.generate()
                if value is not None:
                    self.history.set_event(event, value)
                    sample[event.label] = value

            # Only add sample if it is not empty.
            if not all(value is None for value in sample.values()):
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

    def get_events(self) -> List[EventInterface]:
        return self.__events

    def get_time(self) -> Union[Time, None]:
        return self.__time

    def __next_timestamp(self) -> float:
        return time.time() if self.get_time() is None else self.get_time().generate()

    def __add_noise(self, event: EventInterface) -> Generator:
        event.setup(EventInterface.TYPE_NOISE, self.__events)
        self.__noises.append(event)
        self.__events.append(event)
        return self

    def __add_cause(self, event: EventInterface) -> Generator:
        event.setup(EventInterface.TYPE_CAUSE, self.__events)
        self.__causes.append(event)
        self.__events.append(event)
        return self

    def add_effect(self, effect_function: Callable[[History], float], **kwargs) -> Generator:
        event = Effect(effect_function, self.history, **kwargs)
        event.setup(EventInterface.TYPE_EFFECT, self.__events)
        self.__effects.append(event)
        self.__events.append(event)
        return self

    def add_noise_continuous(self, min_value: int = 0, max_value: int = 10, **kwargs) -> Generator:
        return self.__add_noise(Continuous(min_value, max_value, **kwargs))

    def add_cause_continuous(self, min_value: int = 0, max_value: int = 10, **kwargs) -> Generator:
        return self.__add_cause(Continuous(min_value, max_value, **kwargs))

    def add_noise_discrete(self, weight: float = 0.5, **kwargs) -> Generator:
        return self.__add_noise(Discrete(weight, **kwargs))

    def add_cause_discrete(self, weight: float = 0.5, **kwargs) -> Generator:
        return self.__add_cause(Discrete(weight, **kwargs))

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
