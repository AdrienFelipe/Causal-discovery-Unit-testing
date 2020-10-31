from __future__ import annotations

from typing import List

import pyAgrum as gum

from datasets.DatasetInterface import DatasetInterface
from discovery.scripts.ScriptInterface import ScriptInterface
from generator.relation.Relation import Relation


class PyAgrumScript(ScriptInterface):
    # Greedy Search by hill climbing.
    LEARNER_GES = 'GES'
    # Local search with tabu list.
    LEARNER_TS = 'TS'

    def __init__(self, algorithm: str = LEARNER_GES):
        super().__init__('pyAgrum', algorithm)

    def predict(self, dataset: DatasetInterface) -> List[Relation]:
        # Load from file as can't be used directly from a DataFrame.
        learner = gum.BNLearner(str(dataset.get_filepath()))

        # Greedy Search.
        if self.algorithm == self.LEARNER_GES:
            learner.useGreedyHillClimbing()

        # Tabu search.
        else:
            learner.useLocalSearchWithTabuList()

        return self.__build_relations(learner.learnBN())

    @staticmethod
    def GES() -> PyAgrumScript:
        return PyAgrumScript(PyAgrumScript.LEARNER_GES)

    @staticmethod
    def TS() -> PyAgrumScript:
        return PyAgrumScript(PyAgrumScript.LEARNER_TS)

    @staticmethod
    def __build_relations(bn_tree: gum.BayesNet) -> List[Relation]:
        relations = []
        for arc in bn_tree.arcs():
            relations.append(Relation(arc[0], arc[1]))

        return relations
