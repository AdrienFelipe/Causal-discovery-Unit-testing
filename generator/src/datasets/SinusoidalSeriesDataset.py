from __future__ import annotations

from typing import Callable

import numpy as np

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class SinusoidalSeriesDataset(DatasetInterface):
    name = 'sinusoidal-series'
    items = 100

    def build(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_timestamp() / 60 / 5 * np.pi / 2)

        return Generator() \
            .set_time('2010-01-02 20:10', step='5m') \
            .add_function(event_function, round=0)

    def get_causes(self) -> list:
        return ['T']

    def get_outcome(self) -> str:
        return 'E1'

    def with_noise(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_timestamp() / 60 / 60 * np.pi / 2)

        return Generator() \
            .set_time('2010-10-20 20:00', step='1h', precision='10m') \
            .add_function(event_function, round=1)
