#  Copyright (c) 2022.  OCX Consortium https://3docx.org. See the LICENSE

from typing import Any, DefaultDict, Dict
from logging import Logger
import validators

import click


class UrlParamType(click.ParamType):
    """Check if the param is a valid URL and can be accessed"""

    name = "url"

    def convert(self, value, param, ctx):
        """Parameter validator"""

        if validators.url(value):
            return value
        else:
            self.fail(f"{value!r} is not a valid url", param, ctx)


class GlobalContext:
    """Class holding global context information to be shared between subcommands

    Attributes:
        _tools: Pointers to toolset that can be shared
        _table_format: The formatting used when outputting tables. Default=`outline`
        _table_output: Output tables to a file or `stdout` (default)
        _cli_commands: List of commands from the main CLI. Can be accessed from any sub-command
        _main_ctx: The main ``click.Context`` instance
    """

    def __init__(self, logger: Logger, ctx: click.Context):
        self._logger = logger
        self._tools: Dict[Any] = {}
        self._table_format: str = "simple"
        self._table_output: str = "stdout"
        self._table_column_separator: str = "U+0020"  # Whitespace
        self._row_numbers = True
        self._cli_commands = []
        self._main_ctx = ctx

    def register_tool(self, tool: Any):
        """Register a class instance with the global context"""
        self._tools[tool.__class__.__name__] = tool
        self._logger.debug(f"Registered class: {tool.__class__.__name__}")

    def get_tool(self, name: str) -> Any:
        """Return the tool with name `name`"""
        return self._tools.get(name)

    def get_logger(self) -> Logger:
        """Return the python `Logger` object"""
        return self._logger

    def register_command(self, command: str):
        """Register a command with the global context object
        Args:
            command: The command name

        """
        self._cli_commands.append(command)

    def get_main_command_context(self) -> click.Context:
        """Return the main CLI context object"""
        return self._main_ctx

    def table_format(self, fmt: str = "simple"):
        """Set the table formatter option
        Args:
            fmt: set output table format; supported formats:
                      plain, simple, github, grid, fancy_grid, pipe,
                      orgtbl, rst, mediawiki, html, latex, latex_raw,
                      latex_booktabs, latex_longtable, tsv
                      (default: simple)
        """
        self._table_format = fmt

    def table_output(self, file: str = "stdout"):
        """Print tables to a file.

        Args:
            file: The file name for table output. Subsequent table output will be amended to the end of the file.
                    Default = `stdout`

        """
        self._table_output = file

    def table_column_separator(self, sep: str = "U+0020"):
        """Set the table column character separator.

        Args:
            sep: The column separator character  for tables. Default = whitespace

        """
        self._table_column_separator = sep

    def get_column_separator(self) -> str:
        """Get the table column character separator.

        Returns:
            sep: The table column separator character for tables

        """
        return self._table_column_separator

    def get_table_output(self) -> str:
        """Get the table output destination.

        Returns:
            file: The file name for table output. Subsequent table output will be amended to the end of the file.
                    Default = `stdout`

        """
        return self._table_output

    def get_table_format(self) -> str:
        """Get the table formatter option

        Returns:
            fmt: The output table format

        """
        return self._table_format

    def table_row_numbers(self, row_number: bool = True):
        """Index all table rows.

        Args:
            row_number: True if table rows are indexed, False otherwise. Default = True

        """
        self._row_numbers = row_number

    def get_row_numbers(self) -> bool:
        """The table row index flag.

        Returns:
            sep: Row index flag

        """
        return self._row_numbers
