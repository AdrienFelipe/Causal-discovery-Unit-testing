from __future__ import annotations

from typing import Callable
from typing import Union

from History import History
from events.EventInterface import EventInterface


class Effect(EventInterface):

    def __init__(self, effect_function: Callable[[History], float], history: History, **kwargs):
        super().__init__(**kwargs)
        self.effect = effect_function
        self.__history = history

    def generate(self) -> Union[float, None]:
        try:
            return self.effect(self.__history)
        except:
            return None
