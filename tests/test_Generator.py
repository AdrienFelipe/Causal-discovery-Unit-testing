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
            1 if history.get_event(1) == 1 else 0

        dataset = Generator() \
            .add_cause_discrete() \
            .add_function(effect_function) \
            .add_noise_discrete() \
            .generate()

        expected = pd.DataFrame({'E1': [1, 1, 0], 'E2': [1, 1, 0], 'E3': [0, 0, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_random_samples():
        random.seed(10)
        effect_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(2)

        dataset = Generator() \
            .add_noise_continuous() \
            .add_cause_continuous() \
            .add_function(effect_function) \
            .generate().astype(int)

        expected = pd.DataFrame({'E1': [4, 6, 9], 'E2': [2, 5, 0], 'E3': [4, 10, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_discrete_ordered():
        random.seed(10)
        effect_function: Callable[[History], float] = lambda history: \
            1 if history.get_event(2, delay=1) == 1 else None

        dataset = Generator(sequential=True) \
            .add_noise_discrete(weight=0.5) \
            .add_cause_discrete(weight=0.5) \
            .add_function(effect_function) \
            .generate(4)

        expected = pd.DataFrame({
            'E1': [0, None, 1, None],
            'E2': [None, 0, None, 1],
            'E3': [None, None, None, None],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_ordered():
        random.seed(0)
        effect_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(1, delay=1) + 3

        dataset = Generator(sequential=True) \
            .add_cause_continuous(probability=0.5, round=0) \
            .add_function(effect_function) \
            .add_noise_continuous(5, 9, probability=0.5, round=0) \
            .generate(5)

        expected = pd.DataFrame({
            'E1': [None, 5, None, 7, None],
            'E2': [None, None, 13, None, 17],
            'E3': [6, None, None, None, None],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_pattern_search():
        effect_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_event() * np.pi / 2)

        dataset = Generator() \
            .add_cause_linear() \
            .add_function(effect_function) \
            .add_noise_linear(start=-2, step=0.5) \
            .generate() \
            .round(1)

        expected = pd.DataFrame({'E1': [1, 2, 3], 'E2': [1, 0, -1], 'E3': [-1.5, -1, -0.5]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_with_time():
        effect_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_timestamp() / 60 / 5 * np.pi / 2)

        dataset = Generator() \
            .add_function(effect_function) \
            .set_time('2018-05-13 20:15', step='5m') \
            .generate(5)

        expected = pd.DataFrame({
            EventInterface.LABEL_EFFECT: [-1, 0, 1, 0, -1],
            EventInterface.LABEL_TIME: [1526235300, 1526235600, 1526235900, 1526236200, 1526236500],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_multiple():
        random.seed(0)
        effect_function: Callable[[History], float] = lambda history: \
            history.get_event(1) + history.get_event(2) + history.get_event(3)

        dataset = Generator() \
            .add_cause_discrete(0.3) \
            .add_cause_discrete(0.5) \
            .add_cause_discrete(0.9) \
            .add_function(effect_function) \
            .add_noise_discrete() \
            .generate()

        expected = pd.DataFrame({
            EventInterface.LABEL_CAUSE + '1': [1, 1, 1],
            EventInterface.LABEL_CAUSE + '2': [0, 0, 1],
            EventInterface.LABEL_CAUSE + '3': [1, 1, 1],
            EventInterface.LABEL_EFFECT + '4': [2, 2, 3],
            EventInterface.LABEL_NOISE + '5': [0, 1, 0],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_with_shadow():
        random.seed(2)

        dataset = Generator() \
            .add_function(lambda history: 1) \
            .add_noise_discrete(shadow=True) \
            .add_noise_discrete() \
            .add_cause_discrete(shadow=False) \
            .add_cause_discrete(shadow=True) \
            .add_cause_continuous(shadow=True) \
            .add_cause_continuous() \
            .generate().round(0)

        expected = pd.DataFrame({
            EventInterface.LABEL_EFFECT + '1': [1, 1, 1],
            EventInterface.LABEL_NOISE + '3': [1, 1, 0],
            EventInterface.LABEL_CAUSE + '4': [1, 0, 1],
            EventInterface.LABEL_CAUSE + '7': [4, 9, 7],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_multiple_effects():
        random.seed(2)

        dataset = Generator() \
            .add_cause_continuous() \
            .add_function(lambda history: round(history.get_event()) * 2) \
            .add_function(lambda history: history.get_event(2) + 1) \
            .generate().round(0)

        expected = pd.DataFrame({
            EventInterface.LABEL_CAUSE + '1': [9, 7, 6],
            EventInterface.LABEL_EFFECT + '2': [18, 14, 12],
            EventInterface.LABEL_EFFECT + '3': [19, 15, 13],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    def test_sales_dataset(self):
        random.seed(3)

        def effect1(history: History) -> float:
            day = history.get_datetime().weekday()
            ratios = [20, 20, 15, 10, 0, -30, -50]
            return history.get_event(1) * (1 + ratios[day] / 100)

        def effect2(history: History) -> float:
            week = history.get_datetime().isocalendar()[1]
            ratio = week - history.get_datetime(-1).isocalendar()[1]
            return history.get_event(1) * (1 + ratio / 20)

        def effect3(history: History) -> float:
            value = history.get_event(2)
            if history.get_event(2, delay=1):
                value *= 1.5
            elif history.get_event(2, delay=2):
                value *= 3
            elif history.get_event(2, delay=3):
                value *= 1.2
            return value

        dataset = Generator() \
            .set_time('2020-02-20', step='1d') \
            .add_cause_continuous(250, 300) \
            .add_function(effect1) \
            .add_function(effect2) \
            .add_function(effect3) \
            .generate(20)

    @staticmethod
    def test_search():
        for seed in range(50):
            random.seed(seed)

            effect_function: Callable[[History], float] = lambda history: \
                1 if history.get_event(2, delay=1) == 1 else None

            dataset = Generator(sequential=True) \
                .add_noise_discrete(weight=0.5) \
                .add_cause_discrete(weight=0.5) \
                .add_function(effect_function) \
                .generate(4)

            d = 3


if __name__ == '__main__':
    unittest.main()
