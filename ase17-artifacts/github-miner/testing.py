import unittest

from datetime import date, timedelta

from core import TimeInterval


class TimeIntervalTest(unittest.TestCase):
    def test_init(self):
        t = TimeInterval("2016-01-01", "2017-01-01")
        self.assertEqual(t.starting_date, date(2016, 1, 1))
        self.assertEqual(t.ending_date, date(2017, 1, 1))
        self.assertEqual(t.delta, timedelta(days=30))

        t = TimeInterval("2016-01-01")
        self.assertEqual(t.ending_date, date.today())

    def test_iterator(self):
        t = TimeInterval("2016-01-01", "2016-01-20",  delta=1)
        expected_dates = ["2016-01-{:02}".format(d) for d in range(1, 20 + 1)]

        i = 0
        for interval in t:
            expected = (expected_dates[i], expected_dates[i + 1])
            self.assertEqual(interval, expected)
            i += 2

        self.assertEqual(i, len(expected_dates), "Expected to compare with all intervals")


if __name__ == "__main__":
    unittest.main()

