#  Copyright (c) 2023.  OCX Consortium https://3docx.org. See the LICENSE
from __future__ import annotations

import logging
from logging import config

import colorlog
from click import Choice, clear, option, pass_context, secho
from click_shell import shell
from tabulate import tabulate

import ocx_tools
import ocx_tools.cli
from ocx_tools.cli import APP, ERROR_COLOR, INFO_COLOR, LOGO_COLOR, log_config
from ocx_tools.schema import SCHEMA_FOLDER
from ocx_tools.schema.parser import OcxSchema

from .cli_context import GlobalContext
from .schema import schema

LOGO = r"""
             ,----..                                    
            /   /   \    ,----..   ,--,     ,--,  
           /   .     :  /   /   \  |'. \   / .`|                  
          .   /   ;.  \|   :     : ; \ `\ /' / ;  
         .   ;   /  ` ;.   |  ;. / `. \  /  / .'          ______   ___    ___   _     _____
         ;   |  ; \ ; |.   ; /--`   \  \/  / ./          |      | /   \  /   \ | |   / ___/
         |   :  | ; | ';   | ;       \  \.'  /     _____ |      ||     ||     || |  (   \_ 
         .   |  ' ' ' :|   : |        \  ;  ;     |     ||_|  |_||  O  ||  O  || |___\__  |
         '   ;  \; /  |.   | '___    / \  \  \    |_____|  |  |  |     ||     ||     /  \ |
          \   \  ',  / '   ; : .'|  ;  /\  \  \            |  |  |     ||     ||     \    |
           ;   :    /  '   | '/  :./__;  \  ;  \           |__|   \___/  \___/ |_____|\___|                                         
            \   \ .'   |   :    / |   : / \  \  ;                                          
             `---`      \   \ .'  ;   |/   \  ' |                                          
                         `---`    `---'     `--`            
    """

# Set the logging configuration
config.dictConfig(log_config)
bold_seq = "\033[1m"
colorlog_format = (
    f"{bold_seq} "
    "%(log_color)s "
    f"{log_config.get('formatters').get('std_out').get('format')}"
)
colorlog.basicConfig(format=colorlog_format)
logger = logging.getLogger()  # Todo: Color logging does not work from main.py


@shell(prompt=f"{APP} > ", intro=f"Starting {APP}...")
@pass_context
def cli(ctx):
    """
    Main CLI
    """

    secho(LOGO, fg=LOGO_COLOR)
    secho(f"Version: {ocx_tools.__version__}", fg=INFO_COLOR)
    secho("Copyright (c) 2023. OCX Consortium https://3docx.org\n", fg=INFO_COLOR)
    secho(
        f"Effective log level is: {logging.getLevelName(logger.getEffectiveLevel())}",
        fg=INFO_COLOR,
    )
    ctx.obj = GlobalContext(logger, ctx)
    # add tools to the context
    ctx.obj.register_tool(OcxSchema(logger, SCHEMA_FOLDER))
    # Register the cli commands with the app context object
    glob_ctx = ctx.obj
    for command in cli.list_commands(ctx):
        glob_ctx.register_command(command)


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
    secho(
        f"Effective log level: {logging.getLevelName(logger.getEffectiveLevel())}",
        fg=INFO_COLOR,
    )


@cli.command(short_help="Print the logging level")
def log_level():
    """Print the application logging levels"""
    secho(
        f"Effective log level: {logging.getLevelName(logger.getEffectiveLevel())}",
        fg=INFO_COLOR,
    )


@cli.command(short_help="List the table options")
@pass_context
def table_defaults(ctx):
    """List the table default settings."""
    glob_ctx = ctx.obj
    fmt = glob_ctx.get_table_format()
    sep = glob_ctx.get_column_separator()
    out = glob_ctx.get_table_output()
    index_rows = glob_ctx.get_row_numbers()
    table = [
        ["Format", "Column seperator", "Output", "Row indexes"],
        [fmt, sep, out, index_rows],
    ]
    secho(tabulate(table, headers="firstrow"), fg=INFO_COLOR)


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
@option(
    "--output", help="Output the table to a file. Default =stdout`", default="stdout"
)
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


# Arrange all command groups
cli.add_command(schema)
""" The schema sub-commands """
