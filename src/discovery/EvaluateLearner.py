from __future__ import annotations

import datetime
from typing import List

import matplotlib.pyplot as plt
from tabulate import tabulate
from termcolor import colored

from datasets.DatasetInterface import DatasetInterface
from discovery.ScriptInterface import ScriptInterface
from generator.events.EventInterface import EventInterface
from generator.relation.Relation import Relation
from generator.relation.RelationPlot import RelationPlot


class EvaluateLearner:
    EXIT_CODE_SUCCESS = 0
    EXIT_CODE_FAILED = 1

    TABLE_OUTPUT = 'table'
    GRAPH_OUTPUT = 'graph'

    @staticmethod
    def run(scripts: List[ScriptInterface], datasets: List[DatasetInterface], threshold=90, output=TABLE_OUTPUT,
            force_rebuild=False, dpi=None):
        # Whether all explorations met the threshold.
        exit_status = EvaluateLearner.EXIT_CODE_SUCCESS

        results = {}
        for dataset in datasets:
            # Make sure dataset file was generated.
            dataset.get_data(force_rebuild)
            for script in scripts:
                generator = dataset.get_generator()
                events = generator.get_events(include_shadow=False)
                relations = generator.build_relations(include_shadow=False)

                # Measure algorithm execution time.
                time = datetime.datetime.now()
                ori_learned = script.predict(dataset)
                time = (datetime.datetime.now() - time).total_seconds()

                learned = EvaluateLearner.relations_to_label(ori_learned, events)
                real = EvaluateLearner.relations_to_label(relations, generator.get_events())

                missing, added, inverted = EvaluateLearner.compare_relations(real, learned)
                found = 1 - (len(missing) + len(inverted) + len(added)) / (len(real) + len(added)) \
                    if len(real) + len(added) > 0 else 0

                # Validate threshold.
                if found < threshold / 100:
                    exit_status = EvaluateLearner.EXIT_CODE_FAILED

                # Format print outputs with colors.
                color = 'red' if found < 0.5 else 'yellow' if found < 0.75 else 'green'
                found_print = colored(f'{int(found * 100)}%', color)
                erroneous_print = colored(len(added), 'red' if len(added) > 0 else 'white')
                inverted_print = colored(len(inverted), 'red' if len(inverted) > 0 else 'white')
                missing_print = colored(len(missing), 'red' if len(missing) > 0 else 'white')

                # Build results to be printed
                if output == EvaluateLearner.TABLE_OUTPUT:
                    results.setdefault('dataset', []).append(dataset.get_label())
                    results.setdefault('samples', []).append(dataset.samples)
                    results.setdefault('library', []).append(script.library)
                    results.setdefault('algorithm', []).append(colored(script.algorithm, 'cyan'))
                    results.setdefault('found', []).append(found_print)
                    results.setdefault('erroneous', []).append(erroneous_print)
                    results.setdefault('inverted', []).append(inverted_print)
                    results.setdefault('missing', []).append(missing_print)
                    results.setdefault('time', []).append(f'{int(time * 1000)}ms')

                # Plot graph output.
                elif output == EvaluateLearner.GRAPH_OUTPUT:
                    print('\n\n')
                    print(f'{dataset.get_label()} → {script.algorithm} ({script.library}): {found_print}')

                    fig, ax = plt.subplots(1, 2, figsize=(17, 5), dpi=dpi)
                    RelationPlot.draw_plot(generator.get_events(), relations, ax=ax[0], title='Original graph',
                                           node_size=dataset.node_size)
                    RelationPlot.draw_plot(events, ori_learned, ax=ax[1], title='Learned graph',
                                           node_size=dataset.node_size)

                    plt.show()

        if output == EvaluateLearner.TABLE_OUTPUT:
            print()
            print(tabulate(results, headers='keys'))
            print()

        return exit_status

    @staticmethod
    def relations_to_label(relations: List[Relation], events: List[EventInterface]) -> List[Relation]:
        labeled_relations = []
        for relation in relations:
            labeled_relations.append(
                Relation(events[relation.target].label, events[relation.source].label, relation.delay))

        # Sort relations.
        labeled_relations.sort(key=lambda item: item.source)

        return labeled_relations

    @staticmethod
    def compare_relations(real_relations, learned_relations):
        missing = []
        added = learned_relations.copy()
        inverted = []

        for real in real_relations:
            found = False
            for learned in added:
                if real.source == learned.source and real.target == learned.target:
                    added.remove(learned)
                    found = True
                    break
                elif real.source == learned.target and real.target == learned.source:
                    added.remove(learned)
                    inverted.append(learned)
                    found = True
                    break
            if not found:
                missing.append(real)

        return missing, added, inverted
