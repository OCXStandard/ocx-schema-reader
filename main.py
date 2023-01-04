#  Copyright (c) 2022. OCX Consortium https://3docx.org. See the LICENSE

"""Allow the module to be run as a CLI. I.e.:
.. code-block:: shell-session
    $ python -m meta_package_manager
Removes empty string and current working directory from the first entry of
`sys.path`, if present to avoid using current directory
in subcommands when invoked as `python -m meta_package_manager <command>`.
"""

from __future__ import annotations
from pathlib import Path
from click_shell import shell
from click import pass_context, clear, option, secho, Choice
from tabulate import tabulate
import yaml
import logging
from logging import config
import colorlog

from ocx_schema_reader.cli import schema
from ocx_schema_reader.cli_context import GlobalContext
from ocx_schema_reader import INFO_COLOR
from ocx_schema_reader.utils import ROOT_DIR

LOG_CONFIG_YAML = "log_config.yaml"
conf = Path(ROOT_DIR) / LOG_CONFIG_YAML

with open(conf) as f:
    log_config = yaml.safe_load(f)

hndle = log_config["handlers"].get("file")
LOG_FILE = hndle.get("filename")
# Set the logging configuration
config.dictConfig(log_config)
bold_seq = "\033[1m"
colorlog_format = f"{bold_seq} " "%(log_color)s " f"{log_config.get('formatters').get('std_out').get('format')}"
colorlog.basicConfig(format=colorlog_format)
logger = logging.getLogger()  # Todo: Color logging does not work from main.py


@shell(prompt=f"CLI > ", intro=f"Starting CLI...")
@pass_context
def cli(ctx):
    """
    Main CLI
    """
    secho(f"Effective log level is: {logging.getLevelName(logger.getEffectiveLevel())}", color=INFO_COLOR)
    ctx.obj = GlobalContext(logger)


@cli.command(short_help="Clear the screen")
def clear():
    """Clear the console window."""
    clear()


@cli.command(short_help="Set the logging level")
@option(
    "--level",
    "-l",
    required=True,
    default="INFO",
    type=Choice(["INFO", "WARNING", "ERROR", "DEBUG"], case_sensitive=False),
)
def set_level(level):
    """Set the application log level"""
    match level.lower():
        case "debug":
            lev = logging.DEBUG
        case "error":
            lev = logging.ERROR
        case "warning":
            lev = logging.WARNING
        case _:
            lev = logging.INFO
    logger.setLevel(lev)
    secho(f"Effective log level: {logging.getLevelName(logger.getEffectiveLevel())}", color=INFO_COLOR)


@cli.command(short_help="Print the logging level")
def log_level():
    """Print the application log handler levels"""
    secho(f"Effective log level: {logging.getLevelName(logger.getEffectiveLevel())}", color=INFO_COLOR)


@cli.command(short_help="List the table options")
@pass_context
def table_defaults(ctx):
    """List the table default settings."""
    glob_ctx = ctx.obj
    fmt = glob_ctx.get_table_format()
    sep = glob_ctx.get_column_separator()
    out = glob_ctx.get_table_output()
    index_rows = glob_ctx.get_row_numbers()
    table = [["Format", "Column seperator", "Output", "Row indexes"], [fmt, sep, out, index_rows]]
    secho(tabulate(table, headers="firstrow"), color=INFO_COLOR)


@cli.command(short_help="Table formatting")
@option(
    "--fmt",
    help="The formatting instruction for tables",
    default="simple",
    type=Choice(
        [
            "plain",
            "simple",
            "github",
            "grid",
            "fancy_grid",
            "pipe",
            "orgtbl",
            "rst",
            "mediawiki",
            "html",
            "latex",
            "latex_raw",
            "latex_booktabs",
            "latex_longtable",
            "tsv",
        ],
        case_sensitive=False,
    ),
)
@option("--sep", help="The column seperator. Default = whitespace", default="")
@option("--output", help="Output the table to a file. Default =stdout`", default="stdout")
@option(
    "--row-numbers",
    "-r",
    help="Index the table rows and output row index in the first column. Default = True",
    default=True,
)
@pass_context
def table_options(ctx, fmt, sep, output, row_numbers):
    """Set the table options"""
    glob_ctx = ctx.obj
    glob_ctx.table_format(fmt)
    glob_ctx.table_output(output)
    glob_ctx.table_column_separator(sep)
    glob_ctx.table_row_numbers(row_numbers)


cli.add_command(schema)
""" The schema sub-commands """

if __name__ == "__main__":
    cli()
    # from ocx_schema_reader.cli import schema
    # Execute the CLI but force its name to not let Click defaults to:
    # "python -m ocx_schema_reader".
    # schema(prog_name=schema.name)
