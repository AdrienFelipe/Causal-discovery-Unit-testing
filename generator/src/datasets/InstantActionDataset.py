from __future__ import annotations


from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class InstantActionDataset(DatasetInterface):
    name = 'instant-action'

    def build(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            1 if history.get_event(1) == 1 else 0

        return Generator() \
            .add_discrete() \
            .add_discrete() \
            .add_function(event_function, round=0)

    def get_causes(self) -> list:
        return ['E1', 'E2']

    def get_outcome(self) -> str:
        return 'E3'
