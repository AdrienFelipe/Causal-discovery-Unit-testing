from __future__ import annotations

from random import gauss
from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator


class MultipleEffectsCausalityDataset(DatasetInterface):
    name = 'Multiple Effects'
    noise = 5

    def __init__(self, case: str, function1: Callable, function2: Callable, *args, **kwargs):
        self.__function1 = function1
        self.__function2 = function2
        super().__init__(self.name, case, *args, **kwargs)

    def get_generator(self) -> Generator:
        return Generator() \
            .add_uniform(10, 100) \
            .add_uniform(0, 200) \
            .add_uniform(0, 200) \
            .add_function(self.__function1) \
            .add_function(self.__function2)

    @staticmethod
    def linear(*args, **kwargs) -> MultipleEffectsCausalityDataset:
        function1 = lambda h: 10 * h.e(1) + 10 + gauss(0, MultipleEffectsCausalityDataset.noise)
        function2 = lambda h: h.e(1) / 2 + 50 + gauss(0, MultipleEffectsCausalityDataset.noise)

        return MultipleEffectsCausalityDataset('Linear', function1, function2, *args, **kwargs)

    @staticmethod
    def power(*args, **kwargs) -> MultipleEffectsCausalityDataset:
        function1 = lambda h: h.e(1) ** 2 + gauss(0, MultipleEffectsCausalityDataset.noise)
        function2 = lambda h: 150 - h.e(1) ** 3 + 50 + gauss(0, MultipleEffectsCausalityDataset.noise)

        return MultipleEffectsCausalityDataset('Power', function1, function2, *args, **kwargs)
