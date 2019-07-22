import itertools
from datetime import timedelta, datetime
from typing import List

import numpy as np
from dateutil.rrule import rrule, MINUTELY
from sortedcontainers import SortedList

from unbabel_cli.helpers import Event, Average


def calculate_moving_average(events: SortedList, window_size: int) -> List[Average]:
    """
    Calculates the moving average of a list of `Event` by a sliding window of `window_size`
    Running complexity O(n*log(n)) where n == len(events)
    """
    earliest_event, latest_event = _first_and_last_of(events)

    timestamps_between_start_end = _calculate_per_minute_timestamp(
        earliest_event.timestamp,
        latest_event.timestamp
    )

    averages = []
    for idx, window_between_start_and_end in enumerate(_sliding_window(timestamps_between_start_end, size=window_size)):
        earliest_timestamp, latest_timestamp = _first_and_last_of(window_between_start_and_end)
        events_in_range = _get_events_in_range(events, earliest_timestamp, latest_timestamp)
        averages.append(Average(latest_timestamp, _calculate_mean_duration(events_in_range)))

    return averages


def _calculate_per_minute_timestamp(start_date: datetime, end_date: datetime) -> List:
    """
    Returns a list of datetime, one per minute, between start_date and end_date
    """
    return list(rrule(
        freq=MINUTELY,
        dtstart=_floor_nearest_minute(start_date),
        until=_ceil_nearest_minute(end_date)
    ))


def _floor_nearest_minute(timestamp: datetime) -> datetime:
    return timestamp.replace(second=0)


def _ceil_nearest_minute(timestamp: datetime) -> datetime:
    return _floor_nearest_minute(timestamp + timedelta(minutes=1))


def _sliding_window(
        seq: List,
        size: int=10,
        fill=None,
        fill_left: bool=True,
        fill_right: bool=False
):
    """ Returns a sliding window (of width n) over data from the iterable:
      s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ... by optionally filling
      non-covered window areas. Inspired by itertools examples at
      https://docs.python.org/release/2.3.5/lib/itertools-example.html
    """
    sliding_size = size - 1
    it = itertools.chain(
        itertools.repeat(fill, sliding_size * fill_left),
        iter(seq),
        itertools.repeat(fill, sliding_size * fill_right))

    result = tuple(itertools.islice(it, size))

    if len(result) == size:
        yield result

    for elem in it:
        result = result[1:] + (elem,)
        yield result


def _first_and_last_of(iterable: List):
    if len(iterable) == 0:
        raise ValueError("No first and left for empty list")
    return iterable[0], iterable[-1]


def _get_events_in_range(events: SortedList, earliest_timestamp: datetime, latest_timestamp: datetime) -> List[Event]:
    """
    Select events within `earliest_timestamp` and `latest_timestamp`
    Running complexity O(log(n)) where n == len(events)
    """
    def _sorting_event_of(timestamp):
        return Event(timestamp, 0)

    if earliest_timestamp and latest_timestamp:
        return events[
               events.bisect_left(_sorting_event_of(earliest_timestamp)):
               events.bisect_right(_sorting_event_of(latest_timestamp))
               ]
    if earliest_timestamp:
        return events[events.bisect_left(_sorting_event_of(earliest_timestamp)):]

    return events[:events.bisect_right(_sorting_event_of(latest_timestamp))]


def _calculate_mean_duration(events: List[Event]):
    if not events:
        return 0
    return np.mean([event.duration for event in events])
