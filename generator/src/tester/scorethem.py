from __future__ import annotations

from typing import List

from datasets.DatasetInterface import DatasetInterface
from datasets.InstantActionDataset import InstantActionDataset
from tester.scripts.CausalInferenceScript import CausalInferenceScript
from tester.scripts.DowhyScript import DowhyScript
from tester.scripts.ScriptInterface import ScriptInterface


def score_it(scripts: List[ScriptInterface], datasets: List[DatasetInterface]):
    for dataset in datasets:
        data = dataset.read()
        for script in scripts:
            print(f'{dataset.name} {script.name}')
            script.predict(data)


datasets = [InstantActionDataset()]
scripts = [CausalInferenceScript(), DowhyScript()]
score_it(scripts, datasets)
