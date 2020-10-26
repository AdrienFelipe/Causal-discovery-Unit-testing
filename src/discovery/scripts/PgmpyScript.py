from __future__ import annotations

from typing import List

import pandas as pd
from pgmpy.base import PDAG
from pgmpy.estimators import PC

from datasets.DatasetInterface import DatasetInterface
from discovery.scripts.ScriptInterface import ScriptInterface
from generator.relation.Relation import Relation


class PgmpyScript(ScriptInterface):
    name = 'pgmpy'

    DEFAULT_DELAY = 0

    def predict(self, dataset: DatasetInterface) -> List[Relation]:
        data = dataset.get_data()
        estimator = PC(data)
        graph = estimator.estimate(variant='stable', max_cond_vars=4, show_progress=False)

        return self.__build_relations(graph, data)

    def __build_relations(self, graph: PDAG, data: pd.DataFrame) -> List[Relation]:
        relations = []
        for edge in graph.edges:
            source = data.columns.get_loc(edge[0])
            target = data.columns.get_loc(edge[1])
            relations.append(Relation(target, source, self.DEFAULT_DELAY))

        return relations