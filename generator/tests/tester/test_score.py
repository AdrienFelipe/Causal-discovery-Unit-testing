import unittest

from generator.relation.Relation import Relation
from discovery.EvaluateLearner import EvaluateLearner
from tests.generator.asserts.RelationAssert import RelationAssert


class EvaluateLearnerTest(unittest.TestCase):

    def test_compare_relations(self):
        real_relations = [
            Relation(0, 1, 0),
            Relation(0, 2, 0),
            Relation(4, 2, 0),
        ]
        learned_relations = [
            Relation(0, 2, 0),
            Relation(1, 0, 0),
            Relation(3, 1, 0),
        ]
        expected_missing = [
            Relation(4, 2, 0),
        ]
        expected_added = [
            Relation(3, 1, 0),
        ]
        expected_inverted = [
            Relation(1, 0, 0),
        ]

        missing, added, inverted = EvaluateLearner.compare_relations(real_relations, learned_relations)

        RelationAssert.equal(self, expected_missing, missing, 'Missing relations')
        RelationAssert.equal(self, expected_added, added, 'Added relations')
        RelationAssert.equal(self, expected_inverted, inverted, 'Inverted relations')

    def test_empty_learned(self):
        real_relations = [
            Relation(0, 1, 0),
            Relation(0, 2, 0),
        ]
        learned_relations = []

        expected_missing = [
            Relation(0, 1, 0),
            Relation(0, 2, 0),
        ]
        expected_added = []
        expected_inverted = []

        missing, added, inverted = EvaluateLearner.compare_relations(real_relations, learned_relations)

        RelationAssert.equal(self, expected_missing, missing, 'Missing relations')
        RelationAssert.equal(self, expected_added, added, 'Added relations')
        RelationAssert.equal(self, expected_inverted, inverted, 'Inverted relations')


if __name__ == '__main__':
    unittest.main()
