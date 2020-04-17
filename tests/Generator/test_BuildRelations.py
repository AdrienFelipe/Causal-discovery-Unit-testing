import unittest
from collections import Callable
from typing import List

from Generator import Generator
from History import History
from Relation import Relation


class RelationFactoryTest(unittest.TestCase):
    def test_simple_relation_function(self):
        def effect_function(history: History) -> float:
            return history.get_effect()

        relations = Generator() \
            .add_effect(effect_function) \
            .build_relations()

        expected = [
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, History.DEFAULT_DELAY)
        ]

        self.assertEqualRelation(expected, relations)

    def test_function_combinations(self):
        def effect_function(history: History) -> float:
            value = history.get_effect()
            if history.get_effect(201, delay=200):
                value *= 1.5
            elif history.get_effect(position=301, delay=300, null_value=None):
                value *= 3
            elif history.get_effect(delay=500):
                value *= 3
            elif history.get_effect(delay=600, position=601):
                value *= 3
            value = history.get_effect(401) + 4

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
            return h.get_effect()

        def effect_function2(var) -> float:
            return var.get_effect(10, delay=20)

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


if __name__ == '__main__':
    unittest.main()
