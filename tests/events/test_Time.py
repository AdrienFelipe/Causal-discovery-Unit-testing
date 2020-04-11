import random
import unittest
from datetime import datetime

from events.Time import Time


class TimeTest(unittest.TestCase):
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
