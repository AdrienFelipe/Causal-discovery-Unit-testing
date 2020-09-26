import random
import unittest
from datetime import datetime

from generator.events.Time import Time


class TimeTest(unittest.TestCase):
    def test_step(self):
        start_timestamp = 1582153200
        step = 60 * 60
        time_event = Time('2020-02-20', step='1h')
        for count in range(24):
            timestamp = time_event.generate()
            expected = start_timestamp + step * count
            self.assertEqual(expected, timestamp)

    def test_step_with_precision(self):
        random.seed(1)

        start_timestamp = 1582153200
        step = 60 * 60 * 5
        precision = 600 + 20 * 60
        time_event = Time('2020-02-20', step='5h', precision='20m600s')
        for count in range(30):
            timestamp = time_event.generate()
            expected_low = start_timestamp + step * count - precision
            expected_high = start_timestamp + step * count + precision
            self.assertGreaterEqual(timestamp, expected_low)
            self.assertLess(timestamp, expected_high)

    def test_precision(self):
        random.seed(1)

        min_day = max_day = None
        for step in range(100):
            timestamp = Time('2020-02-20', step='0s', precision='5d').generate()
            day = datetime.fromtimestamp(timestamp).day
            month = datetime.fromtimestamp(timestamp).month
            year = datetime.fromtimestamp(timestamp).year

            min_day = day if min_day is None else min(day, min_day)
            max_day = day if max_day is None else max(day, max_day)

            self.assertEqual(2020, year)
            self.assertEqual(2, month)
            self.assertLessEqual(day, 24)
            self.assertGreaterEqual(day, 15)

        self.assertEqual(24, max_day)
        self.assertEqual(15, min_day)


if __name__ == '__main__':
    unittest.main()
