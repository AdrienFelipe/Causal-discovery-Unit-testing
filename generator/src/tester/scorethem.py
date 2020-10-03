from __future__ import annotations

from typing import List

from datasets.DatasetInterface import DatasetInterface
from datasets.DelayedEffectDataset import DelayedEffectDataset
from datasets.GeneExpressionDataset import GeneExpressionDataset
from datasets.InstantActionDataset import InstantActionDataset
from datasets.LinearActionDataset import LinearActionDataset
from datasets.LogsDataset import LogsDataset
from datasets.MultipleCausesDataset import MultipleCausesDataset
from datasets.MultipleEffectsDataset import MultipleEffectsDataset
from datasets.SalesDataset import SalesDataset
from datasets.SensorsReadsDataset import SensorsReadsDataset
from datasets.ShadowCauseDataset import ShadowCauseDataset
from datasets.SinusoidalSeriesDataset import SinusoidalSeriesDataset
from tester.scripts.CausalInferenceExampleScript import CausalInferenceExampleScript
from tester.scripts.CausalInferenceScript import CausalInferenceScript
from tester.scripts.DowhyScript import DowhyScript
from tester.scripts.MeDILExampleScript import MeDILExampleScript
from tester.scripts.MeDILScript import MeDILScript
from tester.scripts.ScriptInterface import ScriptInterface


def score_it(scripts: List[ScriptInterface], datasets: List[DatasetInterface]):
    for dataset in datasets:
        for script in scripts:
            print(f'{dataset.name} ({dataset.items}) → {script.name}')
            script.predict(dataset)


datasets = [
    InstantActionDataset(),
    LinearActionDataset(),
    #SensorsReadsDataset(),
    SinusoidalSeriesDataset(),
    DelayedEffectDataset(),
    GeneExpressionDataset(),
    #LogsDataset(),
    MultipleCausesDataset(),
    MultipleEffectsDataset(),
    SalesDataset(),
    ShadowCauseDataset(),
]

# http://www-desir.lip6.fr/~phw/aGrUM/docs/last/notebooks/11-structuralLearning.ipynb.html
# learner.useLocalSearchWithTabuList()
# learner.useGreedyHillClimbing()

scripts = [
    DowhyScript(),
    #MeDILExampleScript(),
    #MeDILScript(),
    #CausalInferenceExampleScript(),
    #CausalInferenceScript(),

]

score_it(scripts, datasets)
