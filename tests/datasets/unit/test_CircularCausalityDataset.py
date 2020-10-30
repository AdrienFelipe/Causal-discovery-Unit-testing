import random
import unittest

from datasets.unit.CircularCausalityDataset import CircularCausalityDataset


class CircularCausalityDatasetTest(unittest.TestCase):

    def setUp(self):
        random.seed(0)

    def test_discrete(self):
        dataset = CircularCausalityDataset.discrete()
        data = dataset.get_generator().generate(20)

        expected_first_row = [0, 0, 0, 0, 9]
        self.assertEqual(expected_first_row, list(data.iloc[0]))


if __name__ == '__main__':
    unittest.main()
