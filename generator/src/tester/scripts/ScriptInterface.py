import pandas as pd

from tester.scripts.ScriptException import ScriptException


class ScriptInterface:
    name = None

    def predict(self, data: pd.DataFrame):
        raise ScriptException('Script must implement its own predict method')
