from __future__ import annotations

from random import gauss
from typing import Callable, List

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.relation.RelationPlot import RelationPlot


class RelationalCausalityDataset(DatasetInterface):
    name = 'Relational Causality'
    node_size = RelationPlot.NODE_SIZE_BIG

    def __init__(self, case: str, functions: List[Callable], *args, **kwargs):
        super().__init__(self.name, case, *args, **kwargs)
        self.__functions = functions

    def get_generator(self) -> Generator:
        return Generator() \
            .add_discrete(3, label='Cause 1') \
            .add_discrete(3, label='Cause 2') \
            .add_discrete(3) \
            .add_discrete(3) \
            .add_function(self.__functions[0], label='Effect')

    @staticmethod
    def discrete(*args, **kwargs) -> RelationalCausalityDataset:
        functions = [
            lambda h: 'greater' if h.e(1) + gauss(0, 0.1) > h.e(2) + gauss(0, 0.1) else 'lower'
        ]

        return RelationalCausalityDataset('Discrete', functions, *args, **kwargs)
