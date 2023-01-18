#  Copyright (c) 2023. OCX Consortium https://3docx.org. See the LICENSE
#
from click.testing import CliRunner
from ocx_tools.cli.cli_main import cli

def test_table_defaults():
    runner = CliRunner()
    result = runner.invoke(cli, ['table-defaults'])
    assert result.exit_code == 0

def test_table_options():
    runner = CliRunner()
    result = runner.invoke(cli,['table-options','--fmt', 'fancy_grid', '--row-numbers', 'True'])
    assert result.exit_code == 0

def test_log_level():
    runner = CliRunner()
    result = runner.invoke(cli,['log-level'])
    assert result.exit_code == 0

def test_set_level():
    runner = CliRunner()
    result = runner.invoke(cli,['set-level', '--level', 'DEBUG'])
    assert result.exit_code == 0
