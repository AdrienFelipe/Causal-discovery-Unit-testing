from __future__ import annotations

from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class DelayedEffectDataset(DatasetInterface):
    name = 'delayed-effect'
    samples = 50

    def get_generator(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(delay=2, null_value=0)

        return Generator() \
            .add_uniform(1, 3, round=0) \
            .add_function(event_function, round=0)

    def get_causes(self) -> list:
        return ['E1']

    def get_outcome(self) -> str:
        return 'E2'
