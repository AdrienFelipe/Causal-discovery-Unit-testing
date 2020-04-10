import random
import unittest
from typing import Callable

import pandas as pd

from Generator import Generator
from events.History import History


class MyTestCase(unittest.TestCase):

    @staticmethod
    def test_discrete_instant_action():
        random.seed(1)
        cause_function: Callable[[History], float] = lambda history: \
            1 if history.get_event(0) == 1 else 0

        dataset = Generator(cause_function) \
            .add_noise_discrete() \
            .add_cause_discrete() \
            .generate()

        expected = pd.DataFrame({'E': [1, 0, 0], 'N': [0, 1, 0], 'X': [1, 0, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_random():
        random.seed(10)
        cause_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(0)

        dataset = Generator(cause_function) \
            .add_noise_continuous() \
            .add_cause_continuous() \
            .generate().astype(int)

        expected = pd.DataFrame({'E': [4, 2, 8], 'N': [5, 5, 8], 'X': [8, 4, 16]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_log_like():
        random.seed(14)
        cause_function: Callable[[History], float] = lambda history: \
            1 if history.get_event(0, time=1) == 1 else None

        dataset = Generator(cause_function, ordered=True) \
            .add_noise_discrete() \
            .add_cause_discrete() \
            .generate(4)

        expected = pd.DataFrame({'E': [0, 1, 0, 0], 'N': [1, 0, 0, 0], 'X': [0, 0, 1, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    def test_search(self):
        for seed in range(20):
            random.seed(seed)

            cause_function: Callable[[History], float] = lambda history: \
                1 if history.get_event(0, time=1) == 1 else None

            dataset = Generator(cause_function, ordered=True) \
                .add_noise_discrete(0.3) \
                .add_cause_discrete(0.3) \
                .generate(4)
            d = 3


if __name__ == '__main__':
    unittest.main()
