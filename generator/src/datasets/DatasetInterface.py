from __future__ import annotations

from abc import abstractmethod
from pathlib import Path

import pandas as pd

from datasets.DatasetException import DatasetException
from generator.Generator import Generator
from utils import ProjectRoot


class DatasetInterface:
    name = None
    data = None
    items = 10

    @abstractmethod
    def build(self) -> Generator:
        raise DatasetException('Dataset must implement its own build method')

    @abstractmethod
    def get_causes(self) -> list:
        raise DatasetException('Dataset must implement its own get_causes method')

    @abstractmethod
    def get_outcome(self) -> str:
        raise DatasetException('Dataset must implement its own get_outcome method')

    def get_data(self, force_rebuild: bool = False) -> pd.DataFrame:
        if self.data is None:
            self.data = self.read() if self.get_filepath().is_file() and not force_rebuild else self.save(self.items)

        return self.data

    def read(self) -> pd.DataFrame:
        return pd.read_pickle(self.get_filepath())

    def save(self, items: int) -> pd.DataFrame:
        data = self.build().generate(items)
        data.to_pickle(str(self.get_filepath()))
        return data

    def get_filepath(self) -> Path:
        if self.name is None or self.name == '':
            raise DatasetException('Dataset name is undefined')

        return ProjectRoot.get() / f'res/datasets/{self.name}.pkl'
