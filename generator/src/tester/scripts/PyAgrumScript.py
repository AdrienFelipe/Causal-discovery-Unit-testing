from __future__ import annotations

from typing import List

import pyAgrum as gum

from datasets.DatasetInterface import DatasetInterface
from generator.relation.Relation import Relation
from tester.scripts.ScriptInterface import ScriptInterface
from utils import ProjectRoot


class PyAgrumScript(ScriptInterface):
    DEFAULT_DELAY = 0
    name = 'pyAgrum'

    def predict(self, dataset: DatasetInterface) -> List[Relation]:
        return self.greedy_hill_climbing(dataset)

    def greedy_hill_climbing(self, dataset: DatasetInterface) -> List[Relation]:
        dataset.get_data().to_csv('crapfuck.csv')
        learner = gum.BNLearner('crapfuck.csv')
        learner.useGreedyHillClimbing()

        return self.__build_relations(learner.learnBN())

    def __build_relations(self, bn_tree) -> List[Relation]:
        relations = []
        for arc in bn_tree.arcs():
            relations.append(Relation(arc[0], arc[1], self.DEFAULT_DELAY))

        return relations

    def get_filepath(self, file: str) -> str:
        return str(ProjectRoot.get() / f'res/pyagrum/{file}')
