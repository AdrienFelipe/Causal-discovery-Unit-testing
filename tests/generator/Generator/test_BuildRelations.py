import unittest
from collections.abc import Callable

from generator.Generator import Generator
from generator.History import History
from generator.relation.Relation import Relation
from tests.generator.asserts.RelationAssert import RelationAssert


class RelationFactoryTest(unittest.TestCase):
    def test_simple_relation_function(self):
        def effect_function(history: History) -> float:
            return history.get_event()

        relations = Generator() \
            .add_function(effect_function) \
            .build_relations()

        expected = [
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, History.DEFAULT_DELAY)
        ]

        RelationAssert.equal(self, expected, relations)

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
            .add_function(effect_function) \
            .build_relations()

        expected = [
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, History.DEFAULT_DELAY),
            Relation(201, History.DEFAULT_POSITION, 200),
            Relation(301, History.DEFAULT_POSITION, 300),
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, 500),
            Relation(601, History.DEFAULT_POSITION, 600),
            Relation(401, History.DEFAULT_POSITION, History.DEFAULT_DELAY),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_function_short_variable(self):
        def effect_function1(h: History) -> float:
            return h.get_event()

        def effect_function2(var) -> float:
            return var.get_event(10, delay=20)

        def effect_function3(h) -> float:
            return h

        relations = Generator() \
            .add_function(effect_function1) \
            .add_function(effect_function2) \
            .add_function(effect_function3) \
            .build_relations()

        expected = [
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION, History.DEFAULT_DELAY),
            Relation(10, History.DEFAULT_POSITION + 1, 20),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_lambda_as_function(self):
        function1: Callable[[History], float] = lambda history: \
            1 if history.get_event(0) == 1 else 0

        function2 = lambda h: max([1, 4]) if h.get_event() == 1 else 0

        relations = Generator() \
            .add_function(function1) \
            .add_function(function2) \
            .build_relations()

        expected = [
            Relation(0, History.DEFAULT_POSITION, History.DEFAULT_DELAY),
            Relation(History.DEFAULT_POSITION, History.DEFAULT_POSITION + 1, History.DEFAULT_DELAY),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_lambda_as_argument(self):
        relations = Generator() \
            .add_uniform() \
            .add_uniform(6, 10).add_function(lambda h: h.get_event(2, delay=3)) \
            .build_relations()

        expected = [
            Relation(2, 3, 3),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_circular_relations(self):
        relations = Generator() \
            .add_function(lambda h: round(h.e(2, delay=0))) \
            .add_function(lambda h: round(h.e(3, delay=1))) \
            .add_function(lambda h: round(h.e(4, delay=2))) \
            .add_function(lambda h: round(h.e(1, delay=3))) \
            .build_relations()

        expected = [
            Relation(2, 1, 0),
            Relation(3, 2, 1),
            Relation(4, 3, 2),
            Relation(1, 4, 3),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_circular_relations_excluding_shadows(self):
        functions = [
            lambda h: round((h.e(2, delay=0) or 0), 0),
            lambda h: round((h.e(3, delay=1) or 0), 0),
            lambda h: round((h.e(4, delay=2) or 0), 0),
            lambda h: round((h.e(1, delay=3) or 0), 0),
        ]

        relations = Generator() \
            .add_function(functions[0]) \
            .add_function(functions[1]) \
            .add_function(functions[2], shadow=True) \
            .add_function(functions[3]) \
            .add_discrete(3) \
            .build_relations(include_shadow=False)

        expected = [
            Relation(2, 1, 0),
            Relation(1, 4, 0),
            Relation(4, 2, 0),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_with_time(self):
        function1: Callable[[History], float] = lambda history: \
            1 if history.get_datetime() == 1 else history.get_event()

        def function2(h: History) -> float: return h.get_timestamp()

        relations = Generator() \
            .add_function(function1) \
            .add_function(function2) \
            .add_function(lambda v: v.get_datetime(delay=2)) \
            .build_relations()

        expected = [
            Relation(0, 1, 0),
            Relation(1, 1, 0),
            Relation(0, 2, 0),
            Relation(0, 3, 2),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_different_event_types(self):
        event_function: Callable[[History], float] = lambda history: \
            1 if history.get_event() == 1 else history.get_event(2, delay=1)

        relations = Generator() \
            .add_uniform() \
            .add_discrete() \
            .add_function(event_function) \
            .add_linear() \
            .build_relations()

        expected = [
            Relation(1, 3, 0),
            Relation(2, 3, 1),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_independent_effects(self):
        relations = Generator() \
            .add_uniform() \
            .add_function(lambda h: h.get_event()) \
            .add_linear() \
            .add_function(lambda h: h.get_event(3)) \
            .build_relations()

        expected = [
            Relation(1, 2, 0),
            Relation(3, 4, 0),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_time_arguments(self):
        def func1(history: History) -> float:
            return history.get_datetime().weekday()

        def func2(history: History) -> float:
            return history.get_datetime(1).isocalendar()[1]

        def func3(history: History) -> float:
            return history.get_timestamp(delay=2)

        relations = Generator() \
            .set_time('2020-02-20', step='1d') \
            .add_function(func1, shadow=True) \
            .add_function(func2, shadow=True) \
            .add_function(func3, shadow=True) \
            .add_function(lambda h: h.get_event(1) * h.get_event(2, delay=2) * h.get_event(3)) \
            .build_relations()

        expected = [
            Relation(0, 1, 0),
            Relation(0, 2, 1),
            Relation(0, 3, 2),
            Relation(1, 4, 0),
            Relation(2, 4, 2),
            Relation(3, 4, 0),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_jump_shadows(self):
        relations = Generator() \
            .set_time('2020-02-20', step='1d') \
            .add_uniform(label='1') \
            .add_uniform(label='2') \
            .add_function(lambda h: h.e(0), label='3') \
            .add_function(lambda h: h.e(3) + h.e(2), shadow=True, label='4') \
            .add_function(lambda h: h.e(4), shadow=True, label='5') \
            .add_function(lambda h: h.e(5), label='6') \
            .build_relations(include_shadow=False)

        expected = [
            Relation(2, 6),
            Relation(0, 3),
            Relation(3, 6),
        ]

        RelationAssert.equal(self, expected, relations)

    def test_shadows_doubles(self):
        relations = Generator() \
            .add_function(lambda h: h.e(4) + h.e(6), shadow=True, label='1') \
            .add_function(lambda h: h.e(1) + h.e(7), label='2') \
            .add_function(lambda h: h.e(1), label='3') \
            .add_uniform(label='4') \
            .add_uniform(label='5') \
            .add_uniform(label='6') \
            .add_uniform(label='6') \
            .build_relations(include_shadow=False)

        expected = [
            Relation(7, 2),
            Relation(4, 2),
            Relation(4, 3),
            Relation(6, 2),
            Relation(6, 3),
        ]

        RelationAssert.equal(self, expected, relations)


if __name__ == '__main__':
    unittest.main()
