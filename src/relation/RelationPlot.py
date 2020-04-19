from typing import List

import matplotlib.pyplot as plt
import networkx as nx

from events.EventInterface import EventInterface
from relation.Relation import Relation


class RelationPlot:

    @staticmethod
    def show(events: List[EventInterface], relations: List[Relation]):
        graph = nx.DiGraph()

        for relation in relations:
            source = events[relation.source]
            target = events[relation.target]
            graph.add_edges_from([(target, source)])

        # Sort nodes for the colors to be correctly applied.
        from functools import cmp_to_key
        graph_events = graph.nodes
        graph_events = sorted(graph_events, key=cmp_to_key(lambda event1, event2: event1.position - event2.position))

        colors = []
        borders = []
        for event in graph_events:
            colors.append('#FFFFFF' if event.shadow else '#F8F8F8')
            borders.append('#EDEDED' if event.shadow else '#DEDEDE')

        # This needs to be last as events are transformed to strings.
        nx.relabel_nodes(graph, lambda event: event.label, copy=False)

        nx.draw_networkx(graph, node_size=2000, node_color=colors, edgecolors=borders)
        plt.margins(0.25)
        plt.show()
