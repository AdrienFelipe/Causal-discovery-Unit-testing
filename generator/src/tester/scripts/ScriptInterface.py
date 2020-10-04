from abc import abstractmethod
from typing import List

from datasets.DatasetInterface import DatasetInterface
from generator.relation.Relation import Relation
from tester.scripts.ScriptException import ScriptException


class ScriptInterface:
    name = None

    @abstractmethod
    def predict(self, data: DatasetInterface) -> List[Relation]:
        raise ScriptException('Script must implement a predict method')
