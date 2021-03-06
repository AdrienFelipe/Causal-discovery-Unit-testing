from __future__ import annotations

from random import gauss
from typing import Callable, List

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.relation.RelationPlot import RelationPlot


class ChainedCausalityDataset(DatasetInterface):
    name = 'Chained Causality'
    node_size = RelationPlot.NODE_SIZE_BIG
    noise = 0.5

    def __init__(self, case: str, functions: List[Callable], *args, **kwargs):
        self.__functions = functions
        super().__init__(self.name, case, *args, **kwargs)

    def get_generator(self) -> Generator:
        return Generator() \
            .add_uniform(label='Cause') \
            .add_function(self.__functions[0], round=2, label='Chain 1') \
            .add_function(self.__functions[1], round=2, label='Chain 2') \
            .add_function(self.__functions[2], round=2, label='Effect')

    @staticmethod
    def linear(*args, **kwargs) -> ChainedCausalityDataset:
        functions = [
            lambda h: 20 * h.e(1) + 10 + gauss(0, ChainedCausalityDataset.noise),
            lambda h: 10 * h.e(2) - 5 + gauss(0, ChainedCausalityDataset.noise),
            lambda h: 2 * h.e(3) + 20 + gauss(0, ChainedCausalityDataset.noise),
        ]

        return ChainedCausalityDataset('Linear', functions, *args, **kwargs)
