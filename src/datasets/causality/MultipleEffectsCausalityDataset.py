from __future__ import annotations

from random import gauss
from typing import Callable, List

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.relation.RelationPlot import RelationPlot


class MultipleEffectsCausalityDataset(DatasetInterface):
    name = 'Multiple Effects'
    node_size = RelationPlot.NODE_SIZE_BIG
    noise = 5

    def __init__(self, case: str, functions: List[Callable], *args, **kwargs):
        self.__functions = functions
        super().__init__(self.name, case, *args, **kwargs)

    def get_generator(self) -> Generator:
        return Generator() \
            .add_discrete(100, label='Cause') \
            .add_function(self.__functions[0], label='Effect 1') \
            .add_function(self.__functions[1], label='Effect 2') \
            .add_function(self.__functions[2], label='Effect 3') \
            .add_discrete(10) \
            .add_discrete(10) \
            .add_discrete(10) \
            .add_discrete(10)

    @staticmethod
    def discrete(*args, **kwargs) -> MultipleEffectsCausalityDataset:
        function1 = lambda h: round(h.e(1) + gauss(0.5, 1), 0)
        function2 = lambda h: round(h.e(1) + gauss(0.5, 1), 0)
        function3 = lambda h: round(h.e(1) + gauss(0.5, 1), 0)

        return MultipleEffectsCausalityDataset('Discrete', [function1, function2, function3], *args, **kwargs)

    @staticmethod
    def linear(*args, **kwargs) -> MultipleEffectsCausalityDataset:
        function1 = lambda h: 10 * h.e(1) + 10 + gauss(0, MultipleEffectsCausalityDataset.noise)
        function2 = lambda h: h.e(1) / 2 + 50 + gauss(0, MultipleEffectsCausalityDataset.noise)
        function3 = lambda h: 5 * h.e(1) + gauss(0, MultipleEffectsCausalityDataset.noise)

        return MultipleEffectsCausalityDataset('Linear', [function1, function2, function3], *args, **kwargs)

    @staticmethod
    def power(*args, **kwargs) -> MultipleEffectsCausalityDataset:
        function1 = lambda h: h.e(1) ** 2 + gauss(0, MultipleEffectsCausalityDataset.noise)
        function2 = lambda h: 150 - h.e(1) ** 3 + 50 + gauss(0, MultipleEffectsCausalityDataset.noise)
        function3 = lambda h: 2 * h.e(1) ** 1.2 + gauss(0, MultipleEffectsCausalityDataset.noise)

        return MultipleEffectsCausalityDataset('Power', [function1, function2, function3], *args, **kwargs)
