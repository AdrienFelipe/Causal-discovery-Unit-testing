from __future__ import annotations

from typing import Tuple

from datasets.DatasetInterface import DatasetInterface
from datasets.InstantActionDataset import InstantActionDataset
from tester.scripts.DowhyScript import DowhyScript
from tester.scripts.ScriptInterface import ScriptInterface


def score_it(scripts: Tuple[ScriptInterface], datasets: Tuple[DatasetInterface]):
    for dataset in datasets:
        data = dataset.read()
        for script in scripts:
            print(f'{dataset.name} {script.name}')


datasets = (InstantActionDataset(),)
scripts = (DowhyScript(),)
score_it(scripts, datasets)
