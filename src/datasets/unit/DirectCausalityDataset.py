from __future__ import annotations

import math
from random import gauss
from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator


class DirectCausalityDataset(DatasetInterface):
    name = 'Direct Causality'
    noise = 0.5

    def __init__(self, case: str, function: Callable, *args, **kwargs):
        self.__function = function
        super().__init__(self.name, case, *args, **kwargs)

    def get_generator(self) -> Generator:
        return Generator() \
            .add_uniform() \
            .add_discrete() \
            .add_gaussian() \
            .add_function(self.__function, round=2) \
            .add_constant()

    @staticmethod
    def linear(*args, **kwargs) -> DirectCausalityDataset:
        function = lambda h: 20 * h.e(1) + 10 + gauss(0, DirectCausalityDataset.noise)

        return DirectCausalityDataset('Linear', function, *args, **kwargs)

    @staticmethod
    def square_root(*args, **kwargs) -> DirectCausalityDataset:
        function = lambda h: 20 * math.sqrt(h.e(1) + 1) + 10 + gauss(0, DirectCausalityDataset.noise)

        return DirectCausalityDataset('Square root', function, *args, **kwargs)

    @staticmethod
    def power(*args, **kwargs) -> DirectCausalityDataset:
        function = lambda h: 20 * h.e(1) ** 2 + 10 + gauss(0, DirectCausalityDataset.noise)

        return DirectCausalityDataset('Power', function, *args, **kwargs)

    @staticmethod
    def exponential(*args, **kwargs) -> DirectCausalityDataset:
        function = lambda h: 20 * math.exp(h.e(1) / 10) + 10 + gauss(0, DirectCausalityDataset.noise)

        return DirectCausalityDataset('Exponential', function, *args, **kwargs)
