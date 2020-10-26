import unittest

from generator.Generator import Generator
from generator.events.EventInterface import EventInterface


class GetEventsTest(unittest.TestCase):
    def test_get_all_events(self):
        generator = Generator() \
            .add_uniform() \
            .add_uniform()

        events = generator.get_events()
        expected_events = ['T', 'E1', 'E2']

        for key, event in enumerate(events):
            self.assertEqual(event.label, expected_events[key])

    def test_get_events_exclude_shadow(self):
        generator = Generator() \
            .add_uniform() \
            .add_uniform(shadow=True) \
            .add_uniform()

        events = generator.get_events(include_shadow=False)
        expected_events = ['E1', 'E3']

        for key, event in enumerate(events):
            self.assertEqual(event.label, expected_events[key])


if __name__ == '__main__':
    unittest.main()
