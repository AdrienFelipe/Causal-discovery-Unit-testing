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
        self.__time = None
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

    def get_events(self) -> List[EventInterface]:
        return self.__events

    def __add_event(self, event: EventInterface) -> Generator:
        event.setup(self.__events)
        self.__events.append(event)
        return self

    def add_function(self, event_function: Callable[[History], float], **kwargs) -> Generator:
        return self.__add_event(Effect(event_function, self.history, **kwargs))

    def add_continuous(self, min: int = 0, max: int = 10, **kwargs) -> Generator:
        return self.__add_event(Continuous(min, max, **kwargs))

    def add_discrete(self, weight: float = 0.5, **kwargs) -> Generator:
        return self.__add_event(Discrete(weight, **kwargs))

    def add_linear(self, start: float = 0, step: float = 1, **kwargs) -> Generator:
        return self.__add_event(Linear(start, step, **kwargs))

    def set_time(self, start_date: str = None, step: str = '1m', precision: str = None, **kwargs) -> Generator:
        self.__time = Time(start_date, step, precision, **kwargs)
        return self

    def get_time(self) -> Union[Time, None]:
        return self.__time

    def __next_timestamp(self) -> float:
        return time.time() if self.get_time() is None else self.get_time().generate()

    def build_relations(self) -> List[Relation]:
        events = [event for event in self.get_events() if isinstance(event, Effect)]
        return RelationFactory.build_relations(events)

    def plot_relations(self):
        RelationPlot.show(self.get_events(), self.build_relations())
