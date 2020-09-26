import unittest

from History import History
from generator.events.Linear import Linear
from generator.events.Time import Time


class HistoryTest(unittest.TestCase):
    def test_simple_time_range(self):
        events = [
            Time('2020-02-10', step='5m'),
            Linear(start=0, step=1),
            Linear(start=0, step=-1),
        ]
        history = History()
        history.start(events_count=len(events))
        for _ in range(10):
            for position, event in enumerate(events):
                event.position = position
                history.set_event(event, event.generate())

        self.assertEqual([10, 9, 8], list(history.get_range(1, '15m')))
        self.assertEqual([-10, -9, -8], list(history.get_range(2, '15m')))
        self.assertEqual([10, 9, 8], list(history.get_range(1, '720s')))


if __name__ == '__main__':
    unittest.main()
