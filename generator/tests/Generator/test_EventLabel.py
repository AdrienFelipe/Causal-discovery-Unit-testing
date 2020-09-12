import unittest

from Generator import Generator
from events.EventInterface import EventInterface


class EventLabelTest(unittest.TestCase):
    def test_single_label(self):
        dataset = Generator() \
            .add_uniform() \
            .add_uniform() \
            .generate()

        self.assertEqual(EventInterface.LABEL_EVENT + '1', dataset.columns[0])
        self.assertEqual(EventInterface.LABEL_EVENT + '2', dataset.columns[1])

    def test_multiple_cause_labels(self):
        dataset = Generator() \
            .add_uniform() \
            .add_uniform() \
            .add_uniform() \
            .add_uniform() \
            .generate()

        self.assertEqual(EventInterface.LABEL_EVENT + '1', dataset.columns[0])
        self.assertEqual(EventInterface.LABEL_EVENT + '2', dataset.columns[1])
        self.assertEqual(EventInterface.LABEL_EVENT + '3', dataset.columns[2])
        self.assertEqual(EventInterface.LABEL_EVENT + '4', dataset.columns[3])

    def test_multiple_labels(self):
        dataset = Generator() \
            .add_uniform() \
            .add_uniform() \
            .add_uniform() \
            .add_uniform() \
            .generate()

        self.assertEqual(EventInterface.LABEL_EVENT + '1', dataset.columns[0])
        self.assertEqual(EventInterface.LABEL_EVENT + '2', dataset.columns[1])
        self.assertEqual(EventInterface.LABEL_EVENT + '3', dataset.columns[2])
        self.assertEqual(EventInterface.LABEL_EVENT + '4', dataset.columns[3])


if __name__ == '__main__':
    unittest.main()
