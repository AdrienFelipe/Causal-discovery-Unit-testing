from __future__ import annotations

from typing import List

from datasets.DatasetInterface import DatasetInterface
from datasets.InstantActionDataset import InstantActionDataset
from tester.scripts.CausalInferenceExampleScript import CausalInferenceExampleScript
from tester.scripts.CausalInferenceScript import CausalInferenceScript
from tester.scripts.DowhyScript import DowhyScript
from tester.scripts.MeDILExampleScript import MeDILExampleScript
from tester.scripts.MeDILScript import MeDILScript
from tester.scripts.ScriptInterface import ScriptInterface


def score_it(scripts: List[ScriptInterface], datasets: List[DatasetInterface]):
    for dataset in datasets:
        for script in scripts:
            print(f'{dataset.name} {script.name}')
            script.predict(dataset)


datasets = [InstantActionDataset()]
scripts = [
    #MeDILExampleScript(),
    #MeDILScript(),
    #CausalInferenceExampleScript(),
    #CausalInferenceScript(),
    DowhyScript()
]
score_it(scripts, datasets)