import random
import unittest
from typing import Callable

import numpy as np
import pandas as pd

from Generator import Generator
from History import History
from events.EventInterface import EventInterface


class GeneratorTest(unittest.TestCase):

    @staticmethod
    def test_discrete_instant_action():
        random.seed(1)
        effect_function: Callable[[History], float] = lambda history: \
            1 if history.get_cause(0) == 1 else 0

        dataset = Generator() \
            .add_effect(effect_function) \
            .add_noise_discrete() \
            .add_cause_discrete() \
            .generate()

        expected = pd.DataFrame({'C': [1, 0, 0], 'E': [1, 0, 0], 'N': [0, 1, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_random_samples():
        random.seed(10)
        effect_function: Callable[[History], float] = lambda history: \
            2 * history.get_cause(0)

        dataset = Generator() \
            .add_effect(effect_function) \
            .add_noise_continuous() \
            .add_cause_continuous() \
            .generate().astype(int)

        expected = pd.DataFrame({'C': [4, 2, 8], 'E': [8, 4, 16], 'N': [5, 5, 8]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_discrete_ordered():
        random.seed(14)
        effect_function: Callable[[History], float] = lambda history: \
            1 if history.get_cause(0, delay=1) == 1 else None

        dataset = Generator(ordered=True) \
            .add_effect(effect_function) \
            .add_noise_discrete() \
            .add_cause_discrete() \
            .generate(4)

        expected = pd.DataFrame({'C': [0, 1, 0, 0], 'E': [0, 0, 1, 0], 'N': [1, 0, 0, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_ordered():
        random.seed(14)
        effect_function: Callable[[History], float] = lambda history: \
            2 * history.get_cause(0, delay=1) + 3

        dataset = Generator(ordered=True) \
            .add_effect(effect_function) \
            .add_noise_continuous() \
            .add_cause_continuous() \
            .generate(4) \
            .astype(int)

        expected = pd.DataFrame({'C': [0, 9, 0, 0], 'E': [0, 0, 21, 0], 'N': [7, 0, 0, 2]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_pattern_search():
        effect_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_cause(0) * np.pi / 2)

        dataset = Generator() \
            .add_effect(effect_function) \
            .add_noise_linear(start=-2, step=0.5) \
            .add_cause_linear() \
            .generate() \
            .round(1)

        expected = pd.DataFrame({'C': [1, 2, 3], 'E': [1, 0, -1], 'N': [-1.5, -1, -0.5]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_with_time():
        effect_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_timestamp() / 60 / 5 * np.pi / 2)

        dataset = Generator() \
            .add_effect(effect_function) \
            .set_time('2018-05-13 20:15', step='5m') \
            .generate(5)

        expected = pd.DataFrame({
            EventInterface.LABEL_EFFECT: [-1, 0, 1, 0, -1],
            EventInterface.LABEL_TIME: [1526235300, 1526235600, 1526235900, 1526236200, 1526236500],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_multiple():
        random.seed(2)
        effect_function: Callable[[History], float] = lambda history: \
            history.get_cause(0) + history.get_cause(1) + history.get_cause(2)

        dataset = Generator() \
            .add_effect(effect_function) \
            .add_noise_discrete() \
            .add_cause_discrete(0.3) \
            .add_cause_discrete(0.5) \
            .add_cause_discrete(0.9) \
            .generate()

        expected = pd.DataFrame({
            EventInterface.LABEL_CAUSE + '1': [1, 1, 0],
            EventInterface.LABEL_CAUSE + '2': [0, 1, 1],
            EventInterface.LABEL_CAUSE + '3': [0, 1, 1],
            EventInterface.LABEL_EFFECT: [1, 3, 2],
            EventInterface.LABEL_NOISE: [1, 1, 0],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_with_shadow():
        random.seed(2)

        dataset = Generator() \
            .add_effect(lambda history: 1) \
            .add_noise_discrete(shadow=True) \
            .add_noise_discrete() \
            .add_cause_discrete(shadow=False) \
            .add_cause_discrete(shadow=True) \
            .add_cause_continuous(shadow=True) \
            .add_cause_continuous() \
            .generate().round(0)

        expected = pd.DataFrame({
            EventInterface.LABEL_CAUSE + '1': [0, 0, 1],
            EventInterface.LABEL_CAUSE + '4': [7, 2, 5],
            EventInterface.LABEL_EFFECT: [1, 1, 1],
            EventInterface.LABEL_NOISE + '2': [1, 0, 0],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_multiple_effects():
        random.seed(2)

        dataset = Generator() \
            .add_cause_continuous() \
            .add_effect(lambda history: round(history.get_cause()) * 2) \
            .add_effect(lambda history: history.get_effect() + 1) \
            .generate().round(0)

        expected = pd.DataFrame({
            EventInterface.LABEL_CAUSE: [10, 9, 1],
            EventInterface.LABEL_EFFECT + '1': [20, 18, 2],
            EventInterface.LABEL_EFFECT + '2': [21, 19, 3],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_search():
        for seed in range(20):
            random.seed(seed)

            effect_function: Callable[[History], float] = lambda history: \
                history.get_cause(0) + history.get_cause(1) + history.get_cause(2)

            dataset = Generator() \
                .add_effect(lambda history: 1) \
                .add_noise_discrete() \
                .add_cause_discrete(0.3) \
                .add_cause_discrete(0.5) \
                .add_cause_discrete(0.9) \
                .generate()

            d = 3


if __name__ == '__main__':
    unittest.main()
