from abc import abstractmethod
from typing import List

from datasets.DatasetInterface import DatasetInterface
from discovery.scripts.ScriptException import ScriptException
from generator.relation.Relation import Relation


class ScriptInterface:
    library = None
    algorithm = 'default'

    @abstractmethod
    def predict(self, data: DatasetInterface) -> List[Relation]:
        raise ScriptException('Script must implement a predict method')
