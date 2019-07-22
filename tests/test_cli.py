import json

import pytest
from click.testing import CliRunner

from unbabel_cli.cli import run


class TestCli(object):

    @pytest.fixture
    def result(self):
        return json.load(open('./fixtures/output.json'))

    def test_cli_throws_no_exception_with_default_parameters(self):
        runner = CliRunner()
        output = runner.invoke(run)
        assert not output.exception
        assert output.exit_code == 0

    def test_cli_works_with_default_parameters(self):
        runner = CliRunner()
        output = json.loads(runner.invoke(run).stdout)
        expected_output = self.result()
        assert output == expected_output

