from __future__ import annotations

from datasets.SalesDataset import SalesDataset
from datasets.unit.ChainedCausalityDataset import ChainedCausalityDataset
from datasets.unit.DirectCausalityDataset import DirectCausalityDataset
from datasets.unit.MultipleCausesCausalityDataset import MultipleCausesCausalityDataset
from datasets.unit.MultipleEffectsCausalityDataset import MultipleEffectsCausalityDataset
from discovery.scripts.PgmpyScript import PgmpyScript
from discovery.scripts.PyAgrumScript import PyAgrumScript

datasets2 = [
    DirectCausalityDataset.linear(100),
    DirectCausalityDataset.square_root(100),
    DirectCausalityDataset.power(100),
    DirectCausalityDataset.exponential(100),
    MultipleCausesCausalityDataset.linear(100),
    MultipleCausesCausalityDataset.power(100),
    MultipleEffectsCausalityDataset.linear(100),
    MultipleEffectsCausalityDataset.power(100),
    ChainedCausalityDataset.linear(100)
]

datasets = [
    SalesDataset.basic(100),
    SalesDataset.marketing_campaigns(100),
    MultipleCausesCausalityDataset.discrete(100),
    DirectCausalityDataset.discrete(100),
    MultipleEffectsCausalityDataset.discrete(100),
]

final = [
    SalesDataset.basic(100),
    SalesDataset.marketing_campaigns(100),
    MultipleCausesCausalityDataset.discrete(100),
    DirectCausalityDataset.discrete(100),
    MultipleEffectsCausalityDataset.discrete(100),
]

# http://www-desir.lip6.fr/~phw/aGrUM/docs/last/notebooks/11-structuralLearning.ipynb.html
# algorithm.useLocalSearchWithTabuList()
# algorithm.useGreedyHillClimbing()

scripts = [
    PgmpyScript.pc(),
    PgmpyScript.local_search(),
    #PgmpyScript.exhaustive_search(),
    PyAgrumScript(PyAgrumScript.LEARNER_GREEDY),
    # PyAgrumScript(PyAgrumScript.LEARNER_LOCAL_SEARCH),
    # DowhyScript(),
    # MeDILExampleScript(),
    # MeDILScript(),
    # CausalInferenceExampleScript(),
    # CausalInferenceScript(),
]
