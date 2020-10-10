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
from discovery.EvaluateLearner import EvaluateLearner
from discovery.scripts.CausalInferenceScript import CausalInferenceScript
from discovery.scripts.DowhyScript import DowhyScript
from discovery.scripts.MeDILScript import MeDILScript
from discovery.scripts.PgmpyScript import PgmpyScript
from discovery.scripts.PyAgrumScript import PyAgrumScript
from discovery.scripts.ScriptInterface import ScriptInterface
from utils import ProjectRoot
import datetime


datasets = [
    GeneExpressionDataset(1000),
    InstantActionDataset(100),
    InstantActionDataset(500),
    InstantActionDataset(1000),
    #LinearActionDataset(500),
    ##SensorsReadsDataset(500),
    #SinusoidalSeriesDataset(500),
    #DelayedEffectDataset(500),
    ##LogsDataset(500),
    #MultipleCausesDataset(500),
    #MultipleEffectsDataset(500),
    #SalesDataset(10000),
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

EvaluateLearner.compare_algorithms(scripts, datasets)
