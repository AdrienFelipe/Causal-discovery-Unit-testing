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
            .add_function(self.__functions[0], data_type=int, label='1') \
            .add_function(self.__functions[1], data_type=int, label='2') \
            .add_function(self.__functions[2], data_type=int, label='3') \
            .add_function(self.__functions[3], data_type=int, label='4') \
            .add_discrete(10, data_type=int)

    @staticmethod
    def discrete(*args, **kwargs) -> CircularCausalityDataset:
        functions = [
            lambda h: (h.e(4, delay=4) or 0) + 0.5 + gauss(0, 1),
            lambda h: (h.e(1, delay=1) or 0) + 0.5 + gauss(0, 1),
            lambda h: (h.e(2, delay=2) or 0) + 0.5 + gauss(0, 1),
            lambda h: (h.e(3, delay=3) or 0) + 0.5 + gauss(0, 1),
        ]

        return CircularCausalityDataset('Discrete', functions, *args, **kwargs)
