from __future__ import annotations

import math
from random import gauss
from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History
from generator.events.Discrete import Discrete
from generator.relation.RelationPlot import RelationPlot


class DirectCausalityDataset(DatasetInterface):
    name = 'Direct Causality'
    node_size = RelationPlot.BIG_NODE_SIZE
    noise = 0.5

    def __init__(self, case: str, function: Callable, *args, **kwargs):
        super().__init__(self.name, case, *args, **kwargs)
        self.__function = function

    def get_generator(self) -> Generator:
        return Generator() \
            .add_discrete(10) \
            .add_discrete(10) \
            .add_discrete(10) \
            .add_discrete(10, label='Cause') \
            .add_function(self.__function, label='Effect')

    @staticmethod
    def discrete(*args, **kwargs) -> DirectCausalityDataset:
        def function(h: History):
            # Place value in a [-10; 10] range, from a [0, 9] input range.
            value = (h.e(4) - 0) / (9 - 0) * 20 - 10
            # Apply a sigmoid probability distribution.
            probability = 1 / (1 + math.exp(-value))
            weights = (1 - probability, probability)
            return Discrete(weights=weights).generate()

        return DirectCausalityDataset('Discrete', function, *args, **kwargs)

    @staticmethod
    def linear(*args, **kwargs) -> DirectCausalityDataset:
        function = lambda h: 20 * h.e(4) + 10 + gauss(0, DirectCausalityDataset.noise)

        return DirectCausalityDataset('Linear', function, *args, **kwargs)

    @staticmethod
    def square_root(*args, **kwargs) -> DirectCausalityDataset:
        function = lambda h: 20 * math.sqrt(h.e(4) + 1) + 10 + gauss(0, DirectCausalityDataset.noise)

        return DirectCausalityDataset('Square root', function, *args, **kwargs)

    @staticmethod
    def power(*args, **kwargs) -> DirectCausalityDataset:
        function = lambda h: 20 * h.e(4) ** 2 + 10 + gauss(0, DirectCausalityDataset.noise)

        return DirectCausalityDataset('Power', function, *args, **kwargs)

    @staticmethod
    def exponential(*args, **kwargs) -> DirectCausalityDataset:
        function = lambda h: 20 * math.exp(h.e(4) / 10) + 10 + gauss(0, DirectCausalityDataset.noise)

        return DirectCausalityDataset('Exponential', function, *args, **kwargs)
