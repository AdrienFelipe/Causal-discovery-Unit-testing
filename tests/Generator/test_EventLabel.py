import unittest

from Generator import Generator
from events.EventInterface import EventInterface


class EventLabelTest(unittest.TestCase):
    def test_single_label(self):
        dataset = Generator(lambda history: 1) \
            .add_cause_continuous() \
            .add_noise_continuous() \
            .generate()

        self.assertEqual(EventInterface.LABEL_CAUSE, dataset.columns[0])
        self.assertEqual(EventInterface.LABEL_NOISE, dataset.columns[1])

    def test_multiple_cause_labels(self):
        dataset = Generator(lambda history: 1) \
            .add_cause_continuous() \
            .add_cause_continuous() \
            .add_cause_continuous() \
            .add_noise_continuous() \
            .generate()

        self.assertEqual(EventInterface.LABEL_CAUSE + '1', dataset.columns[0])
        self.assertEqual(EventInterface.LABEL_CAUSE + '2', dataset.columns[1])
        self.assertEqual(EventInterface.LABEL_CAUSE + '3', dataset.columns[2])
        self.assertEqual(EventInterface.LABEL_NOISE, dataset.columns[3])

    def test_multiple_labels(self):
        dataset = Generator(lambda history: 1) \
            .add_cause_continuous() \
            .add_cause_continuous() \
            .add_noise_continuous() \
            .add_noise_continuous() \
            .generate()

        self.assertEqual(EventInterface.LABEL_CAUSE + '1', dataset.columns[0])
        self.assertEqual(EventInterface.LABEL_CAUSE + '2', dataset.columns[1])
        self.assertEqual(EventInterface.LABEL_NOISE + '1', dataset.columns[2])
        self.assertEqual(EventInterface.LABEL_NOISE + '2', dataset.columns[3])


if __name__ == '__main__':
    unittest.main()
