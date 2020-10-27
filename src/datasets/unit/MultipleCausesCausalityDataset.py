from __future__ import annotations

from random import gauss
from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator


class MultipleCausesCausalityDataset(DatasetInterface):
    name = 'Multiple Causes'
    noise = 1

    def __init__(self, case: str, function: Callable, *args, **kwargs):
        self.__function = function
        super().__init__(self.name, case, *args, **kwargs)

    def get_generator(self) -> Generator:
        return Generator() \
            .add_uniform(10, 100) \
            .add_constant(8) \
            .add_constant(80) \
            .add_function(self.__function)

    @staticmethod
    def linear(*args, **kwargs) -> MultipleCausesCausalityDataset:
        function = lambda h: 10 * h.e(1) + 5 * h.e(2) + 10 + gauss(0, MultipleCausesCausalityDataset.noise)

        return MultipleCausesCausalityDataset('Linear', function, *args, **kwargs)

    @staticmethod
    def power(*args, **kwargs) -> MultipleCausesCausalityDataset:
        function = lambda h: h.e(1) ** 2 - h.e(2) ** 3 + 10 + gauss(0, MultipleCausesCausalityDataset.noise)

        return MultipleCausesCausalityDataset('Power', function, *args, **kwargs)
