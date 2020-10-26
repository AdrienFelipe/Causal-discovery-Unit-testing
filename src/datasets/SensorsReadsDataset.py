from __future__ import annotations

from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class SensorsReadsDataset(DatasetInterface):
    name = 'sensors-reads'
    samples = 100

    def get_generator(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(delay=1) + 3

        return Generator(sequential=True) \
            .add_uniform(round=0) \
            .add_uniform(round=0) \
            .add_function(event_function, round=0)

    def get_causes(self) -> list:
        return ['E1', 'E2']

    def get_outcome(self) -> str:
        return 'E3'
