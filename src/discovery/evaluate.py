from __future__ import annotations

from datasets.unit.DirectCausalityDataset import DirectCausalityDataset
from discovery.EvaluateLearner import EvaluateLearner
from discovery.scripts.PgmpyScript import PgmpyScript
from discovery.scripts.PyAgrumScript import PyAgrumScript

datasets = [
    DirectCausalityDataset.linear(100),
    DirectCausalityDataset.square_root(100),
    DirectCausalityDataset.power(100),
    DirectCausalityDataset.exponential(100),
]

# http://www-desir.lip6.fr/~phw/aGrUM/docs/last/notebooks/11-structuralLearning.ipynb.html
# algorithm.useLocalSearchWithTabuList()
# algorithm.useGreedyHillClimbing()

scripts = [
    PgmpyScript(),
    PyAgrumScript(PyAgrumScript.LEARNER_GREEDY),
    PyAgrumScript(PyAgrumScript.LEARNER_LOCAL_SEARCH),
    # DowhyScript(),
    # MeDILExampleScript(),
    # MeDILScript(),
    # CausalInferenceExampleScript(),
    # CausalInferenceScript(),

]

exit(EvaluateLearner.run(scripts, datasets, force_rebuild=True))
