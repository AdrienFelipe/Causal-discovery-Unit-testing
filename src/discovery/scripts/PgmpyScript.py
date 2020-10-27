from __future__ import annotations

from typing import List

import pandas as pd
from pgmpy.base import PDAG
from pgmpy.estimators import PC, HillClimbSearch, ExhaustiveSearch

from datasets.DatasetInterface import DatasetInterface
from discovery.scripts.ScriptInterface import ScriptInterface
from generator.relation.Relation import Relation


class PgmpyScript(ScriptInterface):
    ESTIMATOR_PC = 'PC'
    ESTIMATOR_LOCAL_SEARCH = 'Local search'
    ESTIMATOR_EXHAUSTIVE_SEARCH = 'Exhaustive search'

    def __init__(self, algorithm: str):
        super().__init__('pgmpy', algorithm)

    def predict(self, dataset: DatasetInterface) -> List[Relation]:
        data = dataset.get_data()

        if self.algorithm == self.ESTIMATOR_PC:
            estimator = PC(data)
        elif self.algorithm == self.ESTIMATOR_EXHAUSTIVE_SEARCH:
            estimator = ExhaustiveSearch(data)
        else:
            estimator = HillClimbSearch(data)

        graph = estimator.estimate(show_progress=False)

        return PgmpyScript.__build_relations(graph, data)

    @staticmethod
    def __build_relations(graph: PDAG, data: pd.DataFrame) -> List[Relation]:
        relations = []
        for edge in graph.edges:
            source = data.columns.get_loc(edge[0])
            target = data.columns.get_loc(edge[1])
            relations.append(Relation(target, source))

        return relations

    @staticmethod
    def pc() -> PgmpyScript:
        return PgmpyScript(PgmpyScript.ESTIMATOR_PC)

    @staticmethod
    def local_search() -> PgmpyScript:
        return PgmpyScript(PgmpyScript.ESTIMATOR_LOCAL_SEARCH)

    @staticmethod
    def exhaustive_search() -> PgmpyScript:
        return PgmpyScript(PgmpyScript.ESTIMATOR_EXHAUSTIVE_SEARCH)
