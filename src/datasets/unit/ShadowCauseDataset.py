from __future__ import annotations

from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class ShadowCauseDataset(DatasetInterface):
    name = 'shadow-cause'

    def get_generator(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            history.get_event(1) + history.get_event(2)

        return Generator() \
            .add_uniform(shadow=True) \
            .add_uniform() \
            .add_function(event_function)
