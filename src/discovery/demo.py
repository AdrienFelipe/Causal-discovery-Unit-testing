import random
from typing import Callable

import numpy as np

from generator.Generator import Generator
from generator.History import History

values = ('Sunny', 'Neutral', 'Rainy')

random.seed(12)


def temperature_function(h):
    # \boldsymbol{30 - \frac{1}{12} (\text{Tiempo} + 0.5) (\text{Viento} +50)}
    return 30 - (values.index(h.e(1)) + 0.5) * (h.e(2)+50) / 12


generator = Generator() \
    .add_categorical(values, label='Weather') \
    .add_uniform(min=0, max=120, label='Wind', round=0) \
    .add_function(temperature_function, label='Temperature', round=1)

print(generator.generate())

# Time

event_function: Callable[[History], float] = lambda history: \
    np.sin(history.get_timestamp() / 60 / 5 * np.pi / 2)

generator = Generator() \
    .set_time('2010-01-02 20:10', step='5m') \
    .add_function(event_function, round=0)

print(generator.generate())


# Sequential

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


generator = Generator(sequential=True) \
    .add_categorical(('notice', 'warning', 'critical'), probability=0.2, weights=(0.7, 0.25, 0.05)) \
    .add_function(server_down, probability=0.9)

print(generator.generate(samples=10000))
