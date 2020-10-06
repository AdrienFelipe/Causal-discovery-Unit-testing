from __future__ import annotations

from typing import List

import pyAgrum as gum

from datasets.DatasetInterface import DatasetInterface
from generator.relation.Relation import Relation
from discovery.scripts.ScriptException import ScriptException
from discovery.scripts.ScriptInterface import ScriptInterface


class PyAgrumScript(ScriptInterface):
    name = 'pyAgrum'

    LEARNER_GREEDY = 'greedy'
    LEARNER_LOCAL_SEARCH = 'local search'

    DEFAULT_DELAY = 0
    DEFAULT_ALGORITHM = LEARNER_GREEDY

    def __init__(self, algorithm: str = DEFAULT_ALGORITHM):
        self.algorithm = algorithm

    def predict(self, dataset: DatasetInterface) -> List[Relation]:
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

    def __build_relations(self, bn_tree: gum.BayesNet) -> List[Relation]:
        relations = []
        for arc in bn_tree.arcs():
            relations.append(Relation(arc[0], arc[1], self.DEFAULT_DELAY))

        return relations
