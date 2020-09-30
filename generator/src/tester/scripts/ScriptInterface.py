from abc import abstractmethod

from datasets.DatasetInterface import DatasetInterface
from tester.scripts.ScriptException import ScriptException


class ScriptInterface:
    name = None

    @abstractmethod
    def predict(self, data: DatasetInterface):
        raise ScriptException('Script must implement its own predict method')
