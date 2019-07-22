import pytest

from unbabel_cli.helpers import extract_events_from_input_file


class TestHelpers(object):

    def test_that_reading_ok_file_works(self):
        events = extract_events_from_input_file('./fixtures/events_ok.json')
        assert len(events) == 3

    def test_that_read_events_are_ok(self):
        events = extract_events_from_input_file('./fixtures/events_ok.json')
        for event in events:
            assert event.duration
            assert event.timestamp

    def test_that_reading_ok_file_raises_value_error(self):
        with pytest.raises(ValueError):
            extract_events_from_input_file('./fixtures/events_ko.json')
