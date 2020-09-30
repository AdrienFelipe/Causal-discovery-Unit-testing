from __future__ import annotations

from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class LinearActionDataset(DatasetInterface):
    name = 'linear-action'
    items = 100

    def build(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            2 * history.get_event() + 10

        return Generator() \
            .add_discrete() \
            .add_discrete() \
            .add_function(event_function)

    def get_causes(self) -> list:
        return ['E1', 'E2']

    def get_outcome(self) -> str:
        return 'E3'
