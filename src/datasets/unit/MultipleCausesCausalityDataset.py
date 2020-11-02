from __future__ import annotations

import math
from random import gauss
from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History
from generator.events.Discrete import Discrete
from generator.relation.RelationPlot import RelationPlot


class MultipleCausesCausalityDataset(DatasetInterface):
    name = 'Multiple Causes'
    node_size = RelationPlot.NODE_SIZE_BIG
    noise = 1

    def __init__(self, case: str, function: Callable, *args, **kwargs):
        self.__function = function
        super().__init__(self.name, case, *args, **kwargs)

    def get_generator(self) -> Generator:
        return Generator() \
            .add_discrete(10, label='Cause 1') \
            .add_discrete(20, label='Cause 2') \
            .add_discrete(5) \
            .add_discrete(3) \
            .add_function(self.__function, label='Effect')

    @staticmethod
    def discrete(*args, **kwargs) -> MultipleCausesCausalityDataset:
        def function(h: History):
            sharpness = 7

            # Place value in a [-sharpness; sharpness] range, from a [0, 9] input range.
            value1 = (h.e(1) - 0) / (9 - 0) * (sharpness * 2) - sharpness
            # Apply a sigmoid probability distribution.
            probability1 = 1 / (1 + math.exp(-value1))

            # Place value in a [-sharpness; sharpness] range, from a [0, 19] input range.
            value2 = (h.e(2) - 0) / (19 - 0) * (sharpness * 2) - sharpness
            # Apply a sigmoid probability distribution.
            probability2 = 1 / (1 + math.exp(-value2))

            probability = 1 / 2 * (probability1 + probability2)
            weights = (1 - probability, probability)

            return Discrete(weights=weights).generate()

        return MultipleCausesCausalityDataset('Discrete', function, *args, **kwargs)

    @staticmethod
    def linear(*args, **kwargs) -> MultipleCausesCausalityDataset:
        function = lambda h: 10 * h.e(1) + 5 * h.e(3) + 10 + gauss(0, MultipleCausesCausalityDataset.noise)

        return MultipleCausesCausalityDataset('Linear', function, *args, **kwargs)

    @staticmethod
    def power(*args, **kwargs) -> MultipleCausesCausalityDataset:
        function = lambda h: h.e(1) ** 2 - h.e(3) ** 3 + 10 + gauss(0, MultipleCausesCausalityDataset.noise)

        return MultipleCausesCausalityDataset('Power', function, *args, **kwargs)
