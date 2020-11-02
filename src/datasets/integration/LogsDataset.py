from __future__ import annotations

from typing import Callable

from datasets.DatasetInterface import DatasetInterface
from generator.Generator import Generator
from generator.History import History
from generator.events.Uniform import Uniform


class LogsDataset(DatasetInterface):
    name = 'logs-action'
    samples = 100

    def get_generator(self) -> Generator:
        return self.basic()

    def basic(self) -> Generator:
        event_function: Callable[[History], float] = lambda history: \
            1 if history.get_event() == 1 else None

        return Generator(sequential=True) \
            .add_discrete() \
            .add_function(event_function) \
            .add_discrete()

    def complex(self) -> Generator:
        return Generator(sequential=True) \
            .set_time(step='10s', precision='10s') \
            .add_function(
                lambda h: Uniform(70, 100, round=0).generate() if len(h.get_range(3, time_range='3m')) == 0 else None,
                probability=0.4, label='System\nhigh load'
            ) \
            .add_categorical(('notice', 'warning', 'critical'), probability=0.2, label='System\nfault') \
            .add_function(self.server_down, probability=0.9, label='Server\ndown')

    @staticmethod
    def server_down(h: History) -> float:
        try:
            load_log = h.get_range(position=1, time_range='1m', null_value=0)
            high_load = max(load_log) > 90 if len(load_log) != 0 else None

            error_log = h.get_range(position=2, time_range='2m')
            critical = any(error_log == 'critical')
            warning = any(error_log == 'warning')

            return 'server down' if critical or (warning and high_load) else None
        except Exception as err:
            print('error:', err)
