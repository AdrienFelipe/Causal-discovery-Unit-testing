import unittest
from collections import Callable
from typing import List

from Generator import Generator
from History import History
from relation.Relation import Relation


class RelationFactoryTest(unittest.TestCase):
    def test_simple_relation_function(self):
        def effect_function(history: History) -> float:
            return history.get_event()

        relations = Generator() \
            .add_effect(effect_function) \
            .build_relations()

        expected = [
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, History.DEFAULT_DELAY)
        ]

        self.assertEqualRelation(expected, relations)

    def test_function_combinations(self):
        def effect_function(history: History) -> float:
            value = history.get_event()
            if history.get_event(201, delay=200):
                value *= 1.5
            elif history.get_event(position=301, delay=300, null_value=None):
                value *= 3
            elif history.get_event(delay=500):
                value *= 3
            elif history.get_event(delay=600, position=601):
                value *= 3
            value = history.get_event(401) + 4

            return value

        relations = Generator() \
            .add_effect(effect_function) \
            .build_relations()

        expected = [
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, History.DEFAULT_DELAY),
            Relation(History.DEFAULT_POSITION, 201, 200),
            Relation(History.DEFAULT_POSITION, 301, 300),
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, 500),
            Relation(History.DEFAULT_POSITION, 601, 600),
            Relation(History.DEFAULT_POSITION, 401, History.DEFAULT_DELAY),
        ]

        self.assertEqualRelation(expected, relations)

    def test_function_short_variable(self):
        def effect_function1(h: History) -> float:
            return h.get_event()

        def effect_function2(var) -> float:
            return var.get_event(10, delay=20)

        def effect_function3(h) -> float:
            return h

        relations = Generator() \
            .add_effect(effect_function1) \
            .add_effect(effect_function2) \
            .add_effect(effect_function3) \
            .build_relations()

        expected = [
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, History.DEFAULT_DELAY),
            Relation(History.DEFAULT_POSITION + 1, 10, 20),
        ]

        self.assertEqualRelation(expected, relations)

    def test_different_event_types(self):
        self.skipTest('Group al events first')

    def assertEqualRelation(self, expected: List[Relation], relations: List[Relation]):
        self.assertEqual(len(expected), len(relations))
        for key, relation in enumerate(relations):
            self.assertEqual(expected[key].source, relation.source, 'Incorrect source')
            self.assertEqual(expected[key].target, relation.target, 'Incorrect target')
            self.assertEqual(expected[key].delay, relation.delay, 'Incorrect delay')

    def test_fuck_sake(self):
        import networkx as nx

        def effect1(history: History) -> float:
            return 4

        def effect2(history: History) -> float:
            return history.get_event(position=1)

        def effect3(history: History) -> float:
            if history.get_event(1, delay=1):
                value += 500
            if history.get_event(1, delay=2):
                value += 400
            if history.get_event(2, delay=3):
                value += 200

            return value

        generator = Generator() \
            .add_effect(effect1) \
            .add_effect(effect2) \
            .add_effect(effect3)

        relations = generator.build_relations()

        G = nx.DiGraph()

        for relation in relations:
            source = generator.get_effects()[relation.source - 1]
            target = generator.get_effects()[relation.target - 1]
            G.add_edges_from([(source.label, target.label)], weight=relation.delay)

if __name__ == '__main__':
    unittest.main()
