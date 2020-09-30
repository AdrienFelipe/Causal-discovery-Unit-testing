from __future__ import annotations

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator


class MultipleEffectsDataset(DatasetInterface):
    name = 'multiple-effects'
    items = 100

    def build(self) -> Generator:
        return Generator() \
            .add_uniform() \
            .add_function(lambda history: int(history.get_event()) * 2) \
            .add_function(lambda history: history.get_event() + 1)

    def get_causes(self) -> list:
        return ['E1', 'E2']

    def get_outcome(self) -> str:
        return 'E3'
