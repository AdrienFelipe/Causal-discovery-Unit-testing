from __future__ import annotations

from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class GeneExpressionDataset(DatasetInterface):
    name = 'gene-expression'
    items = 100

    def build(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            history.get_event(1) + history.get_event(2)

        return Generator() \
            .add_uniform(0, 1) \
            .add_uniform(0, 1, shadow=True) \
            .add_uniform(0, 1) \
            .add_uniform(0, 1) \
            .add_function(lambda h: (h.e(3) + h.e(4)) / 2) \
            .add_uniform(0, 1) \
            .add_uniform(0, 1) \
            .add_function(self.pathology, label='P')

    def get_causes(self) -> list:
        return ['E1', 'E3', 'E4', 'E5', 'E6', 'E7']

    def get_outcome(self) -> str:
        return 'P'

    @staticmethod
    def pathology(history: History) -> float:
        gene1 = history.get_event(1) > 0.8
        gene2 = history.get_event(2) > 0.7
        gene5 = history.get_event(5) > 0.6

        return gene1 and gene2 or gene5
