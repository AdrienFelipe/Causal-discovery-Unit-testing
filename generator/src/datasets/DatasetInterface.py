from __future__ import annotations

from pathlib import Path

import pandas as pd

from datasets.DatasetException import DatasetException
from generator.Generator import Generator
from utils import ProjectRoot


class DatasetInterface:
    name = None

    def build(self) -> Generator:
        raise DatasetException('Dataset must implement its own build method')

    def read(self) -> pd.DataFrame:
        return pd.read_pickle(self.__get_filepath())

    def save(self, items: int) -> None:
        self.build().generate(items).to_pickle(self.__get_filepath())

    def __get_filepath(self) -> str:
        if self.name is None or self.name == '':
            raise DatasetException('Dataset name is undefined')

        return str(ProjectRoot.get() / f'res/datasets/{self.name}.pkl')
