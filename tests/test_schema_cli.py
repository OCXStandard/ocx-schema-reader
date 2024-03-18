#  Copyright (c) 2023. OCX Consortium https://3docx.org. See the LICENSE
#
from click.testing import CliRunner

from ocx_tools.cli.cli_main import cli, schema


def test_schema():
    runner = CliRunner()
    result = runner.invoke(cli, ["schema"])
    assert result.exit_code == 0


def test_schema_parse():
    runner = CliRunner()
    result = runner.invoke(cli, ["schema", "parse"])
    assert result.exit_code == 0
