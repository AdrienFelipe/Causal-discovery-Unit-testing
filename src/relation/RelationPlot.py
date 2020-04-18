from typing import List

import matplotlib.pyplot as plt
import networkx as nx

from relation.Relation import Relation
from events.EventInterface import EventInterface


class RelationPlot:

    @staticmethod
    def show(events: List[EventInterface], relations: List[Relation]):
        graph = nx.DiGraph()

        for relation in relations:
            source = events[relation.source - 1]
            target = events[relation.target - 1]
            graph.add_edges_from([(target, source)])

        colors = []
        borders = []
        for event in graph.nodes:
            colors.append('#FFFFFF' if event.shadow else '#F8F8F8')
            borders.append('#EDEDED' if event.shadow else '#DEDEDE')

        # This needs to be last as events are transformed to strings.
        nx.relabel_nodes(graph, lambda event: event.label, copy=False)

        nx.draw_networkx(graph, node_size=2000, node_color=colors, edgecolors=borders)
        plt.margins(0.25)
        plt.show()
