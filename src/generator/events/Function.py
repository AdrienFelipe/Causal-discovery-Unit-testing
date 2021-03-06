from __future__ import annotations

from typing import Callable
from typing import Union

from generator.History import History
from generator.events.EventInterface import EventInterface


class Function(EventInterface):

    def __init__(self, effect_function: Callable[[History], float], history: History, round=None, **kwargs):
        super().__init__(**kwargs)
        self.function = effect_function
        self.__history = history
        self.__round = round

    def generate(self) -> Union[float, None]:
        try:
            result = self.function(self.__history)
            if self.__round is not None:
                result = round(result, self.__round)
            return result
        except:
            return None
