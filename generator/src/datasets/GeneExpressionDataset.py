from __future__ import annotations

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class GeneExpressionDataset(DatasetInterface):
    name = 'gene-expression'

    def get_generator(self) -> Generator:
        return self.simple()

    def simple(self) -> Generator:
        return Generator() \
            .add_uniform(0, 1, round=1) \
            .add_uniform(0, 1, round=1) \
            .add_uniform(0, 1, round=1) \
            .add_uniform(0, 1, round=1) \
            .add_uniform(0, 1, round=1) \
            .add_function(lambda h: h.e(1) > 0.3 and h.e(2) > 0.8 or h.e(3) < 0.3, label='P', round=3)

    def complex(self) -> Generator:
        return Generator() \
            .add_uniform(0, 1, round=3) \
            .add_uniform(0, 1, round=3, shadow=True) \
            .add_uniform(0, 1, round=3) \
            .add_uniform(0, 1, round=3) \
            .add_function(lambda h: (h.e(3) + h.e(4)) / 2, round=3) \
            .add_uniform(0, 1, round=3) \
            .add_uniform(0, 1, round=3) \
            .add_function(self.pathology, label='P', round=3)

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
