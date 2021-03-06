from __future__ import annotations

from random import random

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History
from generator.events.Uniform import Uniform


class SalesDataset(DatasetInterface):
    name = 'Sales'

    def __init__(self, case: str, generator: Generator, *args, **kwargs):
        super().__init__(self.name, case, *args, **kwargs)
        self.generator = generator

    def get_generator(self) -> Generator:
        return self.generator

    @staticmethod
    def basic(*args, **kwargs) -> SalesDataset:
        case = 'Basic'
        generator = Generator() \
            .set_time('2020-02-20', step='1d') \
            .add_constant(300, shadow=True) \
            .add_function(SalesDataset.week_day, shadow=True) \
            .add_function(SalesDataset.sales, label='Sales')

        return SalesDataset(case, generator, *args, **kwargs)

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

    @staticmethod
    def marketing_campaigns(*args, **kwargs) -> SalesDataset:
        case = 'Marketing campaigns'
        generator = Generator() \
            .set_time('2020-02-20', step='1d', label='Date') \
            .add_uniform(250, 300, shadow=True, label='Base\nsales', data_type=int) \
            .add_function(SalesDataset.week_day, shadow=True, label='Week\nday') \
            .add_function(SalesDataset.year_week, shadow=True, label='Year\nweek') \
            .add_categorical((None, 'Shipping', 'Discount'), weights=(0.85, 0.10, 0.05), label='Promo\nlaunch') \
            .add_function(SalesDataset.promo_delay, shadow=True, label='Promo\ndelay', data_type=int) \
            .add_uniform(min=1000, max=5000) \
            .add_function(lambda h: h.get_event(1) * h.get_event(2) * h.get_event(3) + h.get_event(5), label='Sales', data_type=int)

        return SalesDataset(case, generator, *args, **kwargs)

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
    def promo_delay(history: History) -> float:
        value = 0
        if history.get_event(4):
            value = Uniform(40, 80).generate()
        elif history.get_event(4, delay=1):
            value = Uniform(30, 50).generate()
        elif history.get_event(4, delay=2):
            value = Uniform(0, 20).generate()

        return value
