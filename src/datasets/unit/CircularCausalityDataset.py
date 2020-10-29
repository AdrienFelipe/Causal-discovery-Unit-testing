from __future__ import annotations

from random import gauss
from typing import Callable, List

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.relation.RelationPlot import RelationPlot


class CircularCausalityDataset(DatasetInterface):
    name = 'Circular Causality'
    node_size = RelationPlot.BIG_NODE_SIZE

    def __init__(self, case: str, functions: List[Callable], *args, **kwargs):
        super().__init__(self.name, case, *args, **kwargs)
        self.__functions = functions

    def get_generator(self) -> Generator:
        return Generator() \
            .add_function(self.__functions[0], label='Circle 1') \
            .add_function(self.__functions[1], label='Circle 2') \
            .add_function(self.__functions[2], label='Circle 3') \
            .add_function(self.__functions[3], label='Circle 4') \
            .add_discrete(3)

    @staticmethod
    def discrete(*args, **kwargs) -> CircularCausalityDataset:
        functions = [
            lambda h: round((h.e(2, delay=0) or 0) + 0.5 + gauss(0, 1), 0),
            lambda h: round((h.e(3, delay=1) or 0) + 0.5 + gauss(0, 1), 0),
            lambda h: round((h.e(4, delay=2) or 0) + 0.5 + gauss(0, 1), 0),
            lambda h: round((h.e(1, delay=3) or 0) + 0.5 + gauss(0, 1), 0),
        ]

        return CircularCausalityDataset('Discrete', functions, *args, **kwargs)
