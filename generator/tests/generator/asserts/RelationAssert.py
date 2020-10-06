import unittest
from typing import List

from generator.relation.Relation import Relation


class RelationAssert:

    @staticmethod
    def equal(test: unittest.TestCase, expected: List[Relation], relations: List[Relation], message: str = ''):
        # Format input message to a better output.
        if message:
            message = f'{message}: '

        test.assertEqual(len(expected), len(relations), message + 'number of relations does not match')
        for key, relation in enumerate(relations):
            test.assertEqual(expected[key].source, relation.source, message + f'Incorrect source (key {key})')
            test.assertEqual(expected[key].target, relation.target, message + f'Incorrect target (key {key})')
            test.assertEqual(expected[key].delay, relation.delay, message + f'Incorrect delay (key {key})')
