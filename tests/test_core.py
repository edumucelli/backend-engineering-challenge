import pytest

from datetime import datetime

from sortedcontainers import SortedList

from unbabel_cli.core import calculate_moving_average
from unbabel_cli.helpers import Event


class TestCore(object):

    @pytest.fixture(autouse=True)
    def events(self):
        return SortedList([
            Event(datetime(2018, 12, 26, 18, 11, 8, 509654), 20),
            Event(datetime(2018, 12, 26, 18, 15, 19, 903159), 31),
            Event(datetime(2018, 12, 26, 18, 23, 19, 903159), 54)
        ])

    def test_that_calculate_moving_average_returns_the_correct_number_of_averages(self):
        averages = calculate_moving_average(self.events(), 10)
        assert len(averages) == 14

    def test_that_calculate_moving_average_returns_the_correct_averages(self):
        averages = calculate_moving_average(self.events(), 10)
        expected_averages = [0, 20, 20, 20, 20, 25.5, 25.5, 25.5, 25.5, 25.5, 31, 31, 31, 42.5]

        for average, expected_average in zip(averages, expected_averages):
            assert average.average_delivery_time == expected_average
