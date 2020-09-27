from typing import List

import pandas as pd

from scripts.DowhyScript import DowhyScript
from scripts.ScriptInterface import ScriptInterface

datasets = ('instant-action', 'linear-action', 'logs-action', 'sensors-reads')


def score_it(scripts: List[ScriptInterface]):
    for dataset_name in datasets:
        dataset = pd.read_pickle(f'datasets/{dataset_name}.pkl')
        for script in scripts:
            print(script.name)


scripts = (DowhyScript,)
score_it(scripts)
