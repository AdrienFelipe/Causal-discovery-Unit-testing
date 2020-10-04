from __future__ import annotations

from pathlib import Path
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
from generator.relation.RelationPlot import RelationPlot
from tester.scripts.CausalInferenceExampleScript import CausalInferenceExampleScript
from tester.scripts.CausalInferenceScript import CausalInferenceScript
from tester.scripts.DowhyScript import DowhyScript
from tester.scripts.MeDILExampleScript import MeDILExampleScript
from tester.scripts.MeDILScript import MeDILScript
from tester.scripts.PyAgrumScript import PyAgrumScript
from tester.scripts.ScriptInterface import ScriptInterface
from utils import ProjectRoot


def score_it(scripts: List[ScriptInterface], datasets: List[DatasetInterface]):
    for dataset in datasets:
        # Make sure dataset file was generated.
        dataset.get_data(force_rebuild=True)
        for script in scripts:
            print(f'{dataset.name} ({dataset.items}) → {script.name}')
            relations = script.predict(dataset)

            generator = dataset.get_generator()
            generator.plot_relations(fig_size=(10, 10))
            RelationPlot.show(generator.get_events(include_shadow=False), relations, figsize=(10, 10))


datasets = [
    GeneExpressionDataset(100),
    #InstantActionDataset(1000),
    #LinearActionDataset(),
    #SensorsReadsDataset(),
    SinusoidalSeriesDataset(),
    DelayedEffectDataset(),
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
    PyAgrumScript(PyAgrumScript.LEARNER_GREEDY),
    PyAgrumScript(PyAgrumScript.LEARNER_LOCAL_SEARCH),
    DowhyScript(),
    #MeDILExampleScript(),
    #MeDILScript(),
    #CausalInferenceExampleScript(),
    #CausalInferenceScript(),

]

score_it(scripts, datasets)
