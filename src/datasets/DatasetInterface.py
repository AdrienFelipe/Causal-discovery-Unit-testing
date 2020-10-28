from __future__ import annotations

import re
from abc import abstractmethod
from pathlib import Path

import pandas as pd

from datasets.DatasetException import DatasetException
from generator.Generator import Generator
from utils import ProjectRoot


class DatasetInterface:
    __data = None
    node_size = None

    def __init__(self, name: str, case: str = None, samples: int = 100):
        self.name = name
        self.case = case
        self.samples = samples

    @abstractmethod
    def get_generator(self) -> Generator:
        raise DatasetException('Dataset must implement its own build method')

    def get_data(self, force_rebuild: bool = False) -> pd.DataFrame:
        if self.__data is None:
            self.__data = self.read() if self.get_filepath().is_file() and not force_rebuild else self.save(
                self.samples)

        return self.__data

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.get_filepath())

    def save(self, items: int) -> pd.DataFrame:
        data = self.get_generator().generate(items)
        # Not saving to pickle as some learners need direct csv filepath as input.
        data.to_csv(str(self.get_filepath()), index=False)

        return data

    def get_label(self):
        return self.name + f' - {self.case}' if self.case is not None else ''

    def get_filepath(self) -> Path:
        if self.name is None or self.name == '':
            raise DatasetException('Dataset name is undefined')

        # Parse dataset label to a hyphen separated string.
        filename = re.findall('[A-z]+', self.get_label())
        filename = '-'.join([word.lower() for word in filename])

        return ProjectRoot.get() / f'res/datasets/{filename}-{self.samples}.csv'
