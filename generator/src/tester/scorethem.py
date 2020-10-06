from __future__ import annotations

from pathlib import Path
from typing import List
from tabulate import tabulate

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
from generator.events.EventInterface import EventInterface
from generator.relation.Relation import Relation
from generator.relation.RelationPlot import RelationPlot
from tester.EvaluateLearner import EvaluateLearner
from tester.scripts.CausalInferenceExampleScript import CausalInferenceExampleScript
from tester.scripts.CausalInferenceScript import CausalInferenceScript
from tester.scripts.DowhyScript import DowhyScript
from tester.scripts.MeDILExampleScript import MeDILExampleScript
from tester.scripts.MeDILScript import MeDILScript
from tester.scripts.PgmpyScript import PgmpyScript
from tester.scripts.PyAgrumScript import PyAgrumScript
from tester.scripts.ScriptInterface import ScriptInterface
from utils import ProjectRoot
import datetime


def score_it(scripts: List[ScriptInterface], datasets: List[DatasetInterface]):
    results = {}
    for dataset in datasets:
        # Make sure dataset file was generated.
        dataset.get_data(force_rebuild=True)
        for script in scripts:
            print(f'{dataset.name} ({dataset.items}) → {script.name}')
            # Mesure script execution time.
            time = datetime.datetime.now()
            learned_relations = script.predict(dataset)
            time = (datetime.datetime.now() - time).total_seconds()

            generator = dataset.get_generator()
            #generator.plot_relations(fig_size=(10, 10))
            #RelationPlot.show(generator.get_events(include_shadow=False), learned_relations, figsize=(10, 10))

            real_relations = generator.build_relations()

            real_relations = relations_to_label(real_relations, generator.get_events())
            learned_relations = relations_to_label(learned_relations, generator.get_events(include_shadow=False))

            missing, added, inverted = EvaluateLearner.compare_relations(real_relations, learned_relations)
            found = 1 - (len(missing) + len(inverted)) / len(real_relations)

            # Build results to be printed
            results.setdefault('dataset', []).append(dataset.name)
            results.setdefault('items', []).append(dataset.items)
            results.setdefault('library', []).append(script.name)
            results.setdefault('algorithm', []).append(script.algorithm)
            results.setdefault('found', []).append(f'{int(found * 100)}%')
            results.setdefault('erroneous', []).append(len(added))
            results.setdefault('inverted', []).append(len(inverted))
            results.setdefault('missing', []).append(len(missing))
            results.setdefault('time', []).append(f'{int(time * 1000)}ms')

    print()
    print(tabulate(results, headers='keys'))


def relations_to_label(relations: List[Relation], events: List[EventInterface]) -> List[Relation]:
    labeled_relations = []
    for relation in relations:
        labeled_relations.append(Relation(events[relation.source].label, events[relation.target].label, relation.delay))

    return labeled_relations




datasets = [
    #GeneExpressionDataset(1000),
    #InstantActionDataset(1000),
    #LinearActionDataset(500),
    ##SensorsReadsDataset(500),
    #SinusoidalSeriesDataset(500),
    #DelayedEffectDataset(500),
    ##LogsDataset(500),
    #MultipleCausesDataset(500),
    #MultipleEffectsDataset(500),
    SalesDataset(10000),
    #ShadowCauseDataset(500),
]

# http://www-desir.lip6.fr/~phw/aGrUM/docs/last/notebooks/11-structuralLearning.ipynb.html
# algorithm.useLocalSearchWithTabuList()
# algorithm.useGreedyHillClimbing()

scripts = [
    PgmpyScript(),
    PyAgrumScript(PyAgrumScript.LEARNER_GREEDY),
    PyAgrumScript(PyAgrumScript.LEARNER_LOCAL_SEARCH),
    #DowhyScript(),
    #MeDILExampleScript(),
    #MeDILScript(),
    #CausalInferenceExampleScript(),
    #CausalInferenceScript(),

]

score_it(scripts, datasets)
