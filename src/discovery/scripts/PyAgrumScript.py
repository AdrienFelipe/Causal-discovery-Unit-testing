from __future__ import annotations

from typing import List

import pyAgrum as gum

from datasets.DatasetInterface import DatasetInterface
from discovery.scripts.ScriptException import ScriptException
from discovery.scripts.ScriptInterface import ScriptInterface
from generator.relation.Relation import Relation


class PyAgrumScript(ScriptInterface):
    LEARNER_GREEDY = 'greedy'
    LEARNER_LOCAL_SEARCH = 'local search'

    def __init__(self, algorithm: str = LEARNER_GREEDY):
        super().__init__('pyAgrum', algorithm)

    def predict(self, dataset: DatasetInterface) -> List[Relation]:
        # Load from file as can't be used directly from a DataFrame.
        learner = gum.BNLearner(str(dataset.get_filepath()))

        if self.algorithm == self.LEARNER_GREEDY:
            return self.greedy_hill_climbing(dataset)

        if self.algorithm == self.LEARNER_LOCAL_SEARCH:
            return self.local_search_with_tabu_list(dataset)

        raise ScriptException('Undefined algorithm')

    def greedy_hill_climbing(self, dataset: DatasetInterface) -> List[Relation]:
        learner = gum.BNLearner(str(dataset.get_filepath()))
        learner.useGreedyHillClimbing()
        learner.setMaxIndegree(1)

        return self.__build_relations(learner.learnBN())

    def local_search_with_tabu_list(self, dataset: DatasetInterface) -> List[Relation]:
        learner = gum.BNLearner(str(dataset.get_filepath()))
        learner.useLocalSearchWithTabuList()

        return self.__build_relations(learner.learnBN())

    @staticmethod
    def __build_relations(bn_tree: gum.BayesNet) -> List[Relation]:
        relations = []
        for arc in bn_tree.arcs():
            relations.append(Relation(arc[0], arc[1]))

        return relations
