from __future__ import annotations

import pandas as pd

from datasets.DatasetException import DatasetException
from generator.Generator import Generator


class DatasetInterface:
    name = None
    generator = None

    def build(self) -> Generator:
        raise DatasetException('Dataset cannot be built from the interface')

    def read(self) -> pd.DataFrame:
        return pd.read_pickle(self.__get_filepath())

    def save(self, items: int):
        if self.generator is None:
            raise DatasetException('Dataset generator is undefined')

        self.generator.generate(items).to_pickle(self.__get_filepath())

    def __get_filepath(self):
        if self.name is None or self.name == '':
            raise DatasetException('Dataset name is undefined')

        return f'res/datasets/{self.name}.pkl'
