import random
import unittest
from typing import Callable

import numpy as np
import pandas as pd

from Generator import Generator
from events.History import History


class GeneratorTest(unittest.TestCase):

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
    def test_continuous_random_samples():
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
    def test_discrete_ordered():
        random.seed(14)
        cause_function: Callable[[History], float] = lambda history: \
            1 if history.get_event(0, delay=1) == 1 else None

        dataset = Generator(cause_function, ordered=True) \
            .add_noise_discrete() \
            .add_cause_discrete() \
            .generate(4)

        expected = pd.DataFrame({'E': [0, 1, 0, 0], 'N': [1, 0, 0, 0], 'X': [0, 0, 1, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_ordered():
        random.seed(14)
        cause_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(0, delay=1) + 3

        dataset = Generator(cause_function, ordered=True) \
            .add_noise_continuous() \
            .add_cause_continuous() \
            .generate(4) \
            .astype(int)

        expected = pd.DataFrame({'E': [0, 9, 0, 0], 'N': [7, 0, 0, 2], 'X': [0, 0, 21, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_pattern_search():
        cause_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_event(0) * np.pi / 2)

        dataset = Generator(cause_function) \
            .add_noise_linear(start=-2, step=0.5) \
            .add_cause_linear() \
            .generate() \
            .round(1)

        expected = pd.DataFrame({'E': [1, 2, 3], 'N': [-1.5, -1, -0.5], 'X': [1, 0, -1]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_with_time():
        cause_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_timestamp() / 60 / 5 * np.pi / 2)

        dataset = Generator(cause_function) \
            .set_time('2018-05-13 20:15', step='5m') \
            .generate(5)

        expected = pd.DataFrame({
            'T': [1526235300, 1526235600, 1526235900, 1526236200, 1526236500],
            'X': [-1, 0, 1, 0, -1]
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    def test_multiple(self):
        self.skipTest('wip')
        cause_function: Callable[[History], float] = lambda history: \
            history.get_event(0) + history.get_event(1)

        dataset = Generator(cause_function) \
            .add_noise_continuous() \
            .add_cause_continuous() \
            .add_cause_continuous() \
            .generate()

        expected = pd.DataFrame({
            'T': [1526235300, 1526235600, 1526235900, 1526236200, 1526236500],
            'X': [-1, 0, 1, 0, -1]
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    def test_search(self):
        for seed in range(20):
            random.seed(seed)

            cause_function: Callable[[History], float] = lambda history: \
                1 if history.get_event(0, delay=1) == 1 else None

            dataset = Generator(cause_function, ordered=True) \
                .add_noise_discrete(0.3) \
                .add_cause_discrete(0.3) \
                .generate(4)
            d = 3


if __name__ == '__main__':
    unittest.main()
