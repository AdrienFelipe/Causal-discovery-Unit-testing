from random import gauss

from generator.events.EventInterface import EventInterface


class Gaussian(EventInterface):

    def __init__(self, mu: float, sigma: float, round: int = None, **kwargs):
        super().__init__(**kwargs)
        self.__mu = mu
        self.__sigma = sigma
        self.__round = round

    def generate(self) -> float:
        value = gauss(self.__mu, self.__sigma)
        if self.__round is not None:
            value = round(value, self.__round)
        return value
