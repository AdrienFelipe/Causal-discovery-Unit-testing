from __future__ import annotations

from random import gauss
from typing import Callable, List

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator


class ChainedCausalityDataset(DatasetInterface):
    name = 'Chained Causality'
    noise = 0.5

    def __init__(self, case: str, functions: List[Callable], *args, **kwargs):
        self.__functions = functions
        super().__init__(self.name, case, *args, **kwargs)

    def get_generator(self) -> Generator:
        return Generator() \
            .add_uniform() \
            .add_uniform() \
            .add_function(self.__functions[0], round=2) \
            .add_function(self.__functions[1], round=2) \
            .add_function(self.__functions[2], round=2) \
            .add_uniform()

    @staticmethod
    def linear(*args, **kwargs) -> ChainedCausalityDataset:
        functions = [
            lambda h: 20 * h.e(1) + 10 + gauss(0, ChainedCausalityDataset.noise),
            lambda h: 10 * h.e(3) - 5 + gauss(0, ChainedCausalityDataset.noise),
            lambda h: 2 * h.e(4) + 20 + gauss(0, ChainedCausalityDataset.noise),
        ]

        return ChainedCausalityDataset('Linear', functions, *args, **kwargs)
