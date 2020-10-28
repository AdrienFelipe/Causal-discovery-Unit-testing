from __future__ import annotations

from typing import Callable
from typing import List

import pandas as pd

from generator.History import History
from generator.events.Categorical import Categorical
from generator.events.Constant import Constant
from generator.events.Discrete import Discrete
from generator.events.EventInterface import EventInterface
from generator.events.Function import Function
from generator.events.Gaussian import Gaussian
from generator.events.Linear import Linear
from generator.events.Time import Time
from generator.events.Uniform import Uniform
from generator.relation.Relation import Relation
from generator.relation.RelationFactory import RelationFactory
from generator.relation.RelationPlot import RelationPlot


class Generator:
    EMPTY_VALUE = None

    def __init__(self, sequential: bool = False):
        self.__events = []
        self.__sequential = sequential
        self.history = History()
        self.__add_event(Time(shadow=True))

    def generate(self, samples: int = 3) -> pd.DataFrame:
        data = pd.DataFrame()
        self.history.start(events_count=len(self.__events))
        default_sample = {event.label: self.EMPTY_VALUE for event in self.get_events()}

        events = self.get_events()
        position = 1

        while len(data) < samples:
            sample = default_sample.copy()

            if self.__sequential:
                # Process only one event at a time, but always process time.
                events = [self.get_events()[0], self.get_events()[position]]
                position = position % (len(self.__events) - 1) + 1

            for event in events:
                # Allow event to be executed regarding its probability,
                if not event.draw():
                    continue

                value = event.generate()
                if value is not None:
                    self.history.set_event(event, value)
                    sample[event.label] = value

            # Only add sample if it is not empty.
            if not all(value is None for value in list(sample.values())[1:]):
                data = data.append(sample, ignore_index=True)

        # Remove shadow causes from generator.
        columns = [event.label for event in events if event.shadow]
        data = data.drop(columns, axis=1)

        # Remove line breaks in column names.
        data.columns = data.columns.str.replace("\n", " ")

        return data

    def get_events(self, include_shadow: bool = True) -> List[EventInterface]:
        return self.__events if include_shadow else [event for event in self.__events if not event.shadow]

    def __add_event(self, event: EventInterface) -> Generator:
        event.setup(self.__events)
        self.__events.append(event)
        return self

    def add_function(self, event_function: Callable[[History], float], **kwargs) -> Generator:
        return self.__add_event(Function(event_function, self.history, **kwargs))

    def add_uniform(self, min: int = 0, max: int = 10, **kwargs) -> Generator:
        return self.__add_event(Uniform(min, max, **kwargs))

    def add_gaussian(self, mu: float = 0, sigma: float = 1, **kwargs) -> Generator:
        return self.__add_event(Gaussian(mu, sigma, **kwargs))

    def add_discrete(self, samples: int = 2, weights: tuple = None, **kwargs) -> Generator:
        return self.__add_event(Discrete(samples, weights, **kwargs))

    def add_linear(self, start: float = 0, step: float = 1, **kwargs) -> Generator:
        return self.__add_event(Linear(start, step, **kwargs))

    def add_constant(self, value: float = 1, **kwargs) -> Generator:
        return self.__add_event(Constant(value, **kwargs))

    def add_categorical(self, values: tuple = (0, 1), weights: tuple = None, **kwargs) -> Generator:
        return self.__add_event(Categorical(values, weights, **kwargs))

    def set_time(self, start_date: str = None, step: str = '1m', precision: str = None, **kwargs) -> Generator:
        event = Time(start_date, step, precision, **kwargs)
        event.setup(events=[])
        self.__events[0] = event
        return self

    def get_time(self) -> Time:
        return self.__events[0]

    def build_relations(self) -> List[Relation]:
        events = [event for event in self.get_events() if isinstance(event, Function)]
        return RelationFactory.build_relations(events)

    def plot_relations(self, fig_size=(4, 3), node_size=20):
        RelationPlot.show(self.get_events(), self.build_relations(), fig_size, node_size * 100)
