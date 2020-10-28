import unittest

from discovery.EvaluateLearner import EvaluateLearner
from generator.relation.Relation import Relation
from tests.generator.asserts.RelationAssert import RelationAssert


class EvaluateLearnerTest(unittest.TestCase):

    def test_compare_relations(self):
        real_relations = [
           Relation(1, 0, 0),
           Relation(2, 0, 0),
           Relation(2, 4, 0),
        ]
        learned_relations = [
           Relation(2, 0, 0),
           Relation(0, 1, 0),
           Relation(1, 3, 0),
        ]
        expected_missing = [
           Relation(2, 4, 0),
        ]
        expected_added = [
           Relation(1, 3, 0),
        ]
        expected_inverted = [
           Relation(0, 1, 0),
        ]

        missing, added, inverted = EvaluateLearner.compare_relations(real_relations, learned_relations)

        RelationAssert.equal(self, expected_missing, missing, 'Missing relations')
        RelationAssert.equal(self, expected_added, added, 'Added relations')
        RelationAssert.equal(self, expected_inverted, inverted, 'Inverted relations')

    def test_empty_learned(self):
        real_relations = [
           Relation(1, 0, 0),
           Relation(2, 0, 0),
        ]
        learned_relations = []

        expected_missing = [
           Relation(1, 0, 0),
           Relation(2, 0, 0),
        ]
        expected_added = []
        expected_inverted = []

        missing, added, inverted = EvaluateLearner.compare_relations(real_relations, learned_relations)

        RelationAssert.equal(self, expected_missing, missing, 'Missing relations')
        RelationAssert.equal(self, expected_added, added, 'Added relations')
        RelationAssert.equal(self, expected_inverted, inverted, 'Inverted relations')


if __name__ == '__main__':
    unittest.main()
