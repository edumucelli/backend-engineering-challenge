import json
from json import JSONDecodeError
from typing import List

from dateutil.parser import parse
from sortedcontainers import SortedList

DURATION_ATTRIBUTE = 'duration'
TIMESTAMP_ATTRIBUTE = 'timestamp'


class Event(object):
    def __init__(self, timestamp, duration):
        self.timestamp = timestamp
        self.duration = duration

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __gt__(self, other):
        return self.timestamp > other.timestamp

    def __ge__(self, other):
        return self.timestamp >= other.timestamp

    def __le__(self, other):
        return self.timestamp <= other.timestamp

    def __str__(self):
        return "%s: %s" % (self.timestamp, self.duration)

    def __repr__(self):
        return self.__str__()


class Average(object):
    def __init__(self, date, average_delivery_time):
        self.date = date
        self.average_delivery_time = average_delivery_time


def extract_events_from_input_file(input_file_name: str) -> SortedList:
    """
    Get events from input file and store them
    ascending by timestamp, just in case input
    file is out of order.
    Run complexity is O(n*log(n)) where n == # of lines
    """
    with open(input_file_name) as input_file:
        return SortedList([
            _event_from_input_file_line(line)
            for line in input_file
        ])


def _event_from_input_file_line(input_file_line: str) -> Event:
    try:
        line_as_json = json.loads(input_file_line)
    except JSONDecodeError:
        raise ValueError("Invalid JSON event line format")
    timestamp = parse(line_as_json[TIMESTAMP_ATTRIBUTE])
    duration = int(line_as_json[DURATION_ATTRIBUTE])
    return Event(timestamp, duration)


def to_json(averages: List[Average]) -> str:
    formatted = [
        {"date": average.date, "average_delivery_time": average.average_delivery_time}
        for average in averages
    ]

    return json.dumps(formatted, default=str)
