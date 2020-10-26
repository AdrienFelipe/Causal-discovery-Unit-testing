from __future__ import annotations

from random import random

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History


class SalesDataset(DatasetInterface):
    name = 'sales-history'
    samples = 100

    def get_generator(self) -> Generator:
        return self.basic()

    def get_causes(self) -> list:
        return ['T', 'E1', 'E2']

    def get_outcome(self) -> str:
        return 'E3'

    def basic(self) -> Generator:
        return Generator() \
            .set_time('2020-02-20', step='1d') \
            .add_constant(300, shadow=True) \
            .add_function(self.week_day, shadow=True) \
            .add_function(self.sales)

    def daily_noise(self) -> Generator:
        return Generator() \
            .set_time('2020-02-20', step='1d') \
            .add_uniform(250, 300, shadow=True) \
            .add_function(self.week_day, shadow=True) \
            .add_function(self.sales)

    def year_progressive(self) -> Generator:
        return Generator() \
            .set_time('2020-02-20', step='1d') \
            .add_uniform(250, 300, shadow=True) \
            .add_function(self.week_day, shadow=True) \
            .add_function(self.year_week, shadow=True) \
            .add_function(lambda h: h.get_event(1) * h.get_event(2) * h.get_event(3))

    def promo_pics(self) -> Generator:
        return Generator() \
            .set_time('2020-02-20', step='1d', label='Date') \
            .add_uniform(250, 300, shadow=True, label='Base\nsales') \
            .add_function(self.week_day, shadow=True, label='Week\nday') \
            .add_function(self.year_week, shadow=True, label='Year\nweek') \
            .add_discrete(0.05, label='Promo\nlaunch') \
            .add_function(self.promo, shadow=True, label='Promo\ndelay') \
            .add_function(lambda h: h.get_event(1) * h.get_event(2) * h.get_event(3) + h.get_event(5),
                          round=0, label='Sales')

    @staticmethod
    def week_day(history: History) -> float:
        day = history.get_datetime().weekday()
        ratios = [20, 20, 15, 5, 0, -20, -30]
        return 1 + ratios[day] / 100

    @staticmethod
    def sales(history: History) -> float:
        return history.get_event(1) * history.get_event(2)

    @staticmethod
    def year_week(history: History) -> float:
        week = history.get_datetime().isocalendar()[1]
        ratio = week - history.get_datetime(-1).isocalendar()[1]
        return 1 + ratio / 5

    @staticmethod
    def promo(history: History) -> float:
        value = 0
        if history.get_event(4, delay=1):
            value = random.normal(500, 100, 1)
        if history.get_event(4, delay=2):
            value = 400 + random.uniform(-100, 100)
        if history.get_event(4, delay=3):
            value = 200 + random.uniform(-50, 50)

        return value