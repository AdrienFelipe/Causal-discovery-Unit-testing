from __future__ import annotations

import datetime
from typing import List

from tabulate import tabulate
from termcolor import colored

from datasets.DatasetInterface import DatasetInterface
from discovery.scripts.ScriptInterface import ScriptInterface
from generator.events.EventInterface import EventInterface
from generator.relation.Relation import Relation


class EvaluateLearner:

    @staticmethod
    def run(scripts: List[ScriptInterface], datasets: List[DatasetInterface], threshold=90, force_rebuild=False):
        # Whether all explorations met the threshold.
        failed = False

        results = {}
        for dataset in datasets:
            # Make sure dataset file was generated.
            dataset.get_data(force_rebuild)
            for script in scripts:
                generator = dataset.get_generator()

                # Measure algorithm execution time.
                time = datetime.datetime.now()
                learned = script.predict(dataset)
                time = (datetime.datetime.now() - time).total_seconds()
                learned = EvaluateLearner.relations_to_label(learned, generator.get_events(include_shadow=False))

                real = EvaluateLearner.relations_to_label(generator.build_relations(), generator.get_events())

                # generator.plot_relations(fig_size=(10, 10))
                # RelationPlot.show(generator.get_events(include_shadow=False), learned_relations, figsize=(10, 10))

                missing, added, inverted = EvaluateLearner.compare_relations(real, learned)
                found = 1 - (len(missing) + len(inverted)) / len(real)
                color = 'red' if found < 0.5 else 'yellow' if found < 0.75 else 'green'

                # Validate threshold.
                if found < threshold / 100:
                    failed = True

                # Build results to be printed
                results.setdefault('dataset', []).append(dataset.name)
                results.setdefault('samples', []).append(dataset.samples)
                results.setdefault('library', []).append(script.name)
                results.setdefault('algorithm', []).append(script.algorithm)
                results.setdefault('found', []).append(colored(f'{int(found * 100)}%', color))
                results.setdefault('erroneous', []).append(colored(len(added), 'red' if len(added) > 0 else 'white'))
                results.setdefault('inverted', []).append(
                    colored(len(inverted), 'red' if len(inverted) > 0 else 'white'))
                results.setdefault('missing', []).append(colored(len(missing), 'red' if len(missing) > 0 else 'white'))
                results.setdefault('time', []).append(f'{int(time * 1000)}ms')

        print()
        print(tabulate(results, headers='keys'))
        print()

        return failed

    @staticmethod
    def relations_to_label(relations: List[Relation], events: List[EventInterface]) -> List[Relation]:
        labeled_relations = []
        for relation in relations:
            labeled_relations.append(
                Relation(events[relation.source].label, events[relation.target].label, relation.delay))

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
