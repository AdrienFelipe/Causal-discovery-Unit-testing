import random
import unittest
from typing import Callable

import numpy as np
import pandas as pd

from generator.Generator import Generator
from generator.History import History
from generator.events.EventInterface import EventInterface


class GeneratorTest(unittest.TestCase):

    @staticmethod
    def test_discrete_instant_action():
        random.seed(1)
        effect_function: Callable[[History], float] = lambda history: \
            1 if history.get_event(1) == 1 else 0

        dataset = Generator() \
            .add_discrete() \
            .add_function(effect_function) \
            .add_discrete() \
            .generate()

        expected = pd.DataFrame({'E1': [1, 0, 0], 'E2': [1, 0, 0], 'E3': [0, 0, 1]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_random_samples():
        random.seed(10)
        effect_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(2)

        dataset = Generator() \
            .add_uniform() \
            .add_uniform() \
            .add_function(effect_function) \
            .generate().astype(int)

        expected = pd.DataFrame({'E1': [5, 5, 8], 'E2': [8, 2, 3], 'E3': [16, 4, 7]})
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_discrete_ordered():
        random.seed(10)
        effect_function: Callable[[History], float] = lambda history: \
            1 if history.get_event(2) == 1 else None

        dataset = Generator(sequential=True) \
            .add_discrete(weight=0.5) \
            .add_discrete(weight=0.5) \
            .add_function(effect_function) \
            .generate(4)

        expected = pd.DataFrame({
            'E1': [1, None, None, 0],
            'E2': [None, 1, None, None],
            'E3': [None, None, 1, None],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_continuous_ordered():
        random.seed(0)
        effect_function: Callable[[History], float] = lambda history: \
            2 * history.get_event(1, delay=1) + 3

        dataset = Generator(sequential=True) \
            .add_uniform(probability=0.5, round=0) \
            .add_function(effect_function) \
            .add_uniform(5, 9, probability=0.5, round=0) \
            .generate(5)

        expected = pd.DataFrame({
            'E1': [None, 6, 9, None, None],
            'E2': [None, None, None, 15, None],
            'E3': [8, None, None, None, 8],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_pattern_search():
        effect_function: Callable[[History], float] = lambda history: \
            np.sin(history.get_event() * np.pi / 2)

        dataset = Generator() \
            .add_linear() \
            .add_function(effect_function) \
            .add_linear(start=-2, step=0.5) \
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
            EventInterface.LABEL_EVENT + '1': [-1, 0, 1, 0, -1],
            EventInterface.LABEL_TIME: [1526235300, 1526235600, 1526235900, 1526236200, 1526236500],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_multiple():
        random.seed(0)
        effect_function: Callable[[History], float] = lambda history: \
            history.get_event(1) + history.get_event(2) + history.get_event(3)

        dataset = Generator() \
            .add_discrete(0.3) \
            .add_discrete(0.5) \
            .add_discrete(0.9) \
            .add_function(effect_function) \
            .add_discrete() \
            .generate()

        expected = pd.DataFrame({
            EventInterface.LABEL_EVENT + '1': [0, 0, 1],
            EventInterface.LABEL_EVENT + '2': [1, 1, 0],
            EventInterface.LABEL_EVENT + '3': [1, 1, 1],
            EventInterface.LABEL_EVENT + '4': [2, 2, 2],
            EventInterface.LABEL_EVENT + '5': [1, 1, 1],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_with_shadow():
        random.seed(2)

        dataset = Generator() \
            .add_function(lambda history: 1) \
            .add_discrete(shadow=True) \
            .add_discrete() \
            .add_discrete(shadow=False) \
            .add_discrete(shadow=True) \
            .add_uniform(shadow=True) \
            .add_uniform() \
            .generate().round(0)

        expected = pd.DataFrame({
            EventInterface.LABEL_EVENT + '1': [1, 1, 1],
            EventInterface.LABEL_EVENT + '3': [1, 0, 1],
            EventInterface.LABEL_EVENT + '4': [0, 0, 0],
            EventInterface.LABEL_EVENT + '7': [4, 6, 8],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_multiple_effects():
        random.seed(2)

        dataset = Generator() \
            .add_uniform() \
            .add_function(lambda history: round(history.get_event()) * 2) \
            .add_function(lambda history: history.get_event(2) + 1) \
            .generate().round(0)

        expected = pd.DataFrame({
            EventInterface.LABEL_EVENT + '1': [1, 3, 4],
            EventInterface.LABEL_EVENT + '2': [2, 6, 8],
            EventInterface.LABEL_EVENT + '3': [3, 7, 9],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_range_from_next_event():
        random.seed(25)

        dataset = Generator() \
            .set_time('2018-05-13 20:15', step='5m') \
            .add_categorical(('First', 'Second', 'Third')) \
            .add_function(lambda history: 'Third' in history.get_range(time_range='10m')) \
            .generate()

        expected = pd.DataFrame({
            EventInterface.LABEL_EVENT + '1': ['Third', 'First', 'Second'],
            EventInterface.LABEL_EVENT + '2': [1, 1, 0],
            EventInterface.LABEL_TIME: [1526235300, 1526235600, 1526235900],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_sales_dataset():
        random.seed(30)

        # Impact depending on the week day.
        def effect1(history: History) -> float:
            day = history.get_datetime().weekday()
            # [Sun, Mon, Tue, Wed, Thu, Fri, Sat]
            ratios = [20, 20, 15, 10, 0, -30, -50]
            return history.get_event(1) * (1 + ratios[day] / 100)

        # Impact depending on the week number.
        def effect2(history: History) -> float:
            week = history.get_datetime().isocalendar()[1]
            ratio = week / 52
            return history.get_event(1) * (1 + ratio / 20)

        # Impact depending on history samples.
        def effect3(history: History) -> float:
            value = history.get_event(2)
            if not history.get_event(2, delay=1):
                value *= 1.5
            elif not history.get_event(2, delay=2):
                value *= 3
            elif not history.get_event(2, delay=3):
                value *= 6
            return value

        # Thursday 20/02/2020
        dataset = Generator() \
            .set_time('2020-02-20', step='1d') \
            .add_uniform(250, 300) \
            .add_function(effect1) \
            .add_function(effect2) \
            .add_function(effect3) \
            .generate().round(0)

        expected = pd.DataFrame({
            EventInterface.LABEL_EVENT + '1': [252, 299, 258],
            EventInterface.LABEL_EVENT + '2': [277, 299, 181],
            EventInterface.LABEL_EVENT + '3': [253, 302, 260],
            EventInterface.LABEL_EVENT + '4': [415, 898, 1084],
            EventInterface.LABEL_TIME: [1582153200, 1582239600, 1582326000],
        })
        pd.testing.assert_frame_equal(expected, dataset, check_dtype=False)

    @staticmethod
    def test_search():
        for seed in range(50):
            random.seed(seed)

            event_function: Callable[[History], float] = lambda history: \
                history.get_event(1) and history.get_event(2)

            dataset = Generator() \
                .add_discrete() \
                .add_discrete() \
                .add_function(event_function).generate()

            d = 3

    def test_some(self):
        random.seed(1)

        event_function: Callable[[History], float] = lambda history: \
            1 if history.get_event() == 1 else 0

        dataset = Generator() \
            .add_discrete() \
            .add_discrete() \
            .add_function(event_function)

        # generator.plot_relations()


if __name__ == '__main__':
    unittest.main()
