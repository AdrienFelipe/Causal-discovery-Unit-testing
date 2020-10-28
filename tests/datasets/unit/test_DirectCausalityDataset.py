import random
import unittest

from datasets.unit.DirectCausalityDataset import DirectCausalityDataset
from utils import ProjectRoot


class DirectCausalityDatasetTest(unittest.TestCase):

    def setUp(self):
        random.seed(0)

    def test_linear(self):
        dataset = DirectCausalityDataset.linear(10)
        # Test dataset label.
        self.assertEqual('Direct Causality - Linear', dataset.get_label())
        # Test dataset file path.
        expected_path = ProjectRoot.get() / 'res/datasets/direct-causality-linear-10.csv'
        self.assertEqual(expected_path, dataset.get_filepath())
        # Test dataset value.
        data = dataset.get_generator().generate()
        self.assertEqual(4, data['E4'][0])

    def test_square_root(self):
        dataset = DirectCausalityDataset.square_root()
        data = dataset.get_generator().generate()
        self.assertEqual(4, data['E4'][0])

    def test_power(self):
        dataset = DirectCausalityDataset.power()
        data = dataset.get_generator().generate()
        self.assertEqual(4, data['E4'][0])

    def test_exponential(self):
        dataset = DirectCausalityDataset.exponential()
        data = dataset.get_generator().generate()
        self.assertEqual(4, data['E4'][0])


if __name__ == '__main__':
    unittest.main()
