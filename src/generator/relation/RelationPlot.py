from typing import List

import matplotlib.pyplot as plt
import networkx as nx

from generator.events.EventInterface import EventInterface
from generator.relation.Relation import Relation


class RelationPlot:

    @staticmethod
    def show(events: List[EventInterface], relations: List[Relation], figsize: tuple = (5, 3), node_size=2000):
        fig = plt.figure(figsize=figsize)
        RelationPlot.draw_plot(events, relations, node_size)
        plt.show()

    @staticmethod
    def draw_plot(events: List[EventInterface], relations: List[Relation], node_size=2000, ax=None, title=None):
        graph = nx.DiGraph()

        for relation in relations:
            source = events[relation.source]
            target = events[relation.target]
            graph.add_edges_from([(source, target)])

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

        if ax is not None:
            plt.sca(ax)
            ax.set_title(title, fontsize=12)
            plt.setp(ax.spines.values(), color='#CCCCCC')

        nx.draw_networkx(graph, node_size=node_size, node_color=colors, edgecolors=borders)
        plt.margins(0.25)
