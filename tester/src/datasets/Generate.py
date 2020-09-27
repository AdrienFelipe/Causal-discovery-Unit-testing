import random
from typing import Callable

import numpy as np

from generator.Generator import Generator
from generator.History import History

random.seed(1)


def save_dataset(dataset: Generator, filename: str, items: int):
    dataset.generate(items).to_pickle(f"{filename}.pkl")


def instant_action(items: int, filename: str = 'instant-action'):
    event_function: Callable[[History], float] = lambda history: \
        1 if history.get_event(1) == 1 else 0

    dataset = Generator() \
        .add_discrete() \
        .add_discrete() \
        .add_function(event_function, round=0)

    save_dataset(dataset, filename, items)


def linear_action(items: int, filename: str = 'linear-action'):
    event_function: Callable[[History], float] = lambda history: \
        2 * history.get_event() + 10

    dataset = Generator() \
        .add_discrete() \
        .add_discrete() \
        .add_function(event_function)

    save_dataset(dataset, filename, items)


def logs_action(items: int, filename: str = 'logs-action'):
    event_function: Callable[[History], float] = lambda history: \
        1 if history.get_event() == 1 else None

    dataset = Generator(sequential=True) \
        .add_discrete() \
        .add_function(event_function) \
        .add_discrete()

    save_dataset(dataset, filename, items)


def sensors_reads(items: int, filename: str = 'sensors-reads'):
    event_function: Callable[[History], float] = lambda history: \
        2 * history.get_event(delay=1) + 3

    dataset = Generator(sequential=True) \
        .add_uniform(round=0) \
        .add_uniform(round=0) \
        .add_function(event_function, round=0)

    save_dataset(dataset, filename, items)


def sinusoidal_series(items: int, filename: str = 'sinusoidal-series'):
    event_function: Callable[[History], float] = lambda history: \
        np.sin(history.get_timestamp() / 60 / 5 * np.pi / 2)

    dataset = Generator() \
        .set_time('2010-01-02 20:10', step='5m') \
        .add_function(event_function, round=0)

    save_dataset(dataset, filename, items)


instant_action(10)
linear_action(20)
logs_action(30)
sensors_reads(30)
sinusoidal_series(100)
