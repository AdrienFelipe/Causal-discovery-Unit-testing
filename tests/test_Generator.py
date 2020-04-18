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
            .add_effect(effect_function) \
            .add_noise_discrete() \
            .generate()

        expected = pd.DataFrame({'C1': [0, 1, 0], 'E2': [0, 1, 0], 'N3': [1, 0, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_random_samples():
        random.seed(10)
        effect_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(2)

        dataset = Generator() \
            .add_noise_continuous() \
            .add_cause_continuous() \
            .add_effect(effect_function) \
            .generate().astype(int)

        expected = pd.DataFrame({'C2': [4, 2, 8], 'E3': [8, 4, 16], 'N1': [5, 5, 8]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_discrete_ordered():
        random.seed(14)
        effect_function: Callable[[History], float] = lambda history: \
            1 if history.get_event(2, delay=1) == 1 else None

        dataset = Generator(ordered=True) \
            .add_noise_discrete() \
            .add_cause_discrete() \
            .add_effect(effect_function) \
            .generate(4)

        expected = pd.DataFrame({'C2': [0, 1, 0, 0], 'E3': [0, 0, 1, 0], 'N1': [1, 0, 0, 0]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_ordered():
        random.seed(14)
        effect_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(1, delay=1) + 3

        dataset = Generator(ordered=True) \
            .add_cause_continuous() \
            .add_effect(effect_function) \
            .add_noise_continuous() \
            .generate(4) \
            .astype(int)

        expected = pd.DataFrame({'C1': [0, 9, 0, 0], 'E2': [0, 0, 21, 0], 'N3': [7, 0, 0, 2]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_pattern_search():
        effect_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_event() * np.pi / 2)

        dataset = Generator() \
            .add_cause_linear() \
            .add_effect(effect_function) \
            .add_noise_linear(start=-2, step=0.5) \
            .generate() \
            .round(1)

        expected = pd.DataFrame({'C1': [1, 2, 3], 'E2': [1, 0, -1], 'N3': [-1.5, -1, -0.5]})
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
        random.seed(0)
        effect_function: Callable[[History], float] = lambda history: \
            history.get_event(1) + history.get_event(2) + history.get_event(3)

        dataset = Generator() \
            .add_cause_discrete(0.3) \
            .add_cause_discrete(0.5) \
            .add_cause_discrete(0.9) \
            .add_effect(effect_function) \
            .add_noise_discrete() \
            .generate()

        expected = pd.DataFrame({
            EventInterface.LABEL_CAUSE + '1': [1, 0, 0],
            EventInterface.LABEL_CAUSE + '2': [1, 0, 1],
            EventInterface.LABEL_CAUSE + '3': [1, 1, 1],
            EventInterface.LABEL_EFFECT + '4': [3, 1, 2],
            EventInterface.LABEL_NOISE + '5': [0, 0, 0],
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
            EventInterface.LABEL_CAUSE + '4': [0, 0, 1],
            EventInterface.LABEL_CAUSE + '7': [7, 2, 5],
            EventInterface.LABEL_EFFECT + '1': [1, 1, 1],
            EventInterface.LABEL_NOISE + '3': [1, 0, 0],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_multiple_effects():
        random.seed(2)

        dataset = Generator() \
            .add_cause_continuous() \
            .add_effect(lambda history: round(history.get_event()) * 2) \
            .add_effect(lambda history: history.get_event(2) + 1) \
            .generate().round(0)

        expected = pd.DataFrame({
            EventInterface.LABEL_CAUSE + '1': [10, 9, 1],
            EventInterface.LABEL_EFFECT + '2': [20, 18, 2],
            EventInterface.LABEL_EFFECT + '3': [21, 19, 3],
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
            .add_effect(effect1) \
            .add_effect(effect2) \
            .add_effect(effect3) \
            .generate(20)

    @staticmethod
    def test_search():
        for seed in range(50):
            random.seed(seed)

            effect_function: Callable[[History], float] = lambda history: \
                history.get_event(1) + history.get_event(2) + history.get_event(3)

            dataset = Generator() \
                .add_cause_discrete(0.3) \
                .add_cause_discrete(0.5) \
                .add_cause_discrete(0.9) \
                .add_effect(effect_function) \
                .add_noise_discrete() \
                .generate()

            d = 3


if __name__ == '__main__':
    unittest.main()
