#  Copyright (c) 2022. OCX Consortium https://3docx.org. See the LICENSE

"""Allow the module to be run as a CLI. I.e.:
.. code-block:: shell-session
    $ python -m meta_package_manager
Removes empty string and current working directory from the first entry of
`sys.path`, if present to avoid using current directory
in subcommands when invoked as `python -m meta_package_manager <command>`.
"""

from __future__ import annotations

from click import Choice, clear, option, pass_context, secho
from click_shell import shell
from tabulate import tabulate

from ocx_schema_reader import ERROR_COLOR, INFO_COLOR
from ocx_schema_reader.cli import schema
from ocx_schema_reader.cli_context import GlobalContext


@shell(prompt=f"CLI > ", intro=f"Starting CLI...")
@pass_context
def cli(ctx):
    """
    Main CLI
    """
    ctx.obj = GlobalContext()


@cli.command(short_help="Clear the screen")
def clear():
    """Clear the console window."""
    clear()


@cli.command(short_help="Clear the screen")
def clear():
    """Clear the console window."""
    clear()


@cli.command(short_help="List the table options")
@pass_context
def table_defaults(ctx):
    """List the table default settings."""
    glob_ctx = ctx.obj
    fmt = glob_ctx.get_table_format()
    sep = glob_ctx.get_column_separator()
    out = glob_ctx.get_table_output()
    index_rows = glob_ctx.table_row_numbering()
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
@pass_context
def table_options(ctx, fmt, sep, output):
    """Set the table options"""
    glob_ctx = ctx.obj
    glob_ctx.table_format(fmt)
    glob_ctx.table_output(output)
    glob_ctx.table_column_separator(sep)


cli.add_command(schema)
""" The schema sub-commands """

if __name__ == "__main__":
    cli()
    # from ocx_schema_reader.cli import schema
    # Execute the CLI but force its name to not let Click defaults to:
    # "python -m ocx_schema_reader".
    # schema(prog_name=schema.name)
